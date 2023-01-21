import code
import os

from parsers.psyq_obj import PsyqObj

if 0:
	psq = PsyqObj.from_file("SYS.OBJ")

	file_segments = {'section_symbols': None, 'xdefs_xrefs': None, 'section_definitions': None, 'rest': None}

	misc_tags = [PsyqObj.Tags.eof, PsyqObj.Tags.run_at] # TODO: need more examples. some of these tags might belong to sections and will get duplicated

	# Gather up most of the tags and organize them a little

	file_segments["section_symbols"] = [sect for sect in psq.sections if sect.tag == PsyqObj.Tags.section_symbol]
	file_segments["xdefs_xrefs"] = [sect for sect in psq.sections if sect.tag == PsyqObj.Tags.xref or sect.tag == PsyqObj.Tags.xdef]
	file_segments["section_definitions"] = []
	file_segments["rest"] = [sect for sect in psq.sections if sect.tag in misc_tags]

	sec_def = []
	cur_sec = None

	# Assign tags after a SECTION_SWITCH tag to the section referenced by that tag

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

	#print(file_segments["section_definitions"][0][-1].tag, file_segments["section_definitions"][0][-1].value)
	#print(file_segments["section_definitions"][1][-1].tag, file_segments["section_definitions"][1][-1].value)
	#print(len(file_segments["section_definitions"]))

	# Example query after we processed the parsed structure
	codes = [[tv for tv in segment if tv.tag == PsyqObj.Tags.code] for segment in file_segments["section_definitions"]]

	# Gather up XDEFs for later
	xdefs = [sym for sym in file_segments["xdefs_xrefs"] if sym.tag == PsyqObj.Tags.xdef]


	# Creating a structure to hold all the information gathered from SECTION_SYMBOL and SECTION_SWITCH + CODE tags. This could be extended with a dict to hold all the symbols
	sections = {}

	for sect_tv in file_segments["section_symbols"]:
		sect_num = sect_tv.value.number
		sections[sect_num] = {'number': sect_tv.value.number, 'group': sect_tv.value.group, 'alignment': sect_tv.value.alignment, 'name': sect_tv.value.name.str}

	# Figure out if there are code tags in the section, and extract them if so
	for sec in file_segments["section_definitions"]:
		header = sec[0]
		number = header.value.next_sec
		codes_in_section = [tv for tv in sec if tv.tag == PsyqObj.Tags.code]
		if codes_in_section[0]: # We assume 0 or 1 code tags per section. Symbols declared with section+offset seems to support this interpretation
			sections[number]['code'] = codes_in_section[0].value.code.code
			sections[number]['has_code'] = True
		else:
			sections[number]['has_code'] = False

	# Group XDEFs by section number
	xdefs_by_sect_num = {}
	for sym in xdefs:
		syms = xdefs_by_sect_num.get(sym.value.section, {})
		syms[sym.value.number] = { "value": sym.value }
		xdefs_by_sect_num[sym.value.section] = syms


	# Extract the symbols' code from the associated section's code tag. Doesn't take into account if there's padding after a function ends and another begins
	for sectnum, sect in xdefs_by_sect_num.items():
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

	# code.interact(local=locals())

class ObjSymExtractor:
	misc_tags = [PsyqObj.Tags.eof, PsyqObj.Tags.run_at]

	def __init__(self):
		pass

	# TODO : make these class methods
	def from_tagvalues(self, tagvalues):
		file_segments = {'section_symbols': None, 'xdefs_xrefs': None, 'section_definitions': None, 'rest': None}

		# Gather up most of the tags and organize them a little

		file_segments["section_symbols"] = [sect for sect in tagvalues if sect.tag == PsyqObj.Tags.section_symbol]
		file_segments["xdefs_xrefs"] = [sect for sect in tagvalues if sect.tag == PsyqObj.Tags.xref or sect.tag == PsyqObj.Tags.xdef]
		file_segments["section_definitions"] = []
		file_segments["rest"] = [sect for sect in tagvalues if sect.tag in __class__.misc_tags]

		sec_def = []
		cur_sec = None

		# Assign tags after a SECTION_SWITCH tag to the section referenced by that tag

		for sect in tagvalues:
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

		# Gather up XDEFs for later
		xdefs = [sym for sym in file_segments["xdefs_xrefs"] if sym.tag == PsyqObj.Tags.xdef]

		# Creating a structure to hold all the information gathered from SECTION_SYMBOL and SECTION_SWITCH + CODE tags. This could be extended with a dict to hold all the symbols
		sections = {}

		for sect_tv in file_segments["section_symbols"]:
			sect_num = sect_tv.value.number
			sections[sect_num] = {'number': sect_tv.value.number, 'group': sect_tv.value.group, 'alignment': sect_tv.value.alignment, 'name': sect_tv.value.name.str}

		# Figure out if there are code tags in the section, and extract them if so
		for sec in file_segments["section_definitions"]:
			header = sec[0]
			number = header.value.next_sec
			codes_in_section = [tv for tv in sec if tv.tag == PsyqObj.Tags.code]
			if codes_in_section[0]: # We assume 0 or 1 code tags per section. Symbols declared with section+offset seems to support this interpretation
				sections[number]['code'] = codes_in_section[0].value.code.code
				sections[number]['has_code'] = True
			else:
				sections[number]['has_code'] = False

		# Group XDEFs by section number
		xdefs_by_sect_num = {}
		for sym in xdefs:
			syms = xdefs_by_sect_num.get(sym.value.section, {})
			syms[sym.value.number] = { "value": sym.value }
			xdefs_by_sect_num[sym.value.section] = syms


		# Extract the symbols' code from the associated section's code tag. Doesn't take into account if there's padding after a function ends and another begins
		for sectnum, sect in xdefs_by_sect_num.items():
				if not sections[sectnum]["has_code"]: # TODO : what to do when there is no code section? might need to work with tags for uninitialized memory.
					continue

				sym_offsets = [sym["value"].offset for symnum,sym in sect.items()]
				sym_ends = sym_offsets[1:]
				sym_ends.append(len(sections[sectnum]["code"]))


				offset_arrays_index = 0
				for symnum,sym in sect.items():
					sym["end"] = sym_ends[offset_arrays_index]
					sym["code"] = sections[sectnum]["code"][sym["value"].offset:sym["end"]]
					offset_arrays_index += 1

		result = { 'success': True, 'sections': sections, 'file_segments': file_segments, 'xdefs_by_sect_num': xdefs_by_sect_num } # Intermediate format accepted by to_*() functions (TODO: write these)

	def to_bins_and_txts(self, res_dict, identifier, cwd_path):
		if not res_dict.get('success', False): # Pretty useless for now. Validating results is TODO
			print("Result passed to to_bins_and_txts is invalid")
			return

		if not os.path.exists(cwd_path):
			print("Nonexistent path given to to_bins_and_txts()")
			return

		dest_dir_path = os.path.join(cwd_path, identifier)
		if not os.path.isdir(dest_dir_path):
			os.mkdir(dest_dir_path)

		xdefs = res_dict['xdefs_by_sect_num']
		for xdef in xdefs:
			txt_name = "{}_{}_metadata.txt".format(identifier, hex(xdef["value"].number))
			txt_path = os.path.join(dest_dir_path, txt_name)
			with open(txt_path, "w") as txtfile:
				txtfile.write("Number: {}".format(hex(xdef["value"].number)))
				txtfile.write("Name: {}".format(xdef["value"].sym.str))
				txtfile.write("Offset: {}".format(hex(xdef["value"].offset)))

			bin_name = "{}_{}_code.bin".format(identifier, hex(xdef["value"].number))
			bin_path = os.path.join(dest_dir_path, bin_name)
			with open(bin_path, "wb") as binfile:
				binfile.write(xdef["code"])
