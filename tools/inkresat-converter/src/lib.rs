use std::ops::Deref;
use tptp::{
    fof::{BinaryAssoc, BinaryFormula, LogicFormula, Quantifier, UnitFormula, UnitaryFormula},
    top::{AnnotatedFormula, TPTPInput},
};

pub const LIVENESS_CONDITION_FUNCTION: &str = "ssGTE";
pub const INKRESAT_RELATION: &str = "r1";

pub trait ParenthesesDroppable<'a> {
    fn drop_parentheses(&self) -> LogicFormula<'a>;
}

impl<'a> ParenthesesDroppable<'a> for LogicFormula<'a> {
    fn drop_parentheses(&self) -> LogicFormula<'a> {
        if let LogicFormula::Unitary(UnitaryFormula::Parenthesised(inner)) = self {
            inner.drop_parentheses()
        } else {
            self.clone()
        }
    }
}

impl<'a> ParenthesesDroppable<'a> for UnitFormula<'a> {
    fn drop_parentheses(&self) -> LogicFormula<'a> {
        match self {
            UnitFormula::Unitary(UnitaryFormula::Parenthesised(inner)) => inner.drop_parentheses(),
            UnitFormula::Unitary(inner) => LogicFormula::Unitary(inner.clone()),
            UnitFormula::Unary(inner) => LogicFormula::Unary(inner.clone()),
        }
    }
}

pub fn map_inner_cnf_to_inkresat(formula: &LogicFormula) -> Option<String> {
    Some(format!("{formula:?}")) // TODO
}

#[derive(Debug, Clone)]
pub enum Clause<'a> {
    Liveness(LogicFormula<'a>),
    Safety(LogicFormula<'a>),
}

impl<'a> Clause<'a> {
    pub fn from_formula(formula: &'a LogicFormula) -> Option<Self> {
        let LogicFormula::Unitary(UnitaryFormula::Quantified(quantifier)) = formula.drop_parentheses() else {
            eprintln!("Only quantified formulas are supported");
            return None;
        };
        if quantifier.quantifier != Quantifier::Forall {
            eprintln!("The first quantifier can only be '!' (for all)");
            return None;
        }

        let quantifier = quantifier.formula.drop_parentheses();
        if let LogicFormula::Unitary(UnitaryFormula::Quantified(quantifier)) = quantifier {
            if quantifier.quantifier != Quantifier::Exists {
                eprintln!("The second quantifier can only be '?' (exists)");
                return None;
            }
            let LogicFormula::Binary(BinaryFormula::Assoc(BinaryAssoc::And(and))) =
                quantifier.formula.drop_parentheses()
            else {
                eprintln!("The formula must be a conjunction of two formulas");
                return None;
            };
            if and.0.len() != 2 || !and.0.first().unwrap().to_string().starts_with(LIVENESS_CONDITION_FUNCTION) {
                eprintln!(
                    "The first conjunct must be a liveness condition of the form {LIVENESS_CONDITION_FUNCTION}(...)"
                );
                return None;
            }
            Some(Self::Liveness(and.0[1].drop_parentheses()))
        } else {
            Some(Self::Safety(quantifier))
        }
    }

    pub fn to_inkresat(&self) -> Option<String> {
        match self {
            Clause::Liveness(formula) => {
                map_inner_cnf_to_inkresat(formula).map(|res| format!("<{}> {}", INKRESAT_RELATION, res))
            },
            Clause::Safety(formula) => {
                map_inner_cnf_to_inkresat(formula).map(|res| format!("[{}] {}", INKRESAT_RELATION, res))
            },
        }
    }
}

pub fn map_formula_to_inkresat(formula: &TPTPInput) -> Option<String> {
    let TPTPInput::Annotated(annotated) = formula else {
        eprintln!("Includes are not supported");
        return None;
    };
    let AnnotatedFormula::Fof(inner_formula) = annotated.deref() else {
        eprintln!("Only FOF formulas are supported");
        return None;
    };

    let inner_formula = &inner_formula.0;
    let role = inner_formula.role.0.0;
    if role == "axiom" {
        Clause::from_formula(&inner_formula.formula.0).and_then(|c| c.to_inkresat())
    } else {
        eprintln!("Only axioms are supported, found role: {role}");
        None
    }
}
