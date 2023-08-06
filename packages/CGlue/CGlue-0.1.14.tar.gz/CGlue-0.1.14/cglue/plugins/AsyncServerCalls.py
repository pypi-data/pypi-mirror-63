import chevron

from cglue.function import FunctionImplementation, FunctionPrototype
from cglue.ports import PortType
from cglue.cglue import Plugin, CGlue
from cglue.signal import SignalType, SignalConnection
from cglue.utils.common import indent


def _add_instance_check(assignment, provider_instance):
    return f'if (instance == &{provider_instance.instance_var_name})\n' \
           f'{{\n' \
           f'{indent(assignment)}\n' \
           f'}}'


def _port_component_is_instanced(context, port_name):
    component_instance_name = port_name.split('/', 2)[0]
    component_instance = context['component_instances'][component_instance_name]

    return component_instance.component.config['multiple_instances']


# FIXME clean up implementation
# FIXME see what can be done about duplicated pass-by-pointer logic
# TODO: multiple callers to the same server
class AsyncServerCallSignal(SignalType):
    def __init__(self):
        super().__init__('single', {'update_on'})

    def create(self, context, connection: SignalConnection):
        provider_instance_name = connection.provider
        port = context.get_port(provider_instance_name)

        provider_component_instance_name = provider_instance_name.split('/', 2)[0]
        provider_instance = context['component_instances'][provider_component_instance_name]

        # updater function is unique for each signal, no need for instance argument
        update_function = FunctionImplementation(FunctionPrototype(connection.name + '_Update', 'void'))

        # create updater function
        context['functions'][provider_instance_name] = {'update': update_function}

        stored_arguments = []
        callee_arguments = {}

        indentation = ' ' * 12
        arg_prefix = '\n' + indentation

        port_args = port.get('arguments', {}).copy()
        if _port_component_is_instanced(context, provider_instance_name):
            callee_arguments['instance'] = arg_prefix + '&' + provider_instance.instance_var_name
            del port_args['instance']
            context['used_types'].append(port._owner.instance_type)

        for name, arg_data in port_args.items():
            if type(arg_data) is str:
                arg_dir = 'in'
                arg_type = context.types.get(arg_data)
            else:
                arg_dir = arg_data['direction']
                arg_type = context.types.get(arg_data['data_type'])

            stored_arguments.append({'name': name, 'type': arg_type.name})

            if arg_dir == 'out' or arg_type.passed_by() == 'pointer':
                callee_arguments[name] = f'{arg_prefix}&{connection.name}_argument_{name}'
            else:
                callee_arguments[name] = f'{arg_prefix}{connection.name}_argument_{name}'

        context['declarations'].append(chevron.render(**{
            'template':
                '\n/* {{ signal_name }} */\n'
                'static AsyncOperationState_t {{ signal_name }}_state = AsyncState_Idle;\n'
                'static AsyncCommand_t {{ signal_name }}_command = AsyncCommand_None;\n'
                '{{# arguments }}'
                'static {{ type }} {{ signal_name }}_argument_{{ name }};\n'
                '{{/ arguments }}'
                'static {{ updater_header }};',
            'data': {
                'signal_name': connection.name,
                'arguments': stored_arguments,
                'updater_header': update_function.get_header()
            }
        }))
        context['used_types'].append('AsyncOperationState_t')
        context['used_types'].append('AsyncCommand_t')

        # generate the updater function
        if 'run' in port.functions:
            self._generate_sync_updater_impl(callee_arguments, connection, port, update_function)

        elif 'async_run' in port.functions:
            self._generate_async_updater_impl(callee_arguments, connection, port, update_function)
        else:
            raise NotImplementedError

    def _generate_async_updater_impl(self, callee_arguments, connection, port, update_function):
        lock, unlock = self._get_lock_impl(connection)

        # long running handler function
        update_function.add_body(chevron.render(**{
            'template': '''{{ lock }}
AsyncCommand_t command = {{ signal_name }}_command;
{{ signal_name }}_command = AsyncCommand_None;

switch (command)
{
    case AsyncCommand_Start:
        {{ signal_name }}_state = AsyncOperationState_Busy;
        {{ unlock }}

        AsyncResult_t result = {{ run_call }};
        switch (result)
        {
            case AsyncResult_Ok:
                {{ signal_name }}_state = AsyncOperationState_Done;
                break;

            case AsyncResult_Pending:
                break;

            default:
                ASSERT(0);
                break;
        }
        break;

    case AsyncCommand_None:
        if ({{ signal_name }}_state == AsyncOperationState_Busy)
        {
            {{ unlock }}

            AsyncResult_t result = {{ run_call }};
            switch (result)
            {
                case AsyncResult_Ok:
                    {{ signal_name }}_state = AsyncOperationState_Done;
                    break;

                case AsyncResult_Pending:
                    break;

                default:
                    ASSERT(0);
                    break;
            }
        }
        else
        {
            {{ unlock }}
        }
        break;

    case AsyncCommand_Cancel:
        if ({{ signal_name }}_state == AsyncOperationState_Busy)
        {
            {{ unlock }}
            (void) {{ cancel_call }};
        }
        else
        {
            {{ unlock }}
        }
        {{ signal_name }}_state = AsyncState_Idle;
        break;

    default:
        {{ unlock }}
        ASSERT(0);
        break;
}
''',
            'data': {
                'lock': lock,
                'unlock': unlock,
                'run_call': port.functions['async_run'].generate_call(
                    {'asyncCommand': 'command', **callee_arguments}),
                'cancel_call': port.functions['async_run'].generate_call(
                    {'asyncCommand': 'AsyncCommand_Cancel', **callee_arguments}),
                'signal_name': connection.name
            }
        }))

    def _generate_sync_updater_impl(self, callee_arguments, connection, port, update_function):
        lock, unlock = self._get_lock_impl(connection)

        # simple handler function to wrap synchronous runnables
        update_function.add_body(chevron.render(**{
            'template': '''{{ lock }}
AsyncCommand_t command = {{ signal_name }}_command;
{{ signal_name }}_command = AsyncCommand_None;

switch (command)
{
    case AsyncCommand_Start:
        {{ signal_name }}_state = AsyncState_Busy;
        {{ unlock }}

        {{{ call }}};

        {{ signal_name }}_state = AsyncState_Done;
        break;

    case AsyncCommand_Cancel:
        {{ unlock }}
        {{ signal_name }}_state = AsyncState_Idle;
        break;

    default:
        {{ unlock }}
        break;
}''',
            'data': {
                'lock': lock,
                'unlock': unlock,
                'call': port.functions['run'].generate_call(callee_arguments),
                'signal_name': connection.name
            }
        }))

    def generate_provider(self, context, connection: SignalConnection, provider_name):
        return {}

    def generate_consumer(self, context, connection: SignalConnection, consumer_instance_name, attributes):
        provider_instance_name = connection.provider
        provider_port = context.get_port(provider_instance_name)
        consumer_port_name = context.get_component_ref(consumer_instance_name)

        port_functions = context['functions'][consumer_port_name]

        call_function = port_functions['async_call']
        result_function = port_functions['get_result']
        update_function = context['functions'][connection.provider]['update']

        lock, unlock = self._get_lock_impl(connection)

        consumer_component_instance_name = consumer_instance_name.split('/', 2)[0]
        consumer_instance = context['component_instances'][consumer_component_instance_name]

        consumer_is_multiple_instance = _port_component_is_instanced(context, consumer_instance_name)
        provider_is_multiple_instance = _port_component_is_instanced(context, provider_instance_name)

        call_mods = self.generate_call_function(
            context.types, attributes.get('arguments', {}), call_function.prototype.arguments, connection,
            consumer_instance_name, provider_instance_name, provider_port['arguments'], lock, unlock)

        result_arg_names = list(result_function.arguments.keys())
        if provider_is_multiple_instance:
            result_arg_names.pop(0)

        get_result_mods = self.generate_get_result_function(call_function, connection, result_arg_names, lock, unlock)

        cancel_mods = {
            'body': f'{connection.name}_command = AsyncCommand_Cancel;',
            'used_arguments': []
        }

        update_call_mods = {
            'body': update_function.prototype.generate_call({}) + ';'
        }

        if consumer_is_multiple_instance:
            cancel_mods['used_arguments'].append('instance')
            get_result_mods['used_arguments'].append('instance')

            busy_value = context.types.get('AsyncOperationState_t').render_value('AsyncState_Busy')

            cancel_mods['body'] = _add_instance_check(cancel_mods['body'], consumer_instance)
            call_mods['body'] = _add_instance_check(call_mods['body'], consumer_instance)
            call_mods['return_statement'] = busy_value
            get_result_mods['body'] = _add_instance_check(get_result_mods['body'], consumer_instance)
            get_result_mods['return_statement'] = busy_value

        return {
            connection.attributes['update_on']: {
                'run': update_call_mods
            },
            consumer_port_name: {
                'cancel': cancel_mods,
                'get_result': get_result_mods,
                'async_call': call_mods
            }
        }

    @staticmethod
    def generate_get_result_function(call_function, connection, result_arg_names, lock, unlock):
        # get result
        # if the provider doesn't have an out arg, the default value for the type is passed back
        result_arguments = []
        used_arguments = []
        for arg_name in result_arg_names:
            if arg_name not in call_function.arguments:
                value = f'{connection.name}_argument_{arg_name}'
            else:
                value = call_function.arguments[arg_name]['data_type'].render_value(None)

            used_arguments.append(arg_name)
            result_arguments.append({'name': arg_name, 'value': value})

        result_body = chevron.render(**{
            'template': '''AsyncOperationState_t returned_state;
{{ lock }}
switch ({{ signal_name }}_state)
{
    case AsyncState_Done:
{{# arguments }}
        if ({{ name }})
        {
            *{{ name }} = {{{ value }}};
        }
{{/ arguments }}
        {{ signal_name }}_state = AsyncState_Idle;
        {{ unlock }}
        returned_state = AsyncState_Done;
        break;

    case AsyncState_Started:
        {{ unlock }}
        returned_state = AsyncState_Busy;
        break;

    default:
        {{ unlock }}
        returned_state = {{ signal_name }}_state;
        break;
}
return returned_state;''',
            'data': {
                'signal_name': connection.name,
                'lock': lock,
                'unlock': unlock,
                'arguments': result_arguments
            }
        })
        return {
            'body': result_body,
            'used_arguments': used_arguments
        }

    @staticmethod
    def generate_call_function(types, signal_args, call_function_args, connection, consumer_instance_name,
                               provider_instance_name, provider_args, lock, unlock):
        # generate the caller functions
        extra_args = set(signal_args.keys()) - provider_args.keys()
        if extra_args:
            print(f'Warning: extra argument "{", ".join(extra_args)}" on signal'
                  f' {provider_instance_name}, consumed by {consumer_instance_name}')

        call_arguments, missing_arguments = AsyncServerCallSignal._get_consumer_call_args(
            signal_args, call_function_args, provider_args, types)

        if missing_arguments:
            raise Exception(f'{consumer_instance_name} does not provide {provider_instance_name} with'
                            f' the following in-arguments: {", ".join(missing_arguments)}')

        call_body = chevron.render(**{
            'template': '''AsyncOperationState_t returned_state = AsyncState_Busy;
{{ signal_name }}_command = AsyncCommand_None;
{{ lock }}
if ({{ signal_name}}_state == AsyncState_Idle || {{ signal_name}}_state == AsyncState_Done)
{
    {{ signal_name}}_state = AsyncState_Started;
    {{ unlock }}

{{# arguments }}
    {{ signal_name }}_argument_{{ name }} = {{# by_pointer }}*{{/ by_pointer }}{{ value }};
{{/ arguments }}

    returned_state = AsyncState_Started;
    {{ signal_name }}_command = AsyncCommand_Start;
}
else
{
    {{ unlock }}
}
return returned_state;''',
            'data': {
                'signal_name': connection.name,
                'lock': lock,
                'unlock': unlock,
                'arguments': call_arguments
            }
        })
        return {
            'body': call_body,
            'used_arguments': call_function_args
        }

    @staticmethod
    def _get_consumer_call_args(signal_arguments, function_args, provider_port_args, types):
        call_arguments = []
        missing_arguments = set()
        for arg, data in provider_port_args.items():
            arg_type = types.get(data['data_type'])

            if data['direction'] == 'in':
                if arg in signal_arguments:
                    # there is a config entry in the runtime config for this argument
                    config_value = signal_arguments[arg]
                    if config_value in function_args:
                        # argument remapping (different names, same types)
                        if arg_type != function_args[config_value]['data_type']:
                            raise Exception('Incompatible port types')

                        call_arguments.append({
                            'name': arg,
                            'value': config_value,
                            'by_pointer': arg_type.passed_by() == 'pointer'
                        })
                    else:
                        # constant value
                        call_arguments.append({
                            'name': arg,
                            'value': arg_type.render_value(config_value),
                            'by_pointer': False
                        })
                elif arg in function_args:
                    # connect arguments by name
                    call_arguments.append({
                        'name': arg,
                        'value': arg,
                        'by_pointer': arg_type.passed_by() == 'pointer'
                    })
                else:
                    missing_arguments.add(arg)

        return call_arguments, missing_arguments

    @staticmethod
    def _get_lock_impl(connection):
        if 'no_locks' not in connection.attributes or not connection.attributes['no_locks']:
            lock = '__disable_irq();'
            unlock = '__enable_irq();'
        else:
            lock = ''
            unlock = ''
        return lock, unlock


class AsyncCallPortType(PortType):
    def __init__(self, types):
        super().__init__(types, {
            'order':          1,
            'consumes':       {'async_call': 'multiple'},
            'def_attributes': {
                'required': [],
                'optional': {"arguments": {}},
                'static':   {}
            }
        })

    def declare_functions(self, port):
        call_fn_name = f'{port.component_name}_Async_{port.port_name}_Call'
        result_fn_name = f'{port.component_name}_Async_{port.port_name}_GetResult'
        cancel_fn_name = f'{port.component_name}_Async_{port.port_name}_Cancel'

        call_function = port.declare_function(call_fn_name, 'AsyncOperationState_t')
        result_function = port.declare_function(result_fn_name, 'AsyncOperationState_t')
        cancel_function = port.declare_function(cancel_fn_name, 'void')

        for name, arg_data in port.get('arguments', {}).items():
            if type(arg_data) is str:
                call_function.arguments.add(name, 'in', self._types.get(arg_data))
            elif arg_data['direction'] == 'in':
                call_function.arguments.add(name, 'in', self._types.get(arg_data['data_type']))
            else:
                result_function.arguments.add(name, 'out', self._types.get(arg_data['data_type']))

        return {
            'async_call': call_function,
            'get_result': result_function,
            'cancel': cancel_function
        }

    def create_component_functions(self, port):
        declared_functions = port.functions

        call_fn = FunctionImplementation(declared_functions['async_call'])
        call_fn.attributes.add('weak')
        call_fn.set_return_statement('AsyncState_Busy')

        result_fn = FunctionImplementation(declared_functions['get_result'])
        result_fn.attributes.add('weak')
        result_fn.set_return_statement('AsyncState_Busy')

        cancel_fn = FunctionImplementation(declared_functions['cancel'])
        cancel_fn.attributes.add('weak')

        return {'async_call': call_fn, 'get_result': result_fn, 'cancel': cancel_fn}

    def create_runtime_functions(self, port):
        declared_functions = port.functions

        call_fn = FunctionImplementation(declared_functions['async_call'])
        result_fn = FunctionImplementation(declared_functions['get_result'])
        cancel_fn = FunctionImplementation(declared_functions['cancel'])

        return {'async_call': call_fn, 'get_result': result_fn, 'cancel': cancel_fn}


class AsyncRunnablePortType(PortType):
    def __init__(self, types):
        super().__init__(types, {
            'order':          1,
            'provides':       {'async_call'},
            'def_attributes': {
                'required': [],
                'optional': {"arguments": {}},
                'static':   {}
            }
        })

    def declare_functions(self, port):
        fn_name = f'{port.component_name}_AsyncRunnable_{port.port_name}'

        function = port.declare_function(fn_name, 'AsyncResult_t')

        function.arguments.add('asyncCommand', 'in', self._types.get('AsyncCommand_t'))

        for name, arg_data in port.get('arguments', {}).items():
            if type(arg_data) is str:
                data_type = arg_data
                direction = 'in'
            else:
                data_type = arg_data['data_type']
                direction = arg_data['direction']

            function.arguments.add(name, direction, self._types.get(data_type))

        return {
            'async_run': function
        }

    def create_component_functions(self, port):
        function = FunctionImplementation(port.functions['async_run'])

        return {'async_run': function}

    def create_runtime_functions(self, port):
        return {}


def init(owner: CGlue):
    types = owner.types

    types.add(
        'AsyncOperationState_t',
        types.category('enum').process_type({
            'values': [
                'AsyncState_Idle',
                'AsyncState_Started',
                'AsyncState_Busy',
                'AsyncState_Done'
            ],
            'default_value': 'AsyncState_Idle'
        }),
        "builtin type"
    )
    types.add(
        'AsyncCommand_t',
        types.category('enum').process_type({
            'values': [
                'AsyncCommand_None',
                'AsyncCommand_Start',
                'AsyncCommand_Continue',
                'AsyncCommand_Cancel'
            ],
            'default_value': 'AsyncCommand_None'
        }),
        "builtin type"
    )
    types.add(
        'AsyncResult_t',
        types.category('enum').process_type({
            'values': [
                'AsyncResult_Pending',
                'AsyncResult_Ok'
            ],
            'default_value': 'AsyncResult_Pending'
        }),
        "builtin type"
    )

    add_event_to = ['Runnable']
    for port_type, known_port_type in owner.port_types.items():
        if port_type in add_event_to:
            known_port_type['provides'].add('async_call')

    owner.add_signal_type('async_call', AsyncServerCallSignal())
    owner.add_port_type('AsyncServerCall', AsyncCallPortType(types))
    owner.add_port_type('AsyncRunnable', AsyncRunnablePortType(types))


def async_server_calls():
    return Plugin("AsyncServerCalls", {
        'init': init,
    }, requires=['BuiltinDataTypes', 'RuntimeEvents'])
