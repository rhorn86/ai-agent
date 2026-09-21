import os
from os.path import join
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_path: str = os.path.normpath(join(working_dir_abs, file_path))
        valid_target_path: bool = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_path]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, cwd=working_dir_abs, text=True, timeout=30)
        return f'{f"Process exited with code {result.returncode}. " if result.returncode != 0 else ""}{f"No output produced" if not result.stdout and not result.stderr else f"STDOUT: {result.stdout}STDERR: {result.stderr}"}'
    except:
        return f'Error: executing Python file'




