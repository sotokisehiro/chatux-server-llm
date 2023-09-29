import os

import pytest

from engine import CTranslate2Engine


class TestCTranslate2Engine:
    @pytest.fixture
    def init_engine(self):
        self.engine = CTranslate2Engine(os.cpu_count())

    def test_self_introduction(self, init_engine):
        res = self.engine.generate_text("自己紹介してください。")
        words = [
            "アシスタント",
            "チャット",
            "ボット",
            "言語",
            "モデル",
            "学習",
            "AI",
            "人工",
            "知能",
            "システム",
            "質問",
        ]
        assert any(word in res for word in words)
