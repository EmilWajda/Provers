from enum import Enum
from .param_spec import Integer, IntegerList, Float, Boolean, Choice

_BIGGER_THAN_ZERO = 1e-10


class StandardParams(Enum):
    CLAUSES = Integer("Number of all clauses in the formula.", min_value=2)
    LENGTHS = IntegerList("List of clause lengths to be used in the formula.", min_length=2, min_value=2)
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
    CLAUSES_F1 = Integer("Number of clauses for F1 (structural asymmetry).", min_value=2)
    CLAUSES_F2 = Integer("Number of clauses for F2 (structural asymmetry).", min_value=2)
    SEMANTIC_CASE = Choice(
        "Case for semantic asymmetry.\n'case1' - F1 has 80% safety, F2 has 20%.\n'case2' - F1 has 20% safety, F2 has 80%.",
        choices=["case1", "case2"]
    )
    EVOLUTION_MODE = Choice(
        "Evolutionary relation to test.\n'r1' - F1 => F2.\n'r2' - F2 => F1.\n'r3' - F1 ^ ~F2.\n'r4' - F1 ^ F2.",
        choices=["r1", "r2", "r3", "r4"],
    )
    MODIFICATION_PERCENT = Float("Percentage of clauses to modify (e.g. 5, 10, 20, 50).", min_value=0, max_value=100)
    REDUNDANCY_PERCENT = Float("Percentage of redundant clauses (e.g. 0, 10, 25, 50).", min_value=0)
    REDUNDANCY_MODE = Choice(
        "Relation to test for redundancy.\n't1' - Equivalence: F => F' and F' => F.\n't2' - Strengthening: F' => F.\n't3' - Weakening: F => F'.\n't4' - Co-satisfiability: F ^ F'.",
        choices=["t1", "t2", "t3", "t4"],
    )
    DEGRADATION_PERCENT = Float("Percentage of clauses to remove (e.g. 5, 10, 25, 50).", min_value=0, max_value=100)
    DEGRADATION_VARIANT = Choice(
        "Variant of clause removal.\n'd1' - Random.\n'd2' - Safety preference.\n'd3' - Liveness preference.",
        choices=["d1", "d2", "d3"],
    )
    MISSING_INFO_MODE = Choice(
        "Relation to test for missing info (P12).\n'r1' - F => R.\n'r2' - F' => R.\n'r3' - F ^ ~R.\n'r4' - F' ^ ~R.",
        choices=["r1", "r2", "r3", "r4"],
    )
    TOPOLOGY_VARIANT = Choice(
        "Topology variant for Problem 13.\n'g1' - Sparse.\n'g2' - Dense.\n'g3' - Tree-like.\n'g4' - Modular.\n'g5' - Hub.",
        choices=["g1", "g2", "g3", "g4", "g5"],
    )
    MODULES_COUNT = Integer("Number of modules (e.g. 2, 3, 5).", min_value=2)
    COUPLING_VARIANT = Choice(
        "Coupling variant for modules.\n'c1' - Independent (0%).\n'c2' - Weakly coupled (10%).\n'c3' - Medium coupled (25%).\n'c4' - Strongly coupled (50%).",
        choices=["c1", "c2", "c3", "c4"],
    )
    MODULAR_MODE = Choice(
        "Relation to test for modularity (P14).\n'locality' - M_i => R.\n'globality' - G => R.\n'co-sat' - G ^ R.",
        choices=["locality", "globality", "co-sat"],
    )
    CONFLICT_PERCENT = Float("Percentage of clauses involved in conflicts.", min_value=0, max_value=100)
    CONFLICT_TYPE = Choice(
        "Type of conflict (P15).\n'c1' - Direct.\n'c2' - Conditional.\n'c3' - Behavioral.",
        choices=["c1", "c2", "c3"],
    )
    CONFLICT_DEPTH = Choice(
        "Depth/Structural variant of conflict.\n'v1' - Local.\n'v2' - Near.\n'v3' - Distributed.",
        choices=["v1", "v2", "v3"],
    )