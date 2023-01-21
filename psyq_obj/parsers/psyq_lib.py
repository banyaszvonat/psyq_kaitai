# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from .psyq_obj import PsyqObj


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class PsyqLib(KaitaiStruct):
    """Static libraries emitted by Psy-Q toolkit (presumably.) Basically a container
    for Psy-Q OBJs, basically a header for the file, and an extra header / symbol
    table for each module.
    
    There are 12 unknown bytes before the symbol table, which likely encodes build
    time, and perhaps other things not shown on PSYLINK.EXE's extraction output.
    The format is unknown.
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(3)
        if not self.magic == b"\x4C\x49\x42":
            raise kaitaistruct.ValidationNotEqualError(b"\x4C\x49\x42", self.magic, self._io, u"/seq/0")
        self.unk1 = self._io.read_bytes(1)
        self.modules = []
        i = 0
        while not self._io.is_eof():
            self.modules.append(PsyqLib.Module(self._io, self, self._root))
            i += 1


    class TableEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = PsyqObj.CountedStr(self._io, self, self._root)


    class Table(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.entries = []
            i = 0
            while True:
                _ = PsyqLib.TableEntry(self._io, self, self._root)
                self.entries.append(_)
                if _.name.len == 0:
                    break
                i += 1


    class Module(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (self._io.read_bytes(8)).decode(u"ascii")
            self.unk_hdr = self._io.read_bytes(12)
            self.func_table = PsyqLib.Table(self._io, self, self._root)
            self.lnkheader = self._io.read_bytes(3)
            if not self.lnkheader == b"\x4C\x4E\x4B":
                raise kaitaistruct.ValidationNotEqualError(b"\x4C\x4E\x4B", self.lnkheader, self._io, u"/types/module/seq/3")
            self.version = self._io.read_bytes(1)
            self.tagvalues = []
            i = 0
            while True:
                _ = PsyqObj.Tagvalue(self._io, self, self._root)
                self.tagvalues.append(_)
                if _.tag == PsyqObj.Tags.eof:
                    break
                i += 1



