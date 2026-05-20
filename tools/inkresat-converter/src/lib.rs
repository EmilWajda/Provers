use std::ops::Deref;
use tptp::{
    fof::{LogicFormula, UnitaryFormula},
    top::{AnnotatedFormula, TPTPInput},
};

#[derive(Debug, Clone)]
pub enum Clause<'a> {
    Liveness(&'a LogicFormula<'a>),
    Safety(&'a LogicFormula<'a>),
}

impl<'a> Clause<'a> {
    pub fn from_formula(formula: &'a LogicFormula<'a>) -> Option<Self> {
        todo!()
    }

    pub fn to_inkresat(&self) -> String {
        todo!()
    }
}

pub fn map_formula_to_inkresat(formula: &TPTPInput) -> Option<String> {
    if let TPTPInput::Annotated(annotated) = formula {
        if let AnnotatedFormula::Fof(inner_formula) = annotated.deref() {
            let inner_formula = &inner_formula.0;
            let role = inner_formula.role.0.0;
            if role == "axiom" {
                Clause::from_formula(&inner_formula.formula.0).map(|c| c.to_inkresat())
            } else {
                eprintln!("Only axioms are supported, found role: {role}");
                None
            }
        } else {
            eprintln!("Only FOF formulas are supported");
            None
        }
    } else {
        eprintln!("Includes are not supported");
        None
    }
}
