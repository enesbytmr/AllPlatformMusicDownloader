from pathlib import Path
import zipfile


def create_zip(source_dir: Path, zip_path: Path) -> None:
    """Create a zip file from the contents of source_dir."""
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for file_path in source_dir.iterdir():
            zf.write(file_path, arcname=file_path.name)


def zip_temp_directory(temp_dir: Path) -> Path:
    """Zip ``temp_dir`` and return the path to the created archive."""

    zip_path = temp_dir.with_suffix('.zip')
    create_zip(temp_dir, zip_path)
    return zip_path
