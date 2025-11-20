from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import ClassVar, Any
from random import Random
from typing import get_origin, get_args

from ..formulas import LogicToken


@dataclass
class Generator(ABC):
    name: ClassVar[str]
    param_spec: ClassVar[dict[str, type]]

    seed: int
    random: Random = field(init=False)
    params: dict[str, Any]

    def __post_init__(self):
        self.random = Random(self.seed)
        self._validate_params()

    def _validate_params(self):
        for key, expected_type in self.param_spec.items():
            if key not in self.params:
                raise ValueError(f"Missing required parameter '{key}' in params.")

            value = self.params[key]

            # Obsługa list dodatkowo typowanych
            if get_origin(expected_type) is list:
                if not isinstance(value, list):
                    raise TypeError(
                        f"Parameter '{key}' must be a list, got {type(value).__name__}"
                    )

                (elem_type,) = get_args(expected_type)
                for i, elem in enumerate(value):
                    if not isinstance(elem, elem_type):
                        raise TypeError(
                            f"Element params['{key}'][{i}] must be {elem_type}, "
                            f"got {type(elem).__name__}"
                        )

            # obsługa zwykłych typów
            else:
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Parameter '{key}' must be {expected_type}, got {type(value).__name__}."
                    )

    @abstractmethod
    def generate(self) -> list[LogicToken]: ...
