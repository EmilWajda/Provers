from .generator import Generator

from .problem1 import Problem1
from .problem2 import Problem2
from .problem3 import Problem3
from .problem4 import Problem4
from .problem5 import Problem5
from .problem6 import Problem6
from .problem7 import Problem7
from .problem8 import Problem8
from .problem9a import Problem9a
from .problem9b import Problem9b
from .problem10 import Problem10
from .problem11 import Problem11
from .problem12 import Problem12
from .problem13 import Problem13
from .problem14 import Problem14
from .problem15 import Problem15
from .problem16 import Problem16
from .problem17 import Problem17
from .problem18 import Problem18

_ALL_PROBLEMS: list[type[Generator]] = [
    Problem1,
    Problem2,
    Problem3,
    Problem4,
    Problem5,
    Problem6,
    Problem7,
    Problem8,
    Problem9a,
    Problem9b,
    Problem10,
    Problem11,
    Problem12,
    Problem13,
    Problem14,
    Problem15,
    Problem16,
    Problem17,
    Problem18,
]

KNOWN_PROBLEMS: dict[str, type[Generator]] = {gen.name: gen for gen in _ALL_PROBLEMS}
