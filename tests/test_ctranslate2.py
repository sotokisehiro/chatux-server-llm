import os

import pytest

from engine import CTranslate2Engine


class TestCTranslate2Engine:
    @pytest.fixture
    def init_engine(self):
        self.engine = CTranslate2Engine(os.cpu_count())

    def test_self_introduction(self, init_engine):
        res = self.engine.generate_text("自己紹介してください。")
        assert "アシスタント" in res
