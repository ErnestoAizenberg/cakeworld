import os
from functools import lru_cache
from typing import Tuple


def generate_path_by_uuid(
    base_path: str, file_extension: str, file_uuid: str, division: int
) -> str:
    """
    Create a filesystem path for a UUID by splitting it into directory structure.

    Args:
        base_path: Root directory where the path will be created
        file_extension: File extension including the dot (e.g., '.jpg')
        file_uuid: Unique identifier string to use for path generation
        division: Number of characters to use for the filename and to split the rest into directories

    Returns:
        str: The full generated path

    Raises:
        ValueError: If the UUID is too short for the specified division
        OSError: If there are issues creating the directories
    """

    @lru_cache(maxsize=128)
    def _split_uuid(uuid_str: str, split_at: int) -> Tuple[str, str]:
        """
        Split UUID into directory parts and filename part with caching.

        Args:
            uuid_str: The UUID string to split
            split_at: Number of characters to use for the filename part

        Returns:
            Tuple of (directory_structure, filename_part)
        """
        if len(uuid_str) < split_at * 2:
            raise ValueError(f"UUID must be at least {split_at * 2} characters long")

        filename_part = uuid_str[-split_at:]
        dirname_part = uuid_str[:-split_at]
        # Create directory structure by splitting remaining characters into 2-character chunks
        dir_structure = os.path.sep.join(
            dirname_part[i : i + 2] for i in range(0, len(dirname_part), 2)
        )
        return dir_structure, filename_part

    # Validate inputs
    if not file_extension.startswith("."):
        file_extension = f".{file_extension}"

    dir_structure, filename_part = _split_uuid(file_uuid, division)
    filename = f"{filename_part}{file_extension}"
    full_path = os.path.join(base_path, dir_structure, filename)

    # Create directories if they don't exist
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    return full_path


if __name__ == "__main__":
    full_path = generate_path_by_uuid(
        file_uuid="oooopppp",
        file_extension=".png",
        division=4,
        base_path="/storage/emulated/0",
    )
