import numpy as np
import neurom as nm
from morph_tool.nrnhines import point_to_section_end


from morphio.mut import Morphology

from pathlib import Path
DATA = Path(__file__).parent / 'data'

def test_gogo():
    m = Morphology('written.asc')
    a = [5157.592773, 1235.704834, 5408.502930]
    result = point_to_section_end('written.asc', a)
    print("result: {}".format(result))
