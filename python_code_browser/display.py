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
		
code.interact(local=locals())

