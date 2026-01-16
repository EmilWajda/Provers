from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import ClassVar, Any
from argparse import ArgumentParser


@dataclass(frozen=True)
class ParamSpec(ABC):
    name: ClassVar[str]
    description: str

    @abstractmethod
    def validate(self, value: Any) -> bool: ...

    @abstractmethod
    def get_checks(self) -> dict[str, Any]: ...

    @abstractmethod
    def sanitize_value(self, value: Any) -> str: ...

    @abstractmethod
    def add_cli_argument(self, name: str, parser: ArgumentParser) -> None: ...

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": self.name,
            "description": self.description,
            "checks": self.get_checks(),
        }


@dataclass(frozen=True)
class Integer(ParamSpec):
    name: ClassVar[str] = "integer"
    min_value: int | None = None
    max_value: int | None = None

    def validate(self, value: Any) -> bool:
        if not isinstance(value, int):
            return False
        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False
        return True

    def get_checks(self) -> dict[str, Any]:
        return {"min": self.min_value, "max": self.max_value}
    
    def sanitize_value(self, value: Any) -> str:
        return str(value)

    def add_cli_argument(self, name: str, parser: ArgumentParser) -> None:
        parser.add_argument(name, type=int, help=self.description)


@dataclass(frozen=True)
class Float(ParamSpec):
    name: ClassVar[str] = "float"
    min_value: float | None = None
    max_value: float | None = None

    def validate(self, value: Any) -> bool:
        if not isinstance(value, float):
            return False
        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False
        return True

    def get_checks(self) -> dict[str, Any]:
        return {"min": self.min_value, "max": self.max_value}
    
    def sanitize_value(self, value: Any) -> str:
        return f"{value:.2f}"

    def add_cli_argument(self, name: str, parser: ArgumentParser) -> None:
        parser.add_argument(name, type=float, help=self.description)


@dataclass(frozen=True)
class Boolean(ParamSpec):
    name: ClassVar[str] = "boolean"

    def validate(self, value: Any) -> bool:
        return isinstance(value, bool)

    def get_checks(self) -> dict[str, Any]:
        return {}
    
    def sanitize_value(self, value: Any) -> str:
        return "true" if value else "false"

    def add_cli_argument(self, name: str, parser: ArgumentParser) -> None:
        parser.add_argument(f"--{name}", action="store_true", help=self.description)


@dataclass(frozen=True)
class Choice(ParamSpec):
    name: ClassVar[str] = "choice"
    choices: list[str]

    def validate(self, value: Any) -> bool:
        return isinstance(value, str) and value in self.choices

    def get_checks(self) -> dict[str, Any]:
        return {"choices": self.choices}
    
    def sanitize_value(self, value: Any) -> str:
        return value

    def add_cli_argument(self, name: str, parser: ArgumentParser) -> None:
        parser.add_argument(name, type=str, choices=self.choices, help=self.description)


@dataclass(frozen=True)
class IntegerList(ParamSpec):
    name: ClassVar[str] = "integer_list"
    min_length: int | None = None
    max_length: int | None = None
    min_value: int | None = None
    max_value: int | None = None

    def validate(self, value: Any) -> bool:
        if not isinstance(value, list) or not all(isinstance(v, int) for v in value):
            return False
        if self.min_length is not None and len(value) < self.min_length:
            return False
        if self.max_length is not None and len(value) > self.max_length:
            return False
        for v in value:
            if self.min_value is not None and v < self.min_value:
                return False
            if self.max_value is not None and v > self.max_value:
                return False
        return True

    def get_checks(self) -> dict[str, Any]:
        return {
            "min_length": self.min_length,
            "max_length": self.max_length,
            "min_value": self.min_value,
            "max_value": self.max_value,
        }
    
    def sanitize_value(self, value: Any) -> str:
        return "_".join(str(v) for v in value)

    def add_cli_argument(self, name: str, parser: ArgumentParser) -> None:
        parser.add_argument(name, type=int, nargs="*", help=self.description)
