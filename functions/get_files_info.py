import os
from os.path import join

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir: bool = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        results: list[str] = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            file_size: str = str(os.path.getsize(item_path))
            is_dir: str = str(os.path.isdir(item_path))
            result: str = f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            results.append(result)
        return "\n".join(results)
    except:
        return f'Error: The "get_files_info()" function failed with an unexpected error'

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
