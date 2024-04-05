from abc import ABC, abstractmethod


class Engine(ABC):
    def __init__(self, cpu_thread=0) -> None:
        self.cpu_thread = cpu_thread

    @abstractmethod
    def generate_text(self, text_input: str) -> str:
        raise NotImplementedError()
