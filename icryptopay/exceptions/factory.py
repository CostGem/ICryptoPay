import gc
from typing import Optional, Type, Union


class CodeErrorFactory(Exception):
    """CryptoPay API Exception"""

    __error_code: Optional[int] = None
    __error_name: Optional[str] = None

    def __init__(self, code: Optional[int] = None, name: Optional[str] = None) -> None:
        self.code = code
        self.name = name

        super().__init__(self.code)

    @classmethod
    def __call__(cls, code: int, name: Optional[str] = None) -> Union["CodeErrorFactory", Type["CodeErrorFactory"]]:
        if name:
            return cls.exception_to_raise(code=code, name=name)

        return cls.exception_to_handle(code=code)

    @classmethod
    def exception_to_handle(cls, code: Optional[int] = None) -> Type["CodeErrorFactory"]:
        if code is None:
            return cls

        catch_exc_classname = cls.generate_exc_classname(code=code)

        for obj in gc.get_objects():
            if obj.__class__.__name__ == catch_exc_classname:
                return obj.__class__

        return type(catch_exc_classname, (cls,), {})

    @classmethod
    def exception_to_raise(cls, code: int, name: str) -> "CodeErrorFactory":
        """Returns an error with error code and error_name"""

        exception_type = type(cls.generate_exc_classname(code=code), (cls,), {})
        return exception_type(code, name)

    @classmethod
    def generate_exc_classname(cls, code: Optional[int]) -> str:
        """Generates unique exception classname based on error code"""

        return f"{cls.__name__}_{code}"

    def __str__(self):
        return f"[{self.code}] {self.name}\n"
