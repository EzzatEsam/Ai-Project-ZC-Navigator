import time

class timer :
    def __init__(self) -> None:
        pass

    def start(self) :
        self.start = time.time();
        return self

    def get_elabsed(self) :
        return time.time() - self.start