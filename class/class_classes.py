import struct

class FileInterface():
    def __init__(self, contents):
        self.contents = contents

    def read(self, off, size):
        return self.contents[off:off+size]

    def __len__(self):
        return len(self.contents)

class ClassError(Exception):
    pass

class File():
    # ClassFile {
    #     u4             magic;
    #     u2             minor_version;
    #     u2             major_version;
    #     u2             constant_pool_count;
    #     cp_info        constant_pool[constant_pool_count-1];
    #     u2             access_flags;
    #     u2             this_class;
    #     u2             super_class;
    #     u2             interfaces_count;
    #     u2             interfaces[interfaces_count];
    #     u2             fields_count;
    #     field_info     fields[fields_count];
    #     u2             methods_count;
    #     method_info    methods[methods_count];
    #     u2             attributes_count;
    #     attribute_info attributes[attributes_count];
    # }

    def __init__(self, file_interface=None):
        self.magic = ''
        self.minor = 0
        self.major = 0
        self.constant_pool_count = 0
        self.constant_pool = [None]
        self.interfaces_count = 0
        self.interfaces = []
        self.fields_count = 0
        self.fields = []
        self.methods_count = 0
        self.methods = []
        self.attributes_count = 0
        self.attributes = []

        if not file_interface:
            return

        self.raw = file_interface

        self.parse()

    def parse(self):
        off = 0
        self.magic = self.raw.read(off, 4)
        if self.magic != b'\xCA\xFE\xBA\xBE':
            raise ClassError('incorrect magic bytes or version')
        off += 4

        self.minor = U2(off, self.raw)
        off = self.minor.end
        self.major = U2(off, self.raw)
        off = self.major.end

        #TODO: check major version is supported 

        self.constant_pool_count = U2(off, self.raw)
        off = self.constant_pool_count.end

        skip_next = False
        for idx in range(1, self.constant_pool_count.value):
            if skip_next:
                # TODO: create class for 2nd field of longs and dubs
                self.constant_pool.append(None)
                skip_next = False
                continue
            cp_info = ConstantPoolInfo(off, self.raw)
            off = cp_info.end
            self.constant_pool.append(cp_info)
            if cp_info.tag.value in [5, 6]:
                skip_next = True

        self.access_flags = AccessFlags(off, self.raw)
        off = self.access_flags.end

        self.this_class = U2(off, self.raw)
        off = self.this_class.end

        self.super_class = U2(off, self.raw)
        off = self.super_class.end

        self.interfaces_count = U2(off, self.raw)
        off = self.interfaces_count.end
        for idx in range(0, self.interfaces_count.value):
            interface = U2(off, self.raw)
            # TODO: check in bounds
            self.interfaces.append(interface)
            off = interface.end

        self.fields_count = U2(off, self.raw)
        off = self.fields_count.end
        for idx in range(0, self.fields_count.value):
            field_info = FieldInfo(off, self.raw, self.constant_pool)
            # TODO: check in bounds
            self.fields.append(field_info)
            off = field_info.end

        self.methods_count = U2(off, self.raw)
        off = self.methods_count.end
        for idx in range(0, self.methods_count.value):
            method_info = MethodInfo(off, self.raw, self.constant_pool)
            self.methods.append(method_info)
            off = method_info.end


    def pretty_print(self, indent=0):
        print(' '*indent, end='')
        print('Magic: {}'.format(self.magic.hex()))

        print(' '*indent, end='')
        print('Minor: {}'.format(self.minor))
        print(' '*indent, end='')
        print('Major: {}'.format(self.major))

        print(' '*indent, end='')
        print('Constant Pool Count: {}'.format(self.constant_pool_count))
        idx = 0
        for cp_info in self.constant_pool:
            print(' '*indent, end='')
            print('Consant Pool[{}]:'.format(idx))
            if not cp_info:
                print(' '*indent, end='')
                print('INVALID INDEX')
            else:
                cp_info.pretty_print(indent+2)
            idx += 1
        
        print(' '*indent, end='')
        print('Access Flags:')
        self.access_flags.pretty_print(indent+2)

        print(' '*indent, end='')
        print('This Class Index: {}'.format(self.this_class))
        this_class_info = self.constant_pool[self.this_class.value]
        if this_class_info.tag.value != 7:
            raise ClassError('invalid tag for this_class_info')
        print(' '*(indent+2), end='')
        print('Class Info: ')
        this_class_info.pretty_print(indent+4)
        this_class_name = self.constant_pool[this_class_info.name_index.value]
        if this_class_name.tag.value != 1:
            raise ClassError('invalid tag for this_class_name')
        print(' '*(indent+2), end='')
        print('Name: ')
        this_class_name.pretty_print(indent+4)

        print(' '*indent, end='')
        print('Super Class Index: {}'.format(self.super_class))
        if self.super_class.value != 0:
            super_class_info = self.constant_pool[self.super_class.value]
            if super_class_info.tag.value != 7:
                raise ClassError('invalid tag for super_class_info')
            print(' '*(indent+2), end='')
            print('Class Info: ')
            super_class_info.pretty_print(indent+4)
            super_class_name = self.constant_pool[super_class_info.name_index.value]
            if super_class_name.tag.value != 1:
                raise ClassError('invalid tag for super_class_name')
            print(' '*(indent+2), end='')
            print('Name: ')
            super_class_name.pretty_print(indent+4)

        print(' '*indent, end='')
        print('Interfaces Count: {}'.format(self.interfaces_count))
        idx = 0
        for interface in self.interfaces:
            print(' '*indent, end='')
            print('Interfaces[{}]: {}'.format(idx, interface))
            idx += 1

class Template:
    def __init__(self, start=0, file_interface=None):
        self.start = start

        if file_interface:
            Template_CHANGEME.__parse__(self, start, file_interface)

    def __parse__(self, start, file_interface):
        off = start

    def pretty_print(self, indent=0):
        print(' '*indent, end='')

class MethodInfo:
    def __init__(self, start=0, file_interface=None, constant_pool=None):
        self.start = start
        self.access_flags = 0
        self.name_index = 0
        self.descriptor_index = 0
        self.attributes_count = 0
        self.attributes = []

        if file_interface:
            MethodInfo.__parse__(self, start, file_interface, constant_pool)

    def __parse__(self, start, file_interface, constant_pool=None):
        off = start
        self.access_flags = AccessFlags(off, file_interface, method=True)
        off = self.access_flags.end
        self.name_index = U2(off, file_interface)
        off = self.name_index.end
        self.descriptor_index = U2(off, file_interface)
        off = self.descriptor_index.end
        self.attributes_count = U2(off, file_interface)
        off = self.attributes_count.end
        for idx in range(self.attributes_count.value):
            attribute_info = AttributeInfo(off, file_interface)
            attribute_info = AttributeInfo.upgrade(attribute_info, file_interface, constant_pool)
            self.attributes.append(attribute_info)
            off = attribute_info.end
        self.end = off

    def pretty_print(self, indent=0):
        print(' '*indent, end='')


class VerificationTypeInfo:
    tag_names = {
        0: 'ITEM_Top',
        1: 'ITEM_Integer',
        2: 'ITEM_Float',
        3: 'ITEM_Double',
        4: 'ITEM_Long',
        5: 'ITEM_Null',
        6: 'ITEM_UninitializedThis',
        7: 'ITEM_Object',
        8: 'ITEM_Uninitialized',
    }
    def __init__(self, start=0, file_interface=None):
        self.start = start
        if file_interface:
            VerificationTypeInfo.__parse__(self, start, file_interface)

    def __parse__(self, start, file_interface):
        off = self.start
        self.tag = U1(off, file_interface)
        off = self.tag.end
        self.tag_name = self.tag_names[self.tag.value]
        if self.tag.value == 7:
            self.cpool_index = U2(off, file_interface)
            off = self.cpool_index.end
        if self.tag.value == 8:
            self.offset = U2(off, file_interface)
            off = self.offset.end
        self.end = off

class AttributeInfo:
    def __init__(self, start=0, file_interface=None):
        self.start = start
        self.attribute_name_index = 0
        self.attribute_length = 0
        self.info = b''

        if file_interface:
            AttributeInfo.__parse__(self, start, file_interface)

    def __parse__(self, start, file_interface):
        off = start
        self.attribute_name_index = U2(off, file_interface)
        off = self.attribute_name_index.end
        self.attribute_length = U4(off, file_interface)
        off = self.attribute_length.end
        self.info = file_interface.read(off, self.attribute_length.value)
        off += self.attribute_length.value
        self.end = off

    @staticmethod
    def upgrade(attribute_info, file_interface, constant_pool):
        cpi = constant_pool[attribute_info.attribute_name_index.value]
        if cpi.tag.value != 1:
            raise ClassError('invalid name tag')

        name = cpi.bytes
        print('name', name)
        start = attribute_info.start
        if name == b'ConstantValue':
            return ConstantValueAttribute(start, file_interface)
        elif name == b'Code':
            return CodeAttribute(start, file_interface, constant_pool)
        elif name == b'StackMapTable':
            return StackMapTable(start, file_interface)
        # elif name == b'Exceptions':
        #     pass
        # elif name == b'InnerClasses':
        #     pass
        # elif name == b'EnclosingMethod':
        #     pass
        # elif name == b'Synthetic':
        #     pass
        # elif name == b'Signature':
        #     pass
        # elif name == b'SourceFile':
        #     pass
        # elif name == b'SourceDebugExtension':
        #     pass
        # elif name == b'LineNumberTable':
        #     pass
        # elif name == b'LocalVariableTable':
        #     pass
        # elif name == b'LocalVariableTypeTable':
        #     pass
        # elif name == b'Deprecated':
        #     pass
        # elif name == b'RuntimeVisibleAnnotations':
        #     pass
        # elif name == b'RuntimeInvisibleAnnotations':
        #     pass
        # elif name == b'RuntimeVisibleParameterAnnotations':
        #     pass
        # elif name == b'RuntimeInvisibleParameterAnnotations':
        #     pass
        # elif name == b'AnnotationDefault':
        #     pass
        # elif name == b'BootstrapMethods':
        #     pass
        else:
            raise ClassError('unsupported attribute: {}'.format(name))
        return attribute_info

    def pretty_print(self, indent=0):
        print(' '*indent, end='')

class StackMapFrame:
    def __init__(self, start=0, file_interface=None):
        self.start = start
        if file_interface:
            StackMapFrame.__parse__(self, start, file_interface)

    def __parse__(self, start, file_interface):
        off = self.start
        self.frame_type = U1(start, file_interface)
        off = self.frame_type.end
        ft = self.frame_type.value
        if ft <= 63 and ft >= 0 :
            self.frame_type_str = 'SAME'
        elif ft <= 127 and ft >= 64:
            self.frame_type_str = 'SAME_LOCALS_1_STACK_ITEM'
            self.stack = [VerificationTypeInfo(off, file_interface)]
            off = self.stack[0].end
        elif ft == 247:
            self.frame_type_str = 'SAME_LOCALS_1_STACK_ITEM_EXTENDED'
            self.offset_delta = U2(off, file_interface)
            off = self.offset_delta.end
            self.stack = [VerificationTypeInfo(off, file_interface)]
            off = self.stack[0].end
        elif ft <= 250 and ft >= 248:
            self.frame_type_str = 'CHOP'
            self.offset_delta = U2(off, file_interface)
            off = self.offset_delta.end
        elif ft == 251:
            self.frame_type_str = 'SAME_FRAME_EXTENDED'
            self.offset_delta = U2(off, file_interface)
            off = self.offset_delta.end
        elif ft <= 254 and ft >= 252:
            self.frame_type_str = 'APPEND'
            self.offset_delta = U2(off, file_interface)
            off = self.offset_delta.end
            self.locals = []
            for idx in range(ft-251):
                vti = VerificationTypeInfo(off, file_interface)
                self.locals.append(vti)
                off = vti.end
        elif ft == 255:
            self.frame_type_str = 'FULL_FRAME'
            self.offset_delta = U2(off, file_interface)
            off = self.offset_delta.end
            self.number_of_locals = U2(off, file_interface)
            off = self.number_of_locals.end
            self.locals = []
            for idx in range(self.number_of_locals.value):
                vti = VerificationTypeInfo(off, file_interface)
                self.locals.append(vti)
                off = vti.end
            self.number_of_stack_items = U2(off, file_interface)
            off = self.number_of_stack_items.end
            self.stack = []
            for idx in range(self.number_of_stack_items.value):
                vti = VerificationTypeInfo(off, file_interface)
                self.stack.append(vti)
                off = vti.end
        else:
            raise ClassError('invalid frame type {}'.format(ft))
        self.end = off

class StackMapTable(AttributeInfo):
    def __init__(self, start=0, file_interface=None):
        AttributeInfo.__init__(self, start, file_interface)
        self.number_of_entries = 0
        self.entries = []
        if file_interface:
            StackMapTable.__parse__(self, start, file_interface)

    def __parse__(self, start, file_interface):
        off = self.attribute_length.end
        self.number_of_entries = U2(off, file_interface)
        off = self.number_of_entries.end
        for idx in range(self.number_of_entries.value):
            entry = StackMapFrame(off, file_interface)
            self.entries.append(entry)
            off = entry.end


class ConstantValueAttribute(AttributeInfo):
    def __init__(self, start=0, file_interface=None):
        AttributeInfo.__init__(self, start, file_interface)
        if file_interface:
            ConstantValueAttribute.__parse__(self, start, file_interface)

    def __parse__(self, start, file_interface):
        off = self.attribute_length.end
        self.constantvalue_index = U2(off, file_interface)

class ExceptionTableEntry:
    def __init__(self, start=0, file_interface=None):
        if file_interface:
            ExceptionTableEntry.__parse__(self, start, file_interface)

    def __parse__(self, start, file_interface):
        off = start
        self.start_pc = U2(off, file_interface)    
        off = self.start_pc.end
        self.end_pc = U2(off, file_interface)    
        off = self.end_pc.end
        self.handler_pc = U2(off, file_interface)    
        off = self.handler_pc.end
        self.catch_type = U2(off, file_interface)    
        off = self.catch_type.end
        self.end = off

class CodeAttribute(AttributeInfo):
    def __init__(self, start=0, file_interface=None, constant_pool=None):
        AttributeInfo.__init__(self, start, file_interface)
        if file_interface:
            CodeAttribute.__parse__(self, start, file_interface, constant_pool)

    def __parse__(self, start, file_interface, constant_pool=None):
        off = self.attribute_length.end
        self.max_stack = U2(off, file_interface)
        off = self.max_stack.end
        self.max_locals = U2(off, file_interface)
        off = self.max_locals.end
        self.code_length = U4(off, file_interface)
        off = self.code_length.end
        self.code = file_interface.read(off, self.code_length.value)
        off += self.code_length.value
        self.exception_table_length = U2(off, file_interface)
        off = self.exception_table_length.end
        print('ete len', self.exception_table_length)
        self.exception_table = []
        for idx in range(self.exception_table_length.value):
            exception_table_entry = ExceptionTableEntry(off, file_interface)
            self.exception_table.append(exception_table_entry)
            off = exception_table_entry.end
        self.attributes_count = U2(off, file_interface)
        off = self.attributes_count.end
        self.attributes = []
        for idx in range(self.attributes_count.value):
            attribute_info = AttributeInfo(off, file_interface)
            attribute_info = AttributeInfo.upgrade(attribute_info, file_interface, constant_pool)
            self.attributes.append(attribute_info)
            off = attribute_info.end
        self.end = off

class FieldInfo:
    def __init__(self, start=0, file_interface=None, constant_pool=None):
        self.start = start
        self.access_flags = None
        self.name_index = 0
        self.descriptor_index = 0
        self.attributes_count = 0
        self.attributes = []

        if file_interface:
            FieldInfo.__parse__(self, start, file_interface, constant_pool)

    def __parse__(self, start, file_interface, constant_pool=None):
        off = start
        self.access_flags = AccessFlags(off, file_interface)
        off = self.access_flags.end
        self.name_index = U2(off, file_interface)
        off = self.name_index.end
        self.descriptor_index = U2(off, file_interface)
        off = self.descriptor_index.end
        self.attributes_count = U2(off, file_interface)
        off = self.attributes_count.end
        for idx in range(self.attributes_count.value):
            attribute_info = AttributeInfo(off, file_interface)
            attribute_info = AttributeInfo.upgrade(
                attribute_info, file_interface, constant_pool)
            self.attributes.append(attribute_info)
            off = attribute_info.end
        self.end = off

    def pretty_print(self, indent=0):
        print(' '*indent, end='')

class AccessFlags:
    method_flag_lookup = {
        0x0020: 'ACC_SYNCHRONIZED',
        0x0040: 'ACC_BRIDGE',
        0x0080: 'ACC_VARARGS',
        0x0100: 'ACC_NATIVE',
        0x0800: 'ACC_STRICT',
    }

    flag_lookup = {
        0x0001: 'ACC_PUBLIC',
        0x0002: 'ACC_PRIVATE',
        0x0004: 'ACC_PROTECTED',
        0x0008: 'ACC_STATIC',
        0x0010: 'ACC_FINAL',
        0x0020: 'ACC_SUPER',
        0x0040: 'ACC_VOLATILE',
        0x0080: 'ACC_TRANSIENT',
        0x0200: 'ACC_INTERFACE',
        0x0400: 'ACC_ABSTRACT',
        0x1000: 'ACC_SYNTHETIC',
        0x2000: 'ACC_ANNOTATION',
        0x4000: 'ACC_ENUM',
    }

    def __init__(self, start=0, file_interface=None, method=False):
        self.start = start
        self.value = 0
        self.flags = []

        if method:
            for flag in self.method_flag_lookup:
                self.flag_lookup[flag] = self.method_flag_lookup[flag]

        if file_interface:
            AccessFlags.__parse__(self, start, file_interface)

    def __parse__(self, start, file_interface):
        off = start
        self.value = U2(off, file_interface)
        off = self.value.end
        for flag in self.flag_lookup:
            if self.value.value & flag:
                self.flags.append(self.flag_lookup[flag])
        self.end = self.value.end

    def pretty_print(self, indent=0):
        for flag in self.flags:
            print(' '*indent, end='')
            print(flag)


class ConstantPoolInfo:
    tag_name_lookup = {
        1: 'CONSTANT_Utf8',
        3: 'CONSTANT_Integer',
        7: 'CONSTANT_Class',
        # 4: 'CONSTANT_Float',
        5: 'CONSTANT_Long',
        # 6: 'CONSTANT_Double',
        8: 'CONSTANT_String',
        9: 'CONSTANT_Fieldref',
        10: 'CONSTANT_Methodref',
        11: 'CONSTANT_InterfaceMethodref',
        12: 'CONSTANT_NameAndType',
        # 15: 'CONSTANT_MethodHandle',
        # 16: 'CONSTANT_MethodType',
        # 18: 'CONSTANT_InvokeDynamic',
    }

    def __init__(self, start=0, file_interface=None):
        self.start = start

        if file_interface:
            ConstantPoolInfo.__parse__(self, start, file_interface)

    def __parse__(self, start, file_interface):
        off = start
        self.tag = U1(off, file_interface)
        off = self.tag.end
        if self.tag.value == 1:
            self.length = U2(off, file_interface)
            off = self.length.end
            self.bytes = file_interface.read(off, self.length.value)
            off += self.length.value
        elif self.tag.value == 3:
            self.bytes = U4(off, file_interface)
            off = self.bytes.end
        elif self.tag.value == 5:
            self.high_bytes = U4(off, file_interface)
            off = self.high_bytes.end
            self.low_bytes = U4(off, file_interface)
            off = self.low_bytes.end
            self.value = self.high_bytes.value << 32 + self.low_bytes.value
        elif self.tag.value == 7:
            self.name_index = U2(off, file_interface)
            off = self.name_index.end
        elif self.tag.value == 8:
            self.string_index = U2(off, file_interface)
            off = self.string_index.end
        elif self.tag.value in [9, 10, 11]:
            self.class_index = U2(off, file_interface)
            off = self.class_index.end
            self.name_and_type_index = U2(off, file_interface)
            off = self.name_and_type_index.end
        elif self.tag.value == 12:
            self.name_index = U2(off, file_interface)
            off = self.name_index.end
            self.descriptor_index = U2(off, file_interface)
            off = self.descriptor_index.end
        else:
            raise ClassError('invalid tag number: {}'.format(self.tag))

        self.end = off

    def pretty_print(self, indent=0):
        print(' '*indent, end='')
        print('Tag: {} ({})'.format(
            self.tag_name_lookup[self.tag.value], self.tag.value))

        if self.tag.value == 1:
            print(' '*indent, end='')
            print('Length: {}'.format(self.length.value))
            print(' '*indent, end='')
            print('Bytes: {}'.format(self.bytes))
        elif self.tag.value == 3:
            print(' '*indent, end='')
            print('Bytes: {}'.format(self.bytes))
        elif self.tag.value == 5:
            print(' '*indent, end='')
            print('High Bytes: {}'.format(self.high_bytes))
            print(' '*indent, end='')
            print('Low Bytes: {}'.format(self.low_bytes))
            print(' '*indent, end='')
            print('Value: {}'.format(self.value))
        elif self.tag.value == 7:
            print(' '*indent, end='')
            print('Name Index: {}'.format(self.name_index))
        elif self.tag.value == 8:
            print(' '*indent, end='')
            print('String Index: {}'.format(self.string_index))
        elif self.tag.value in [9, 10, 11]:
            print(' '*indent, end='')
            print('Class Index: {}'.format(self.class_index))
            print(' '*indent, end='')
            print('Name and Type Index: {}'.format(self.name_and_type_index))
        elif self.tag.value == 12:
            print(' '*indent, end='')
            print('Name Index: {}'.format(self.name_index))
            print(' '*indent, end='')
            print('Descriptor Index: {}'.format(self.descriptor_index))

class U1:
    def __init__(self, start=0, file_interface=None):
        self.start = start
        self.value = 0

        if file_interface:
            U1.__parse__(self, start, file_interface)

    def __parse__(self, start, file_interface):
        self.value = struct.unpack(
            '>B', file_interface.read(self.start, 1))[0]
        self.end = self.start + 1

    def __repr__(self):
        return 'U1(%d)' % self.value

    def pretty_print(self, indent=0):
        print(' '*indent, end='')
        print('{}'.format(self))

class U2:
    def __init__(self, start=0, file_interface=None):
        self.start = start
        self.value = 0

        if file_interface:
            U2.__parse__(self, start, file_interface)

    def __parse__(self, start, file_interface):
        self.value = struct.unpack(
            '>H', file_interface.read(self.start, 2))[0]
        self.end = self.start + 2

    def __repr__(self):
        return 'U2(%d)' % self.value

    def pretty_print(self, indent=0):
        print(' '*indent, end='')
        print('{}'.format(self))

class U4:
    def __init__(self, start=0, file_interface=None):
        self.start = start
        self.value = 0

        if file_interface:
            U4.__parse__(self, start, file_interface)

    def __parse__(self, start, file_interface):
        self.value = struct.unpack(
            '>I', file_interface.read(self.start, 4))[0]
        self.end = self.start + 4

    def __repr__(self):
        return 'U4(%d)' % self.value

    def pretty_print(self, indent=0):
        print(' '*indent, end='')
        print('{}'.format(self))


