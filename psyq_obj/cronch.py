from parsers.psyq_lib import PsyqLib
from obj_sym_extractor import ObjSymExtractor
import os
import sys

if len(sys.argv) == 1:
	print("Usage: cronch.py <library file>")
	print("PROTIP: you'll want the library file to be in the current directory. Output directory is the first part of the filename split on '.'")
	exit()

extractor = ObjSymExtractor()
psq_lib = PsyqLib.from_file(sys.argv[1])

dest_folder_path = os.path.join(os.getcwd(), sys.argv[1].split(".")[0])
if not os.path.isdir(dest_folder_path):
	os.mkdir(dest_folder_path)

for module in psq_lib.modules:
	res = extractor.from_tagvalues(module.tagvalues)
	extractor.to_bins_and_txts(res, module.name.strip(), dest_folder_path)
