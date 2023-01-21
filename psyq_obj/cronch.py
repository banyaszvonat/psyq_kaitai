from parsers.psyq_lib import PsyqLib
from obj_sym_extractor import ObjSymExtractor
import os

extractor = ObjSymExtractor()
psq_lib = PsyqLib.from_file("LIBMCRD.LIB")

dest_folder_path = os.path.join(os.getcwd(), "LIBMCRD.LIB".split(".")[0])
if not os.path.isdir(dest_folder_path):
	os.mkdir(dest_folder_path)

for module in psq_lib.modules:
	res = extractor.from_tagvalues(module.tagvalues)
	extractor.to_bins_and_txts(res, module.name.strip(), dest_folder_path)
