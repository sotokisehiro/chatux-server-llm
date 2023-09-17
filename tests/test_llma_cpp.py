import os

import pytest

from engine import LlamaCppEngine


class TestLlamaCppEngine:
    @pytest.fixture
    def init_engine(self):
        self.engine = LlamaCppEngine(os.cpu_count())

    def test_self_introduction(self, init_engine):
        res = self.engine.generate_text("自己紹介してください。")
        assert "ELYZA" in res
