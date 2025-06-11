from pathlib import Path
import zipfile


def create_zip(source_dir: Path, zip_path: Path) -> None:
    """Create a zip file from the contents of source_dir."""
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for file_path in source_dir.iterdir():
            zf.write(file_path, arcname=file_path.name)
