from .tptp_builder import TPTPBuilder
from .formulas  import ForAll, Exists, Not, Alternative, Implication, GreaterThan, Atom, Conjunction, BasicToken, LogicToken
from .generators.generator import Generator
from .generators.problem1 import Problem1


# p = ForAll("U", Exists("V", Conjunction([GreaterThan("U", "V"), Implication(Not(Atom("var14", "V")), Atom("var5", "U"))])))

# print(p.to_tptp())

p = Problem1(144, {"clauses": 10, "lengths": [2,3,4]})
clauses = p.generate()

builder = TPTPBuilder()
print(builder.build_tptp_str(clauses))
