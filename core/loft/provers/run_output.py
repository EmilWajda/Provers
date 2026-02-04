from dataclasses import dataclass
from enum import Enum
from typing import Callable, Self


class RunResult(Enum):
    SAT = "satisfiable"
    UNSAT = "unsatisfiable"
    UNKNOWN = "unknown"
    TIMEOUT = "timeout"


def basic_result_parser(sat: str, unsat: str) -> Callable[[str], RunResult]:
    def parser(output: str) -> RunResult:
        output = output.lower()
        if unsat in output:
            return RunResult.UNSAT
        if sat in output:
            return RunResult.SAT
        return RunResult.UNKNOWN

    return parser


def _parse_real_time(time_str: str) -> float:
    parts = time_str.split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    else:
        raise ValueError(f"Invalid real time format: {time_str}")


@dataclass
class RunStats:
    system_time: float  # in seconds
    real_time: float  # in seconds
    peak_memory: int  # in kilobytes

    @classmethod
    def from_raw_stderr(cls, stderr: str) -> Self | None:
        # gnu time stats
        lines = stderr.strip().splitlines()
        lines = [line.strip().lower() for line in lines]
        system_time_line = next(filter(lambda l: l.startswith("system time"), lines), None)
        real_time_line = next(filter(lambda l: l.startswith("elapsed"), lines), None)
        peak_memory_line = next(filter(lambda l: l.startswith("maximum resident"), lines), None)
        if not system_time_line or not real_time_line or not peak_memory_line:
            return None
        system_time = float(system_time_line.split(": ")[-1])
        real_time = _parse_real_time(real_time_line.split(": ")[-1])
        peak_memory = int(peak_memory_line.split(": ")[-1])
        return cls(system_time, real_time, peak_memory)

    def to_dict(self) -> dict:
        return {
            "system_time": self.system_time,
            "real_time": self.real_time,
            "peak_memory": self.peak_memory,
        }
