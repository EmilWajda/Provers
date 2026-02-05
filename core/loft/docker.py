import asyncio
import aiofiles
import time


async def run_docker_container(name: str, input_file: str, timeout: int | None = None) -> tuple[str, str, int | None]:
    async with aiofiles.open(input_file, "rb") as f:
        input_data = await f.read()
    container_name = f"loft-{time.time_ns()}"
    process = await asyncio.create_subprocess_exec(
        "docker",
        "compose",
        "run",
        "--name",
        container_name,
        "--rm",
        name,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    if timeout:
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(input=input_data), timeout=timeout)
        except asyncio.TimeoutError:
            kill_process = await asyncio.create_subprocess_exec(
                "docker", "kill", container_name, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL
            )
            stdout, stderr = (await asyncio.gather(process.communicate(), kill_process.wait()))[0]
            return stdout.decode(), stderr.decode(), None
    else:
        stdout, stderr = await process.communicate(input=input_data)
    return stdout.decode(), stderr.decode(), process.returncode


async def run_tptp_checker(input_file: str) -> bool:
    _, _, ret_code = await run_docker_container("tptp-checker", input_file)
    return ret_code == 0
