import chevron

from cglue.function import FunctionImplementation
from cglue.utils.common import chevron_list_mark_last, dict_to_chevron_list, indent
from cglue.ports import PortType
from cglue.data_types import TypeCollection, TypeCategory
from cglue.cglue import Plugin, CGlue
from cglue.signal import SignalConnection, SignalType
from cglue.component import Component


class StructType(TypeCategory):

    def __init__(self, type_collection):
        attributes = {
            'required': ['fields'],
            'optional': {
                'pass_semantic': TypeCollection.PASS_BY_POINTER,
                'default_value': {}
            },
            'static': {
                'type': TypeCollection.STRUCT
            }
        }
        super().__init__(type_collection, 'struct', attributes)

    def render_typedef(self, type_name, type_data):
        context = {
            'template': "\n"
                        "typedef struct {\n"
                        "    {{# fields }}\n"
                        "    {{ type }} {{ name }};\n"
                        "    {{/ fields }}\n"
                        "} {{ type_name }};",

            'data': {
                'type_name': type_name,
                'fields': dict_to_chevron_list(type_data['fields'], key_name='name', value_name='type')
            }
        }

        return chevron.render(**context)

    def render_value(self, type_name, type_data, value, context='assignment'):
        if type(value) is str:
            return value

        types = self._type_collection
        field_types = type_data['fields']
        field_values = {field_name: value.get(field_name) for field_name in field_types}

        def render(field_name, field_value):
            """Render field values"""
            return types.get(field_types[field_name]).render_value(field_value, 'initialization')

        rendered_values = {name: render(name, value) for name, value in field_values.items()}

        rendered_field_values = (f'.{name} = {rendered}' for name, rendered in rendered_values.items())

        fields_str = ', '.join(rendered_field_values)
        if context == 'initialization':
            return f'{{ {fields_str} }}'
        else:
            return f'({type_name}) {{ {fields_str} }}'

    def attribute(self, type_name, type_data, name):
        if name == 'default_value':
            # if a struct member does not have default value, look for it recursively
            default = type_data['default_value']
            struct_fields = type_data['fields']

            def default_value(field_name):
                # use 'or' so we only look up the default for the field if it is not given in the struct data
                return default.get(field_name) or self._type_collection.get(struct_fields[field_name]).default_value()

            return {name: default_value(name) for name in struct_fields}
        else:
            return super().attribute(type_name, type_data, name)

    def referenced_types(self, type_name, type_data):
        yield from type_data['fields'].values()
        yield from super().referenced_types(type_name, type_data)


class EnumType(TypeCategory):

    def __init__(self, type_collection):
        attributes = {
            'required': ['values', 'default_value'],
            'optional': {'pass_semantic': TypeCollection.PASS_BY_VALUE},
            'static': {
                'type': TypeCollection.ENUM
            }
        }
        super().__init__(type_collection, 'enum', attributes)

    def render_typedef(self, type_name, type_data):
        context = {
            'template': "\n"
                        "typedef enum {\n"
                        "    {{# values }}\n"
                        "    {{ value }}{{^ last }},{{/ last }}\n"
                        "    {{/ values }}\n"
                        "} {{ type_name }};",

            'data': {
                'type_name': type_name,
                'values': chevron_list_mark_last([{'value': value} for value in type_data['values']])
            }
        }

        return chevron.render(**context)


class UnionType(TypeCategory):

    def __init__(self, type_collection):
        attributes = {
            'required': ['members', 'default_value'],
            'optional': {'pass_semantic': TypeCollection.PASS_BY_POINTER},
            'static': {
                'type': TypeCollection.UNION
            }
        }
        super().__init__(type_collection, 'union', attributes)

    def render_typedef(self, type_name, type_data):
        context = {
            'template': "\n"
                        "typedef union {\n"
                        "    {{# members }}\n"
                        "    {{ type }} {{ name }};\n"
                        "    {{/ members }}\n"
                        "} {{ type_name }};",

            'data': {
                'type_name': type_name,
                'members': dict_to_chevron_list(type_data['members'], key_name='name', value_name='type')
            }
        }

        return chevron.render(**context)

    def render_value(self, type_name, type_data, value, context='assignment'):
        if type(value) is str:
            return value

        if len(value) != 1:
            raise Exception('Only a single union member can be assigned')

        members = {name: self._type_collection.get(member_type) for name, member_type in type_data['members'].items()}
        values_str = ', '.join(f'.{name} = {members[name].render_value(value, "initialization")}'
                               for name, value in value.items())
        if context == 'initialization':
            return f'{{ {values_str} }}'
        else:
            return f'({type_name}) {{ {values_str} }}'

    def referenced_types(self, type_name, type_data):
        yield from type_data['members'].values()
        yield from super().referenced_types(type_name, type_data)


def lookup_member(types: TypeCollection, data_type, member_list):
    keys = {
        TypeCollection.STRUCT: 'fields',
        TypeCollection.UNION: 'members'
    }

    for member in member_list:
        type_data = types.get(data_type)

        try:
            member_key = keys[type_data['type']]
            members = type_data[member_key]

            data_type = members[member]
        except KeyError:
            raise Exception(f'Trying to access member of non-struct type {data_type}')

    return data_type


def create_member_accessor(member):
    return '.' + member


def process_member_access(types: TypeCollection, attributes, provided_data_type, consumed_data_type):
    if 'member' in attributes:
        member_list = attributes['member'].split('.')
        provided_data_type = lookup_member(types, provided_data_type, member_list)
        member_accessor = create_member_accessor(attributes['member'])
    else:
        member_accessor = ''

    if consumed_data_type != provided_data_type:
        raise Exception('Port data types don\'t match')

    return member_accessor, types.get(consumed_data_type)


def _add_instance_check(assignment, provider_instance):
    return f'if (instance == &{provider_instance.instance_var_name})\n' \
           f'{{\n' \
           f'{indent(assignment)}\n' \
           f'}}'


def _port_component_is_instanced(context, port_name):
    component_instance_name = port_name.split('/', 2)[0]
    component_instance = context['component_instances'][component_instance_name]

    return component_instance.component.config['multiple_instances']


class VariableSignal(SignalType):
    def __init__(self):
        super().__init__(consumers='multiple')

    def create(self, context, connection: SignalConnection):
        provider_port_data = context.get_port(connection.provider)
        data_type_name = provider_port_data['data_type']
        data_type = context.types.get(data_type_name)
        init_value = connection.attributes.get('init_value')
        rendered_init_value = data_type.render_value(init_value, 'initialization')
        context['declarations'].append(
            f'static {data_type.name} {connection.name} = {rendered_init_value};'
        )

    def generate_provider(self, context, connection: SignalConnection, provider_instance_name):
        provider_port_data = context.get_port(provider_instance_name)
        provider_port_name = context.get_component_ref(provider_instance_name)
        data_type = context.types.get(provider_port_data['data_type'])
        function = context.functions[provider_port_name]['write']
        argument_names = list(function.arguments.keys())

        provider_component_instance_name = provider_instance_name.split('/', 2)[0]
        provider_instance = context['component_instances'][provider_component_instance_name]

        is_multiple_instances = _port_component_is_instanced(context, provider_instance_name)
        if is_multiple_instances:
            argument_names.pop(0)

        data_arg_name = argument_names[0]
        used_args = [data_arg_name]

        if data_type.passed_by() == TypeCollection.PASS_BY_VALUE:
            assignment = f'{connection.name} = {data_arg_name};'
        else:
            assignment = f'{connection.name} = *{data_arg_name};'

        if is_multiple_instances:
            used_args.append('instance')
            assignment = _add_instance_check(assignment, provider_instance)

        return {
            provider_port_name: {
                'write': {
                    'used_arguments': used_args,
                    'body': assignment
                }
            }
        }

    def generate_consumer(self, context, connection: SignalConnection, consumer_instance_name, attributes):
        provider_port_data = context.get_port(connection.provider)
        consumer_port_data = context.get_port(consumer_instance_name)
        consumer_port_name = context.get_component_ref(consumer_instance_name)

        member_accessor, data_type = process_member_access(context.types, attributes,
                                                           provider_port_data['data_type'],
                                                           consumer_port_data['data_type'])

        consumer_component_instance_name = consumer_instance_name.split('/', 2)[0]
        consumer_instance = context['component_instances'][consumer_component_instance_name]

        function = context.functions[consumer_port_name]['read']
        argument_names = list(function.arguments.keys())

        is_multiple_instances = _port_component_is_instanced(context, consumer_instance_name)
        provider_is_multiple_instance = _port_component_is_instanced(context, connection.provider)
        if is_multiple_instances:
            argument_names.pop(0)

        used_args = []
        return_statement = None
        if data_type.passed_by() == TypeCollection.PASS_BY_VALUE:
            read = f'return {connection.name}{member_accessor};'

            if provider_is_multiple_instance:
                return_statement = data_type.render_value(None)
        else:
            out_name = argument_names[0]
            read = f'*{out_name} = {connection.name}{member_accessor};'
            used_args.append(out_name)

        if provider_is_multiple_instance:
            used_args.append('instance')
            read = _add_instance_check(read, consumer_instance)

        mods = {
            'body': read,
            'used_arguments': used_args
        }
        if return_statement:
            mods['return_statement'] = return_statement

        return {
            consumer_port_name: {
                'read': mods
            }
        }


class ArraySignal(SignalType):
    def __init__(self):
        super().__init__(consumers='multiple')

    def create(self, context, connection: SignalConnection):
        provider_port_data = context.get_port(connection.provider)
        data_type_name = provider_port_data['data_type']
        data_type = context.types.get(data_type_name)
        count = provider_port_data['count']

        try:
            # either all init values are specified
            init_values = connection.attributes['init_values']
        except KeyError:
            # ... or a single one is
            init_value = connection.attributes.get('init_value')
            init_values = [data_type.render_value(init_value, 'initialization')] * count

        if type(init_values) is list:
            if len(init_values) != count:
                raise Exception(f'Array initializer count ({len(init_values)}) does not '
                                f'match size ({count}) - signal provided by {connection.provider}')

            init_values = ', '.join(init_values)

        context['declarations'].append(f'static {data_type.name} {connection.name}[{count}] = {{ {init_values} }};')

    def generate_provider(self, context, connection: SignalConnection, provider_instance_name):
        provider_port_data = context.get_port(provider_instance_name)
        provider_port_name = context.get_component_ref(provider_instance_name)
        data_type = context.types.get(provider_port_data['data_type'])

        function = context.functions[provider_port_name]['write']
        argument_names = list(function.arguments.keys())

        provider_component_instance_name = provider_instance_name.split('/', 2)[0]
        provider_instance = context['component_instances'][provider_component_instance_name]

        is_multiple_instances = _port_component_is_instanced(context, provider_instance_name)
        if is_multiple_instances:
            argument_names.pop(0)

        index, value = argument_names
        used_args = [index, value]

        if data_type.passed_by() == TypeCollection.PASS_BY_VALUE:
            body = f'{connection.name}[{index}] = {value};'
        else:
            body = f'{connection.name}[{index}] = *{value};'

        if is_multiple_instances:
            used_args.append('instance')
            body = _add_instance_check(body, provider_instance)

        return {
            provider_port_name: {
                'write': {
                    'used_arguments': used_args,
                    'body': body
                }
            }
        }

    def generate_consumer(self, context, connection: SignalConnection, consumer_instance_name, attributes):
        provider_port_data = context.get_port(connection.provider)
        consumer_port_data = context.get_port(consumer_instance_name)
        consumer_port_name = context.get_component_ref(consumer_instance_name)

        member_accessor, data_type = process_member_access(context.types, attributes,
                                                           provider_port_data['data_type'],
                                                           consumer_port_data['data_type'])

        consumer_component_instance_name = consumer_instance_name.split('/', 2)[0]
        consumer_instance = context['component_instances'][consumer_component_instance_name]

        function = context.functions[consumer_port_name]['read']
        argument_names = list(function.arguments.keys())

        is_multiple_instances = _port_component_is_instanced(context, consumer_instance_name)
        provider_is_multiple_instance = _port_component_is_instanced(context, connection.provider)
        if is_multiple_instances:
            argument_names.pop(0)

        used_args = []
        return_statement = None
        if 'count' not in consumer_port_data:
            # single read, index should be next to consumer name
            try:
                index = attributes['index']
            except KeyError:
                raise Exception(f'{consumer_instance_name} tries to read from an array without specifying the element')
        else:
            if consumer_port_data['count'] > provider_port_data['count']:
                raise Exception(
                    f'{consumer_instance_name} signal count ({consumer_port_data["count"]}) '
                    f'is incompatible with {connection.provider} ({provider_port_data["count"]})')

            index = argument_names.pop(0)
            used_args.append(index)

        if data_type.passed_by() == TypeCollection.PASS_BY_VALUE:
            read = f'return {connection.name}[{index}]{member_accessor};'
            if provider_is_multiple_instance:
                return_statement = data_type.render_value(None)
        else:
            out_name = argument_names[0]
            used_args.append(out_name)

            read = f'*{out_name} = {connection.name}[{index}]{member_accessor};'

        if provider_is_multiple_instance:
            used_args.append('instance')
            read = _add_instance_check(read, consumer_instance)

        mods = {
            'body': read,
            'used_arguments': used_args
        }
        if return_statement:
            mods['return_statement'] = return_statement

        return {
            consumer_port_name: {
                'read': mods
            }
        }


class QueueSignal(SignalType):
    def __init__(self):
        super().__init__(consumers='multiple_signals', required_attributes=['queue_length'])

    def create(self, context, connection: SignalConnection):
        if connection.attributes['queue_length'] == 1:
            template = \
                "static {{ data_type }} {{ signal_name }};\n" \
                "static bool {{ signal_name }}_overflow = false;\n" \
                "static bool {{ signal_name }}_data_valid = false;"
        else:
            template = \
                "static {{ data_type }} {{ signal_name }}[{{ queue_length }}u];\n" \
                "static size_t {{ signal_name}}_count = 0u;\n" \
                "static size_t {{ signal_name}}_write_index = 0u;\n" \
                "static bool {{ signal_name }}_overflow = false;"

        provider_port_data = context.get_port(connection.provider)
        data_type_name = provider_port_data['data_type']
        data_type = context.types.get(data_type_name)

        data = {
            'data_type': data_type.name,
            'signal_name': connection.name,
            'queue_length': connection.attributes['queue_length']
        }
        context['declarations'].append(chevron.render(template, data))

    def generate_provider(self, context, connection: SignalConnection, provider_instance_name):
        provider_port_data = context.get_port(provider_instance_name)
        provider_port_name = context.get_component_ref(provider_instance_name)
        data_type = context.types.get(provider_port_data['data_type'])

        if connection.attributes['queue_length'] == 1:
            needs_scope = False
            template = \
                "{{ signal_name }}_overflow = {{ signal_name }}_data_valid;\n" \
                "{{ signal_name }} = {{ value }};\n" \
                "{{ signal_name }}_data_valid = true;"
        else:
            needs_scope = True
            template = \
                "if ({{ signal_name }}_count < {{ queue_length }}u)\n" \
                "{\n" \
                "    ++{{ signal_name }}_count;\n" \
                "}\n" \
                "else\n" \
                "{\n" \
                "    {{ signal_name }}_overflow = true;\n" \
                "}\n" \
                "size_t idx = {{ signal_name }}_write_index;\n" \
                "{{ signal_name }}_write_index = ({{ signal_name }}_write_index + 1u) % {{ queue_length }}u;\n" \
                "{{ signal_name }}[idx] = {{ value }};"

        function = context.functions[provider_port_name]['write']
        argument_names = list(function.arguments.keys())

        provider_component_instance_name = provider_instance_name.split('/', 2)[0]
        provider_instance = context['component_instances'][provider_component_instance_name]

        is_multiple_instances = _port_component_is_instanced(context, provider_instance_name)
        provider_is_multiple_instances = _port_component_is_instanced(context, connection.provider)
        if is_multiple_instances:
            argument_names.pop(0)

        passed_by_value = data_type.passed_by() == TypeCollection.PASS_BY_VALUE
        value_arg = argument_names[0]
        used_args = [value_arg]

        body = chevron.render(template, {
            'queue_length': connection.attributes['queue_length'],
            'signal_name': connection.name,
            'value': value_arg if passed_by_value else '*' + value_arg
        })

        if provider_is_multiple_instances:
            used_args.append('instance')
            body = _add_instance_check(body, provider_instance)
        elif needs_scope:
            body = f'{{\n' \
                   f'{indent(body)}\n' \
                   f'}}'

        return {
            provider_port_name: {
                'write': {
                    'used_arguments': used_args,
                    'body': body
                }
            }
        }

    def generate_consumer(self, context, connection: SignalConnection, consumer_instance_name, attributes):
        provider_port_data = context.get_port(connection.provider)
        consumer_port_data = context.get_port(consumer_instance_name)
        consumer_port_name = context.get_component_ref(consumer_instance_name)

        member_accessor, data_type = process_member_access(context.types, attributes,
                                                           provider_port_data['data_type'],
                                                           consumer_port_data['data_type'])

        if connection.attributes['queue_length'] == 1:
            template = \
                "bool was_overflow = {{ signal_name }}_overflow;\n" \
                "if ({{ signal_name }}_data_valid)\n" \
                "{\n" \
                "    {{ signal_name }}_overflow = false;\n" \
                "    {{ out_name }} = {{ signal_name }}{{ member_accessor }};\n" \
                "    {{ signal_name }}_data_valid = false;\n" \
                "    if (was_overflow)\n" \
                "    {\n" \
                "        return QueueStatus_Overflow;\n" \
                "    }\n" \
                "    else\n" \
                "    {\n" \
                "        return QueueStatus_Ok;\n" \
                "    }\n" \
                "}"
        else:
            template = \
                "if ({{ signal_name }}_count > 0u)\n" \
                "{\n" \
                "    size_t idx = ({{ signal_name }}_write_index - {{ signal_name }}_count) % {{ queue_length }}u;\n" \
                "    --{{ signal_name }}_count;\n" \
                "    {{ out_name }} = {{ signal_name }}[idx]{{ member_accessor }};\n" \
                "    \n" \
                "    if ({{ signal_name }}_overflow)\n" \
                "    {\n" \
                "        {{ signal_name }}_overflow = false;\n" \
                "        return QueueStatus_Overflow;\n" \
                "    }\n" \
                "    else\n" \
                "    {\n" \
                "        return QueueStatus_Ok;\n" \
                "    }\n" \
                "}"

        consumer_component_instance_name = consumer_instance_name.split('/', 2)[0]
        consumer_instance = context['component_instances'][consumer_component_instance_name]

        function = context.functions[consumer_port_name]['read']
        argument_names = list(function.arguments.keys())

        is_multiple_instances = _port_component_is_instanced(context, consumer_instance_name)
        provider_is_multiple_instances = _port_component_is_instanced(context, connection.provider)
        if is_multiple_instances:
            argument_names.pop(0)

        value_arg = argument_names[0]
        data = {
            'queue_length': connection.attributes['queue_length'],
            'signal_name': connection.name,
            'out_name': '*' + value_arg,
            'member_accessor': member_accessor
        }

        read = chevron.render(template, data)
        used_args = [value_arg]
        if provider_is_multiple_instances:
            used_args.append('instance')
            read = _add_instance_check(read, consumer_instance)

        return {
            consumer_port_name: {
                'read': {
                    'used_arguments': used_args,
                    'body': read,
                    'return_statement': 'QueueStatus_Empty'
                }
            }
        }


class ConstantSignal(SignalType):
    def __init__(self):
        super().__init__(consumers='multiple')

    def create(self, context, connection: SignalConnection):
        pass

    def generate_provider(self, context, connection: SignalConnection, provider_name):
        return {}

    def generate_consumer(self, context, connection: SignalConnection, consumer_instance_name, attributes):
        provider_port_data = context.get_port(connection.provider)
        consumer_port_data = context.get_port(consumer_instance_name)
        consumer_port_name = context.get_component_ref(consumer_instance_name)

        member_accessor, data_type = process_member_access(context.types, attributes,
                                                           provider_port_data['data_type'],
                                                           consumer_port_data['data_type'])

        consumer_component_instance_name = consumer_instance_name.split('/', 2)[0]
        consumer_instance = context['component_instances'][consumer_component_instance_name]

        function = context.functions[consumer_port_name]['read']
        argument_names = list(function.arguments.keys())

        is_multiple_instances = _port_component_is_instanced(context, consumer_instance_name)
        provider_is_multiple_instances = _port_component_is_instanced(context, connection.provider)
        constant_provider = provider_port_data.functions['constant']

        call_args = {}
        if is_multiple_instances:
            argument_names.pop(0)
            call_args['instance'] = '&' + consumer_instance.instance_var_name

        used_args = []
        return_statement = None
        if data_type.passed_by() == TypeCollection.PASS_BY_VALUE:
            call = constant_provider.generate_call(call_args)
            body = f'return {call}{member_accessor};'
            if provider_is_multiple_instances:
                return_statement = data_type.render_value(None)
        else:
            out_arg_name = argument_names[0]
            used_args.append(out_arg_name)
            if member_accessor:
                call_args['value'] = '&tmp'
                body = f"{data_type.name} tmp;\n" \
                       f"{constant_provider.generate_call(call_args)};\n" \
                       f"{out_arg_name} = tmp{member_accessor};"
            else:
                call_args['value'] = out_arg_name
                body = constant_provider.generate_call(call_args) + ';'

        if provider_is_multiple_instances:
            used_args.append('instance')
            body = _add_instance_check(body, consumer_instance)

        mods = {
            'used_arguments': used_args,
            'body': body
        }
        if return_statement:
            mods['return_statement'] = return_statement

        return {
            consumer_port_name: {
                'read': mods
            }
        }


class ConstantArraySignal(SignalType):
    def __init__(self):
        super().__init__(consumers='multiple')

    def create(self, context, connection: SignalConnection):
        pass

    def generate_provider(self, context, connection: SignalConnection, provider_name):
        return {}

    def generate_consumer(self, context, connection: SignalConnection, consumer_instance_name, attributes):
        provider_port_data = context.get_port(connection.provider)
        consumer_port_data = context.get_port(consumer_instance_name)
        consumer_port_name = context.get_component_ref(consumer_instance_name)

        member_accessor, data_type = process_member_access(context.types, attributes,
                                                           provider_port_data['data_type'],
                                                           consumer_port_data['data_type'])

        consumer_component_instance_name = consumer_instance_name.split('/', 2)[0]
        consumer_instance = context['component_instances'][consumer_component_instance_name]

        function = context.functions[consumer_port_name]['read']
        argument_names = list(function.arguments.keys())

        is_multiple_instances = _port_component_is_instanced(context, consumer_instance_name)
        provider_is_multiple_instances = _port_component_is_instanced(context, connection.provider)
        constant_provider = provider_port_data.functions['constant']

        call_args = {}
        if is_multiple_instances:
            argument_names.pop(0)
            call_args['instance'] = '&' + consumer_instance.instance_var_name

        used_args = []
        if 'count' not in consumer_port_data:
            # single read, index should be next to consumer name
            index = attributes['index']
        else:
            if consumer_port_data['count'] > provider_port_data['count']:
                raise Exception(
                    f'{consumer_instance_name} signal count ({consumer_port_data["count"]}) '
                    f'is incompatible with {connection.provider} ({provider_port_data["count"]})')
            index = argument_names.pop(0)
            used_args.append(index)

        call_args['index'] = index

        return_statement = None
        if data_type.passed_by() == TypeCollection.PASS_BY_VALUE:
            call = constant_provider.generate_call(call_args)
            body = f'return {call}{member_accessor};'
            if provider_is_multiple_instances:
                return_statement = data_type.render_value(None)
        else:
            out_name = argument_names[0]
            used_args.append(out_name)

            if member_accessor:
                call_args['value'] = '&tmp'
                call = constant_provider.generate_call(call_args)
                body = f'{data_type.name} tmp;\n' \
                       f'{call};\n' \
                       f'{out_name} = tmp{member_accessor};'
            else:
                call_args['value'] = out_name
                body = constant_provider.function_call(call_args) + ';'

        if provider_is_multiple_instances:
            used_args.append('instance')
            body = _add_instance_check(body, consumer_instance)

        mods = {
            'body': body,
            'used_arguments': used_args
        }
        if return_statement:
            mods['return_statement'] = return_statement

        return {
            consumer_port_name: {
                'read': mods
            }
        }


def process_type_def(types: TypeCollection, type_name, type_def):
    type_data = type_def.copy()
    # determine type of definition
    if 'type' in type_data:
        type_category = type_data['type']
        del type_data['type']
    else:
        if 'defined_in' in type_data:
            type_category = TypeCollection.EXTERNAL_DEF
        elif 'aliases' in type_data:
            type_category = TypeCollection.ALIAS
        elif 'fields' in type_data:
            type_category = TypeCollection.STRUCT
        elif 'members' in type_data:
            type_category = TypeCollection.UNION
        else:
            raise Exception(f'Invalid type definition for {type_name}')

    try:
        return types.category(type_category).process_type(type_data)
    except KeyError:
        print(f'Unknown type category {type_category} set for {type_name}')
        raise
    except Exception as e:
        raise Exception(f'Type {type_name} ({type_category}) definition is not valid: {e}')


class ReadValuePortType(PortType):
    def __init__(self, types):
        super().__init__(types, {
            'order': 3,
            'consumes': {
                'array': 'single',
                'variable': 'single',
                'constant': 'single',
                'constant_array': 'single'
            },
            'def_attributes': {
                'required': ['data_type'],
                'optional': {'default_value': None},
                'static': {}
            }
        })

    def declare_functions(self, port):
        data_type = self._types.get(port['data_type'])

        fn_name = f'{port.component_name}_Read_{port.port_name}'

        if data_type.passed_by() == 'value':
            function = port.declare_function(fn_name, data_type.name)
        else:
            function = port.declare_function(fn_name, 'void', {
                'value': {'direction': 'out', 'data_type': data_type}
            })

        return {'read': function}

    def create_component_functions(self, port):
        prototype = port.functions['read']
        data_type = self._types.get(port['data_type'])

        function = FunctionImplementation(prototype)
        function.attributes.add('weak')

        default_value = data_type.render_value(port['default_value'])
        if data_type.passed_by() == 'value':
            function.set_return_statement(default_value)
        else:
            function.add_input_assert('value != NULL')
            function.mark_argument_used('value')
            function.add_body('*value = {};'.format(default_value))

        return {'read': function}

    def create_runtime_functions(self, port):
        prototype = port.functions['read']
        data_type = self._types.get(port['data_type'])

        function = FunctionImplementation(prototype)
        if data_type.passed_by() == 'pointer':
            function.add_input_assert('value != NULL')

        return {'read': function}


class ReadQueuedValuePortType(PortType):
    def __init__(self, types):
        super().__init__(types, {
            'order': 3,
            'consumes': {'queue': 'single'},
            'def_attributes': {
                'required': ['data_type'],
                'optional': {'default_value': None},
                'static': {}
            }
        })

    def declare_functions(self, port):
        data_type = self._types.get(port['data_type'])

        fn_name = f'{port.component_name}_Read_{port.port_name}'

        function = port.declare_function(fn_name, 'QueueStatus_t', {
            'value': {'direction': 'out', 'data_type': data_type}
        })

        return {'read': function}

    def create_component_functions(self, port):
        prototype = port.functions['read']

        queue_status_type = self._types.get('QueueStatus_t')

        function = FunctionImplementation(prototype)
        function.attributes.add('weak')
        function.add_input_assert('value != NULL')
        function.mark_argument_used('value')

        function.set_return_statement(queue_status_type.render_value(None))

        return {'read': function}

    def create_runtime_functions(self, port):
        prototype = port.functions['read']

        function = FunctionImplementation(prototype)
        function.add_input_assert('value != NULL')
        function.mark_argument_used('value')

        return {'read': function}


class ReadIndexedValuePortType(PortType):
    def __init__(self, types):
        super().__init__(types, {
            'order': 3,
            'consumes': {
                'array': 'multiple',
                'constant_array': 'multiple'
            },
            'def_attributes': {
                'required': ['data_type', 'count'],
                'optional': {'default_value': None},
                'static': {}
            }
        })

    def declare_functions(self, port):
        data_type = self._types.get(port['data_type'])

        fn_name = f'{port.component_name}_Read_{port.port_name}'

        if data_type.passed_by() == 'value':
            function = port.declare_function(fn_name, data_type.name, {
                'index': {'direction': 'in', 'data_type': self._types.get('uint32_t')}
            })
        else:
            function = port.declare_function(fn_name, 'void', {
                'index': {'direction': 'in', 'data_type': self._types.get('uint32_t')},
                'value': {'direction': 'out', 'data_type': data_type}
            })

        return {'read': function}

    def create_component_functions(self, port):
        prototype = port.functions['read']
        data_type = self._types.get(port['data_type'])

        function = FunctionImplementation(prototype)
        function.attributes.add('weak')
        function.add_input_assert(f'index < {port["count"]}')
        function.mark_argument_used('index')

        default_value = data_type.render_value(port['default_value'])
        if data_type.passed_by() == 'value':
            function.set_return_statement(default_value)
        else:
            function.add_input_assert('value != NULL')
            function.mark_argument_used('value')
            function.add_body(f'*value = {default_value};')

        return {'read': function}

    def create_runtime_functions(self, port):
        prototype = port.functions['read']
        data_type = self._types.get(port['data_type'])

        function = FunctionImplementation(prototype)
        function.add_input_assert(f'index < {port["count"]}')
        function.mark_argument_used('index')

        if data_type.passed_by() == 'pointer':
            function.add_input_assert('value != NULL')
            function.mark_argument_used('value')

        return {'read': function}


class WriteDataPortType(PortType):
    def __init__(self, types):
        super().__init__(types, {
            'order': 2,
            'provides': {'variable', 'queue'},
            'def_attributes': {
                'required': ['data_type'],
                'optional': {},
                'static': {}
            }
        })

    def declare_functions(self, port):
        data_type = self._types.get(port['data_type'])

        fn_name = f'{port.component_name}_Write_{port.port_name}'

        function = port.declare_function(fn_name, 'void', {
            'value': {'direction': 'in', 'data_type': data_type}
        })

        return {'write': function}

    def create_component_functions(self, port):
        prototype = port.functions['write']
        data_type = self._types.get(port['data_type'])

        function = FunctionImplementation(prototype)
        function.attributes.add('weak')

        if data_type.passed_by() == 'pointer':
            function.add_input_assert('value != NULL')
            function.mark_argument_used('value')

        return {'write': function}

    def create_runtime_functions(self, port):
        prototype = port.functions['write']
        data_type = self._types.get(port['data_type'])

        function = FunctionImplementation(prototype)

        if data_type.passed_by() == 'pointer':
            function.add_input_assert('value != NULL')
            function.mark_argument_used('value')

        return {'write': function}


class WriteIndexedDataPortType(PortType):
    def __init__(self, types):
        super().__init__(types, {
            'order': 2,
            'provides': {'array'},
            'def_attributes': {
                'required': ['data_type', 'count'],
                'optional': {},
                'static': {}
            }
        })

    def declare_functions(self, port):
        data_type = self._types.get(port['data_type'])

        fn_name = f'{port.component_name}_Write_{port.port_name}'

        function = port.declare_function(fn_name, 'void', {
            'index': {'direction': 'in', 'data_type': self._types.get('uint32_t')},
            'value': {'direction': 'in', 'data_type': data_type}
        })

        return {'write': function}

    def create_component_functions(self, port):
        prototype = port.functions['write']
        data_type = self._types.get(port['data_type'])

        function = FunctionImplementation(prototype)
        function.attributes.add('weak')
        function.add_input_assert(f'index < {port["count"]}')
        function.mark_argument_used('index')

        if data_type.passed_by() == 'pointer':
            function.add_input_assert('value != NULL')
            function.mark_argument_used('value')

        return {'write': function}

    def create_runtime_functions(self, port):
        prototype = port.functions['write']
        data_type = self._types.get(port['data_type'])

        function = FunctionImplementation(prototype)
        function.add_input_assert(f'index < {port["count"]}')
        function.mark_argument_used('index')

        if data_type.passed_by() == 'pointer':
            function.add_input_assert('value != NULL')
            function.mark_argument_used('value')

        return {'write': function}


class ConstantPortType(PortType):
    def __init__(self, types):
        super().__init__(types, {
            'order': 1,
            'provides': {'constant'},
            'def_attributes': {
                'required': ['data_type', 'value'],
                'optional': {},
                'static': {}
            }
        })

    def declare_functions(self, port):
        data_type = self._types.get(port['data_type'])

        fn_name = f'{port.component_name}_Constant_{port.port_name}'

        if data_type.passed_by() == 'value':
            function = port.declare_function(fn_name, data_type.name)
        else:
            function = port.declare_function(fn_name, 'void', {
                'value': {'direction': 'out', 'data_type': data_type}
            })

        return {'constant': function}

    def create_component_functions(self, port):
        prototype = port.functions['constant']
        data_type = self._types.get(port['data_type'])

        function = FunctionImplementation(prototype)

        constant_value = data_type.render_value(port['value'])
        if data_type.passed_by() == 'value':
            function.set_return_statement(constant_value)
        else:
            function.add_input_assert('value != NULL')
            function.mark_argument_used('value')
            function.add_body(f'*value = {constant_value};')

        return {'constant': function}

    def create_runtime_functions(self, port):
        return {}


class ConstantArrayPortType(PortType):
    def __init__(self, types):
        super().__init__(types, {
            'order': 1,
            'provides': {'constant_array'},
            'def_attributes': {
                'required': ['data_type', 'value', 'count'],
                'optional': {},
                'static': {}
            }
        })

    def declare_functions(self, port):
        data_type = self._types.get(port['data_type'])

        fn_name = f'{port.component_name}_Constant_{port.port_name}'

        if data_type.passed_by() == 'value':
            function = port.declare_function(fn_name, data_type.name, {
                'index': {'direction': 'in', 'data_type': self._types.get('uint32_t')}
            })
        else:
            function = port.declare_function(fn_name, 'void', {
                'index': {'direction': 'in', 'data_type': self._types.get('uint32_t')},
                'value': {'direction': 'out', 'data_type': data_type}
            })

        return {'constant': function}

    def create_component_functions(self, port):
        prototype = port.functions['constant']
        data_type = self._types.get(port['data_type'])

        function = FunctionImplementation(prototype)
        function.add_input_assert(f'index < {port["count"]}')
        function.mark_argument_used('index')

        constant_value = ', '.join(map(data_type.render_value, port['value']))
        function.add_body(f'static const {data_type.name} constant[{port["count"]}] = {{ {constant_value} }};')
        if data_type.passed_by() == 'value':
            function.set_return_statement('constant[index]')
        else:
            function.add_input_assert('value != NULL')
            function.mark_argument_used('value')
            function.add_body('*value = constant[index];')

        return {'constant': function}

    def create_runtime_functions(self, port):
        return {}


known_port_types = {
    'ReadValue': ReadValuePortType,
    'ReadIndexedValue': ReadIndexedValuePortType,
    'ReadQueuedValue': ReadQueuedValuePortType,
    'WriteData': WriteDataPortType,
    'WriteIndexedData': WriteIndexedDataPortType,
    'Constant': ConstantPortType,
    'ConstantArray': ConstantArrayPortType
}


def init(owner: CGlue):
    owner.types.add_category(StructType(owner.types))
    owner.types.add_category(EnumType(owner.types))
    owner.types.add_category(UnionType(owner.types))

    owner.add_signal_type('variable', VariableSignal())
    owner.add_signal_type('array', ArraySignal())
    owner.add_signal_type('constant', ConstantSignal())
    owner.add_signal_type('constant_array', ConstantArraySignal())
    owner.add_signal_type('queue', QueueSignal())

    types = owner.types
    types.add(
        'QueueStatus_t',
        types.category('enum').process_type({
            'values': [
                'QueueStatus_Empty',
                'QueueStatus_Ok',
                'QueueStatus_Overflow'
            ],
            'default_value': 'QueueStatus_Empty'
        }),
        "builtin types"
    )

    for port_type_name, port_type_class in known_port_types.items():
        owner.add_port_type(port_type_name, port_type_class(types))


def add_type_def(owner: CGlue, type_name, type_data, defined_by):
    processed_type_data = process_type_def(owner.types, type_name, type_data)
    owner.types.add(type_name, processed_type_data, defined_by)


def process_project_types(owner: CGlue, project_config):
    for type_name, type_data in project_config.get('types', {}).items():
        add_type_def(owner, type_name, type_data, "project file")


def process_component_ports_and_types(owner: CGlue, component: Component):
    print(f"Processing component: {component.name}")

    try:
        for type_name, type_data in component.config['types'].items():
            add_type_def(owner, type_name, type_data, component.name)

        if component.config['multiple_instances']:
            instance_type_name = f'{component.name}_Instance_t'
            instance_type = {
                'fields': component.config['instance_variables'],
                'pass_semantic': 'pointer'
            }
            add_type_def(owner, instance_type_name, instance_type, component.name)
    except Exception:
        print(f"Failed to add type definitions for {component.name}")
        raise


def sort_functions(owner: CGlue, context):
    def sort_by_name(fn):
        # only sort functions of known port types
        if type(context) is dict:
            port = owner.get_port(fn)
        else:
            try:
                port = context.get_port(fn)
            except KeyError:
                port = owner.get_port(fn)
        if port['port_type'] in known_port_types:
            return fn
        else:
            return '0'

    def sort_by_port_type(fn):
        if type(context) is dict:
            port = owner.get_port(fn)
        else:
            try:
                port = context.get_port(fn)
            except KeyError:
                port = owner.get_port(fn)
        return port.port_type.config.get('order', 0)

    by_name = sorted(context['functions'], key=sort_by_name)
    by_port_type = sorted(by_name, key=sort_by_port_type)
    context['functions'] = {fn: context['functions'][fn] for fn in by_port_type}


def cleanup_component(owner: CGlue, _, ctx):
    sort_functions(owner, ctx)


def builtin_data_types():
    return Plugin("BuiltinDataTypes", {
        'init': init,
        'load_project_config': process_project_types,
        'load_component_config': process_component_ports_and_types,
        'before_generating_component': cleanup_component,
        'before_generating_runtime': sort_functions
    })
