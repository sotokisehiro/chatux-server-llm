class Engine(object):
    def __init__(self, cpu_thread=0) -> None:
        self.cpu_thread = cpu_thread

    def generate_text(self, input) -> str:
        raise NotImplementedError()
