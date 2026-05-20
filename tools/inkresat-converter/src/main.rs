use nom::error::Error;
use std::{
    io::{self, Read},
    process::ExitCode,
};
use tptp::TPTPIterator;

fn read_stdin() -> io::Result<Box<[u8]>> {
    let mut buffer = vec![];
    io::stdin().lock().read_to_end(&mut buffer)?;
    Ok(buffer.into_boxed_slice())
}

fn main() -> ExitCode {
    let Ok(bytes) = read_stdin() else {
        eprintln!("Failed to read from stdin");
        return ExitCode::FAILURE;
    };
    let mut parser = TPTPIterator::<Error<_>>::new(&bytes);
    println!("begin");
    let mut first = true;
    for input in &mut parser {
        if !first {
            println!("&");
        }
        first = false;

        if let Ok(formula) = input {
            if let Some(mapped) = inkresat_converter::map_formula_to_inkresat(&formula) {
                println!("({mapped})");
            } else {
                return ExitCode::FAILURE;
            }
        } else {
            eprintln!("Error parsing formula");
            return ExitCode::FAILURE;
        }
    }
    println!("end");
    ExitCode::SUCCESS
}
