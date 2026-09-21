import os
from functions.get_files_info import get_files_info

directories: list[str] = [".", "pkg", "/bin", "../"]
for directory in directories:
    info: str = get_files_info("calculator", directory)
    lines: list[str] = info.split("\n")
    new_lines: list[str] = []
    for line in lines:
        new_line: str = "  " + line
        new_lines.append(new_line)
    new_info: str = "\n".join(new_lines)
    print(f"Result for {"current directory" if directory == "." else f"'{directory}' directory"}:")
    print(new_info)
