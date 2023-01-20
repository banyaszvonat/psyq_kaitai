import code

from psyq_obj import PsyqObj

psq = PsyqObj.from_file("SYS.OBJ")

file_segments = {'section_symbols': None, 'xdefs_xrefs': None, 'section_definitions': None, 'rest': None}

misc_tags = [PsyqObj.Tags.eof, PsyqObj.Tags.run_at] # TODO: need more examples. some of these tags might belong to sections and will get duplicated

file_segments["section_symbols"] = [sect for sect in psq.sections if sect.tag == PsyqObj.Tags.section_symbol]
file_segments["xdefs_xrefs"] = [sect for sect in psq.sections if sect.tag == PsyqObj.Tags.xref or sect.tag == PsyqObj.Tags.xdef]
file_segments["section_definitions"] = []
file_segments["rest"] = [sect for sect in psq.sections if sect.tag in misc_tags]

sec_def = []
cur_sec = None

for sect in psq.sections:
	if sect.tag == PsyqObj.Tags.section_switch:
		if cur_sec: # Prevent appending an empty array as the first section
			file_segments["section_definitions"].append(sec_def)
		sec_def = []
		sec_def.append(sect)
		cur_sec = sect
	elif sect.tag == PsyqObj.Tags.eof and cur_sec:
		file_segments["section_definitions"].append(sec_def)
	elif cur_sec:
		sec_def.append(sect)

print(file_segments["section_definitions"][0][-1].tag, file_segments["section_definitions"][0][-1].value)
print(file_segments["section_definitions"][1][-1].tag, file_segments["section_definitions"][1][-1].value)
print(len(file_segments["section_definitions"]))

codes = [[tv for tv in segment if tv.tag == PsyqObj.Tags.code] for segment in file_segments["section_definitions"]]
symbols = [sym for sym in file_segments["xdefs_xrefs"] if sym.tag == PsyqObj.Tags.xdef]

sections = {}

for sect_tv in file_segments["section_symbols"]:
	sect_num = sect_tv.value.number
	sections[sect_num] = {'number': sect_tv.value.number, 'group': sect_tv.value.group, 'alignment': sect_tv.value.alignment, 'name': sect_tv.value.name.str}

for sec in file_segments["section_definitions"]:
	header = sec[0]
	number = header.value.next_sec
	codes = [tv for tv in sec if tv.tag == PsyqObj.Tags.code]
	if codes[0]: # We assume 0 or 1 code tags per section. Symbols declared with section+offset seems to support this interpretation
		sections[number]['code'] = codes[0].value.code.code
		sections[number]['has_code'] = True
	else:
		sections[number]['has_code'] = False

symbols_by_sect_num = {}
for sym in file_segments["xdefs_xrefs"]:
	if sym.tag == PsyqObj.Tags.xdef:
		syms = symbols_by_sect_num.get(sym.value.section, {})
		syms[sym.value.number] = { "value": sym.value }
		symbols_by_sect_num[sym.value.section] = syms


for sectnum, sect in symbols_by_sect_num.items():
		if not sections[sectnum]["has_code"]: # TODO: what to do when there is no code section? might need to work with tags for uninitialized memory.
			continue

		sym_offsets = [sym["value"].offset for symnum,sym in sect.items()]
		sym_ends = sym_offsets[1:]
		sym_ends.append(len(sections[sectnum]["code"]))


		offset_arrays_index = 0
		for symnum,sym in sect.items():
			sym['end'] = sym_ends[offset_arrays_index]
			sym['code'] = sections[sectnum]["code"][sym['value'].offset:sym['end']]
			offset_arrays_index += 1

code.interact(local=locals())

