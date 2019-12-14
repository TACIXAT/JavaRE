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

    def pretty_print(self, indent=0):
        print(' '*indent, end='')
        print('Magic: {}'.format(self.magic.hex()))
        print(' '*indent, end='')
        print('Minor: {}'.format(self.minor))
        print(' '*indent, end='')
        print('Major: {}'.format(self.major))
        print(' '*indent, end='')
        print('Constant Pool Count: {}'.format(self.constant_pool_count))
        print(' '*indent, end='')
        print('Constant Pool Count: {}'.format(len(self.constant_pool)))
        idx = 0
        for cp_info in self.constant_pool:
            if not cp_info:
                print(' '*indent, end='')
                print('INVALID INDEX')
                idx += 1
                continue
            print(' '*indent, end='')
            print('Index: {}'.format(idx))
            cp_info.pretty_print(indent+2)
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


