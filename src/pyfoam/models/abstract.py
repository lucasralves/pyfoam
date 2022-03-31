from typing import Protocol

class model(Protocol):

    @staticmethod
    def action(func):
        def wrapper(self, *args, **argsv):
            func(self, *args, **argsv)
            self.run()
            return
        return wrapper
    
    def run(self) -> None:
        pass