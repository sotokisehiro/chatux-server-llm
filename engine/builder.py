from abc import ABC, abstractmethod

from engine.ctranslate2 import CTranslate2Engine
from engine.engine import Engine
from engine.llama_cpp import LlamaCppEngine


class EngineBuilder(ABC):
    @abstractmethod
    def get_engine(self) -> Engine:
        raise NotImplementedError()


class Director(object):
    def set_builder(self, builder: EngineBuilder) -> None:
        self.__builder: EngineBuilder = builder

    def get_engine(self) -> Engine:
        return self.__builder.get_engine()


class LlamaCppEngineBuilder(EngineBuilder):
    def __init__(self, cpu_thread=0) -> None:
        self.cpu_thread = cpu_thread

    def get_engine(self) -> LlamaCppEngine:
        engine = LlamaCppEngine(self.cpu_thread)
        return engine


class CTranslate2EngineBuilder(EngineBuilder):
    def __init__(self, cpu_thread=0) -> None:
        self.cpu_thread = cpu_thread

    def get_engine(self) -> CTranslate2Engine:
        engine = CTranslate2Engine(self.cpu_thread)
        return engine
