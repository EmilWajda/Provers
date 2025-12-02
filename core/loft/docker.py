import asyncio
import aiofiles


async def run_docker_container(name: str, input_file: str, timeout: int | None = None) -> tuple[str, str]:
    async with aiofiles.open(input_file, "rb") as f:
        input_data = await f.read()
    process = await asyncio.create_subprocess_exec(
        "docker",
        "compose",
        "run",
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
            process.terminate()
            stdout, stderr = await process.communicate()
    else:
        stdout, stderr = await process.communicate(input=input_data)
    return stdout.decode(), stderr.decode()
