meta:
  id: psyq_lib
  file-extension: lib
  imports:
    - psyq_obj
  endian: le
  encoding: ascii
doc: |
  Static libraries emitted by Psy-Q toolkit (presumably.) Basically a container
  for Psy-Q OBJs, basically a header for the file, and an extra header / symbol
  table for each module.

  There are 12 unknown bytes before the symbol table, which likely encodes build
  time, and perhaps other things not shown on PSYLINK.EXE's extraction output.
  The format is unknown.
seq:
  - id: magic
    contents: [76, 73, 66]
  - id: unk1
    size: 1
  - id: modules
    type: module
    repeat: eos

types:
  table_entry:
    seq:
      - id: name
        type: psyq_obj::counted_str
  table:
    seq:
      - id: entries
        type: table_entry
        # We pretend the 00 byte as terminator is another counted_str, but stop
        # repeating.
        # I don't know how to implement the zero termination better without
        # being tripped up by leading zero in counted strings (wtf)
        repeat: until
        repeat-until: _.name.len == 0
  module:
    seq:
      - id: name
        size: 8
        type: str
        encoding: ascii
      - id: unk_hdr
        size: 12
      - id: func_table
        type: table
      - id: lnkheader
        contents: LNK
      - id: version
        size: 1
      - id: tagvalues
        type: psyq_obj::tagvalue
        repeat: until
        repeat-until: _.tag == psyq_obj::tags::eof
