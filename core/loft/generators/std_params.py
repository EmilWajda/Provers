from enum import Enum
from .param_spec import Integer, IntegerList, Float, Boolean, Choice

_BIGGER_THAN_ZERO = 1e-10


class StandardParams(Enum):
    CLAUSES = Integer("Number of all clauses in the formula.", min_value=2)
    LENGTHS = IntegerList("List of clause lengths to be used in the formula.", min_length=2, min_value=1)
    LAMBDA = Float("Lambda parameter for the Poisson distribution.", min_value=_BIGGER_THAN_ZERO)
    RATIO = Float("Ratio parameter affecting number of atoms.", min_value=_BIGGER_THAN_ZERO)
    LENGTH = Integer("Length of each clause in the formula.", min_value=2)
    DISTRIBUTION = Choice(
        "Distribution type for clause groups lengths.\n'even' - all groups have the same number of clauses.\n'tiny_short' - nearly no shortest clauses.\n'tiny_long' - nearly no longest clauses.",
        choices=["even", "tiny_short", "tiny_long"],
    )
    SAFETY_PERCENTAGE = Float("Percentage of safety clauses in the formula.", min_value=0, max_value=100)
    POISSON = Boolean("Whether to use Poisson distribution for clause lengths.")
    LAMBDA_OR_NONE = Float("Lambda parameter for the Poisson distribution (zero for N/A).", min_value=0)
    LENGTHS_OR_NONE = IntegerList("List of clause lengths to be used in the formula (may be empty).", min_value=1)
    CONJUNCTION = Boolean("Whether to use conjunction for combining subformulas.")
    MODE = Choice(
        "Mode of the problem.\n'contradictory' - formulas are contradictory.\n'subcontrary' - formulas are subcontrary.\n'subalternated' - formulas are subalternated.",
        choices=["contradictory", "subcontrary", "subalternated"],
    )
