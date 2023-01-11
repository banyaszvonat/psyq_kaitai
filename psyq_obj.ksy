meta:
  id: psyq_obj
  file-extension: obj
  endian: le
  encoding: ascii
doc: |
  Created by reverse engineering .LIB and .OBJ files compiled with PSYLINK,
  and inspecting the strings of DUMPOBJ.EXE. The output of DUMPOBJ.EXE
  was used as the canonical parse.

  There are a few things still missing:
  - Patch types (It's unclear what the numbers stand for)
  - In the patch instruction, there's two unknown bytes,
    which are 0x00 0x04 when specifying sectionbase() and a section number. This
    is probably some sort of enum.
  - The 'tags' enum should document all the known tags, but not all of them
    have a type associated to it
seq:
  - id: link_magic
    contents: LNK
  - id: version
    type: u1
  - id: sections
    type: tagvalue

    repeat: eos

types:
  tagvalue:
    seq:
      - id: tag
        type: u1
        enum: tags
      - id: value
        type:
          switch-on: tag
          cases:
            'tags::processor_type': processor_type
            'tags::section_symbol': section_symbol
            'tags::xdef': xdef
            'tags::xref': xref
            #'tags::code': code
            #'tags::section_switch': section_switch
            'tags::section_switch': codesection
            'tags::xbss_symbol': xbss_symbol
            'tags::patch': patch
            'tags::uninitialized': uninitialized
  counted_str:
    seq:
      - id: len
        type: u1
      - id: str
        type: str
        size: len
  processor_type:
    seq:
      - id: value
        type: u1
  section_symbol:
    seq:
      - id: number
        type: u2
      - id: group
        type: u2
      - id: alignment
        type: u1
      - id: name
        type: counted_str
  xdef:
    seq:
      - id: number
        type: u2
      - id: section
        type: u2
      - id: offset
        type: u4
      - id: sym
        type: counted_str
  xref:
    seq:
      - id: number
        type: u2
      - id: sym
        type: counted_str
  section_switch:
    seq:
      - id: next_sec
        type: u2
  code_with_padding:
    seq:
      - id: code
        size: _parent.len
      - id: padding
        size-eos: true
  code:
    seq:
      - id: len
        type: u2
      - id: code
        type: code_with_padding
        size: len + len % 4
  xbss_symbol:
    seq:
      - id: number
        type: u2
      - id: section
        type: u2
      - id: size
        type: u4
      - id: name
        type: counted_str
  patch_indexed:
    seq:
      - id: offset
        type: u2
  patch_base_offset:
    seq:
      - id: with1
        type: u2be
      - id: with2
        type: u2be
      - id: unk
        size: 2
        doc: Some sort of enum? 0,4 when sectbase is used
      - id: sectbase
        type: u2
    instances:
      final_with:
        value: with1+with2
        doc: In the inspected samples, only addition was used, but maybe\
              unk can specify another operation.
  patch_section_only:
    seq:
      - id: sectbase
        type: u2
  patch:
    seq:
      - id: type
        type: u1
      - id: offset
        type: u2
      - id: addr_type
        type: u1
      - id: offsets
        type:
          switch-on: addr_type
          cases:
            2: patch_indexed
            4: patch_section_only
            44: patch_base_offset
  uninitialized:
    seq:
      - id: len
        type: u4
  codesection:
    seq:
      - id: section_switch_segment
        type: section_switch
      - id: code_tag
        type: u1
        enum: tags
      - id: code_segment
        type: code

enums:
# Based on messages extracted from DUMPOBJ.EXE
  tags:
    0x00: 'eof'
    0x02: 'code'
    0x04: 'run_at'
    0x06: 'section_switch'
    0x08: 'uninitialized'
    0x0A: 'patch'
    0x0C: 'xdef'
    0x0E: 'xref'
    0x10: 'section_symbol'
    0x12: 'local_symbol'
    0x14: 'group_symbol'
    0x16: 'set_byte_size'
    0x18: 'set_word_size'
    0x1A: 'set_long_size'
    0x1C: 'define_filenum'
    0x1E: 'set_file_line'
    0x20: 'set_line'
    0x22: 'increment_line'
    0x24: 'increment_line_by'
    0x26: 'increment_line_by_alt'
    0x28: 'very_local_symbol'
    0x2A: 'set_3_byte_size_reg'
    0x2C: 'set_mx_info_at'
    0x2E: 'processor_type'
    0x30: 'xbss_symbol'
    0x32: 'inc_sld_linenum_at'
    0x34: 'inc_sld_linenum_by_byte_at'
    0x36: 'inc_sld_linenum_by_word_at'
    0x38: 'set_sld_linenum_to_at'
    0x3A: 'set_sld_linenum_to_at_in_file'
    0x3C: 'end_sld_info'
    0x3E: 'repeat_byte'
    0x40: 'repeat_word'
    0x42: 'repeat_longword'
    0x44: 'proc_call'

