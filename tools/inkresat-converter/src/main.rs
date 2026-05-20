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
    for input in &mut parser {
        if let Ok(formula) = input {
            println!("{formula}");
        } else {
            eprintln!("Error parsing formula");
            return ExitCode::FAILURE;
        }
    }
    ExitCode::SUCCESS
}
