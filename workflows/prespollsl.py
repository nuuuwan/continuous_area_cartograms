import json
import os

from gig import Ent, EntType
from utils import File, JSONFile

# ENT_TYPE = EntType.PD
# EXAMPLE_NAME = 'lk_pds_in_units'

ENT_TYPE = EntType.ED
EXAMPLE_NAME = 'lk_eds_in_units'

hexbin_data_path = os.path.join(
    'examples', EXAMPLE_NAME, 'hexbin.svg.json.postprocess.json'
)
idx = JSONFile(hexbin_data_path).read()['idx']
ents = Ent.list_from_type(ENT_TYPE)

name_to_id = {ent.name: ent.id for ent in ents}

idx2 = {}
for name, points in idx.items():
    id = name_to_id[name]
    idx2[id] = points[0]

output_path = hexbin_data_path + '.txt'
File(output_path).write(json.dumps(idx2, indent=4))
os.startfile(output_path)
