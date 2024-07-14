import tempfile
import unittest

from gig import Ent, EntType

from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams


class TestDCN(unittest.TestCase):
    def test_run(self):
        ents = Ent.list_from_type(EntType.DISTRICT)
        values = [ent.population for ent in ents]
        dcn = DCN1985.from_ents(
            ents,
            values,
            algo_params=DCN1985AlgoParams(max_iterations=2),
            render_params=DCN1985RenderParams(
                super_title="Sri Lanka's Districts",
                title="Population",
            ),
        )
        dcn.run(
            tempfile.mkdtemp(),
        )
