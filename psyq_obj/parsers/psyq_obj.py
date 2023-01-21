# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class PsyqObj(KaitaiStruct):
    """Created by reverse engineering .LIB and .OBJ files compiled with PSYLINK,
    and inspecting the strings of DUMPOBJ.EXE. The output of DUMPOBJ.EXE
    was used as the canonical parse.
    
    There are a few things still missing:
    - Patch types (It's unclear what the numbers stand for)
    - In the patch instruction, there's two unknown bytes,
      which are 0x00 0x04 when specifying sectionbase() and a section number. This
      is probably some sort of enum.
    - The 'tags' enum should document all the known tags, but not all of them
      have a type associated to it
    """

    class Tags(Enum):
        eof = 0
        code = 2
        run_at = 4
        section_switch = 6
        uninitialized = 8
        patch = 10
        xdef = 12
        xref = 14
        section_symbol = 16
        local_symbol = 18
        group_symbol = 20
        set_byte_size = 22
        set_word_size = 24
        set_long_size = 26
        define_filenum = 28
        set_file_line = 30
        set_line = 32
        increment_line = 34
        increment_line_by = 36
        increment_line_by_alt = 38
        very_local_symbol = 40
        set_3_byte_size_reg = 42
        set_mx_info_at = 44
        processor_type = 46
        xbss_symbol = 48
        inc_sld_linenum_at = 50
        inc_sld_linenum_by_byte_at = 52
        inc_sld_linenum_by_word_at = 54
        set_sld_linenum_to_at = 56
        set_sld_linenum_to_at_in_file = 58
        end_sld_info = 60
        repeat_byte = 62
        repeat_word = 64
        repeat_longword = 66
        proc_call = 68
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.link_magic = self._io.read_bytes(3)
        if not self.link_magic == b"\x4C\x4E\x4B":
            raise kaitaistruct.ValidationNotEqualError(b"\x4C\x4E\x4B", self.link_magic, self._io, u"/seq/0")
        self.version = self._io.read_u1()
        self.sections = []
        i = 0
        while not self._io.is_eof():
            self.sections.append(PsyqObj.Tagvalue(self._io, self, self._root))
            i += 1


    class CountedStr(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len = self._io.read_u1()
            self.str = (self._io.read_bytes(self.len)).decode(u"ascii")


    class PatchBaseOffset(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.with1 = self._io.read_u2be()
            self.with2 = self._io.read_u2be()
            self.unk = self._io.read_bytes(2)
            self.sectbase = self._io.read_u2le()

        @property
        def final_with(self):
            """In the inspected samples, only addition was used, but maybe\ unk can specify another operation."""
            if hasattr(self, '_m_final_with'):
                return self._m_final_with

            self._m_final_with = (self.with1 + self.with2)
            return getattr(self, '_m_final_with', None)


    class ProcessorType(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.value = self._io.read_u1()


    class Uninitialized(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len = self._io.read_u4le()


    class Codesection(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.section_switch_segment = PsyqObj.SectionSwitch(self._io, self, self._root)
            self.code_tag = KaitaiStream.resolve_enum(PsyqObj.Tags, self._io.read_u1())
            self.code_segment = PsyqObj.Code(self._io, self, self._root)


    class Xdef(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.number = self._io.read_u2le()
            self.section = self._io.read_u2le()
            self.offset = self._io.read_u4le()
            self.sym = PsyqObj.CountedStr(self._io, self, self._root)


    class Code(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len = self._io.read_u2le()
            self._raw_code = self._io.read_bytes((self.len + (self.len % 4)))
            _io__raw_code = KaitaiStream(BytesIO(self._raw_code))
            self.code = PsyqObj.CodeWithPadding(_io__raw_code, self, self._root)


    class Xref(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.number = self._io.read_u2le()
            self.sym = PsyqObj.CountedStr(self._io, self, self._root)


    class CodeWithPadding(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.code = self._io.read_bytes(self._parent.len)
            self.padding = self._io.read_bytes_full()


    class SectionSwitch(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.next_sec = self._io.read_u2le()


    class Patch(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._io.read_u1()
            self.offset = self._io.read_u2le()
            self.addr_type = self._io.read_u1()
            _on = self.addr_type
            if _on == 2:
                self.offsets = PsyqObj.PatchIndexed(self._io, self, self._root)
            elif _on == 4:
                self.offsets = PsyqObj.PatchSectionOnly(self._io, self, self._root)
            elif _on == 44:
                self.offsets = PsyqObj.PatchBaseOffset(self._io, self, self._root)


    class XbssSymbol(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.number = self._io.read_u2le()
            self.section = self._io.read_u2le()
            self.size = self._io.read_u4le()
            self.name = PsyqObj.CountedStr(self._io, self, self._root)


    class Tagvalue(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.tag = KaitaiStream.resolve_enum(PsyqObj.Tags, self._io.read_u1())
            _on = self.tag
            if _on == PsyqObj.Tags.processor_type:
                self.value = PsyqObj.ProcessorType(self._io, self, self._root)
            elif _on == PsyqObj.Tags.xref:
                self.value = PsyqObj.Xref(self._io, self, self._root)
            elif _on == PsyqObj.Tags.xbss_symbol:
                self.value = PsyqObj.XbssSymbol(self._io, self, self._root)
            elif _on == PsyqObj.Tags.section_symbol:
                self.value = PsyqObj.SectionSymbol(self._io, self, self._root)
            elif _on == PsyqObj.Tags.uninitialized:
                self.value = PsyqObj.Uninitialized(self._io, self, self._root)
            elif _on == PsyqObj.Tags.section_switch:
                self.value = PsyqObj.SectionSwitch(self._io, self, self._root)
            elif _on == PsyqObj.Tags.code:
                self.value = PsyqObj.Code(self._io, self, self._root)
            elif _on == PsyqObj.Tags.xdef:
                self.value = PsyqObj.Xdef(self._io, self, self._root)
            elif _on == PsyqObj.Tags.patch:
                self.value = PsyqObj.Patch(self._io, self, self._root)


    class PatchSectionOnly(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sectbase = self._io.read_u2le()


    class PatchIndexed(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u2le()


    class SectionSymbol(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.number = self._io.read_u2le()
            self.group = self._io.read_u2le()
            self.alignment = self._io.read_u1()
            self.name = PsyqObj.CountedStr(self._io, self, self._root)



