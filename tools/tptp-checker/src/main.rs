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

fn format_position(input: &[u8], full: &[u8]) -> String {
    let offset = full.len() - input.len();
    let line = full[..offset].iter().filter(|&&c| c == b'\n').count() + 1;
    let next_line_start = input.iter().position(|&c| c == b'\n').unwrap_or(input.len());
    let line_content = &input[..next_line_start];
    format!("line {}: `{}`", line, str::from_utf8(line_content).unwrap_or("???"))
}

fn main() -> ExitCode {
    let Ok(bytes) = read_stdin() else {
        println!("Failed to read from stdin");
        return ExitCode::FAILURE;
    };
    let mut parser = TPTPIterator::<Error<_>>::new(&bytes);
    for input in &mut parser {
        if let Err(e) = input {
            println!("Error parsing formula - {:?} at {}", e.code, format_position(e.input, &bytes));
            return ExitCode::FAILURE;
        }
    }
    if parser.remaining.is_empty() {
        println!("TPTP syntax is valid");
        ExitCode::SUCCESS
    } else {
        println!("Unparsed input remaining - {}", format_position(parser.remaining, &bytes));
        ExitCode::FAILURE
    }
}
