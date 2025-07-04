import os
import subprocess
import shutil
import platform
import sys
import json
from pathlib import Path
import importlib.util

def check_prerequisites():
    """Check if required dependencies and files exist."""
    # Check PyInstaller
    if importlib.util.find_spec("PyInstaller") is None:
        print("❌ Error: PyInstaller is not installed. Install it with: pip install pyinstaller")
        return False

    # Check main.py
    main_file = Path("main.py")
    if not main_file.exists():
        print(f"❌ Error: {main_file} does not exist in the project root.")
        return False

    # Check config.json
    config_file = Path("config.json")
    if not config_file.exists():
        print(f"⚠️ Warning: {config_file} does not exist. Version will be set to 'unknown'.")

    # Check icon file
    icon_path = Path("assets") / ("head.ico" if platform.system() == "Windows" else "head.png")
    if not icon_path.exists():
        print(f"❌ Error: Icon file '{icon_path}' does not exist.")
        return False

    # Check i18n directory
    i18n_dir = Path("i18n")
    if not i18n_dir.exists():
        print(f"⚠️ Warning: 'i18n' directory does not exist. Language files will not be included.")

    return True

def build_exe():
    """Build a cross-platform executable using PyInstaller."""
    # Verify prerequisites
    if not check_prerequisites():
        return False

    # Define paths
    project_root = Path.cwd()
    build_dir = project_root / "build"
    dist_dir = project_root / "dist"
    config_file = project_root / "config.json"
    icon_path = project_root / "assets" / ("head.ico" if platform.system() == "Windows" else "head.png")
    exe_name = f"End_of_Universe_v{get_version(config_file)}"
    spec_file = project_root / f"{exe_name}.spec"
    exe_path = dist_dir / (f"{exe_name}.exe" if platform.system() == "Windows" else exe_name)

    print("🚀 Starting build process...")

    # Clean previous build artifacts
    cleanup_build_files(build_dir, dist_dir, spec_file)

    # Prepare PyInstaller command
    pyinstaller_cmd = [
        sys.executable,  # Use the current Python executable to run PyInstaller
        "-m", "PyInstaller",  # Run PyInstaller as a module
        "--onefile",
        "--windowed",
        f"--name={exe_name}",
        "--clean",
        f"--icon={icon_path}",
    ]

    # Add assets and i18n directories
    data_dirs = [
        (project_root / "assets", "assets"),
        (project_root / "i18n", "i18n"),
        (project_root / "config.json", "."), 
    ]
    for src, dest in data_dirs:
        if src.exists():
            pyinstaller_cmd.extend(["--add-data", f"{src}{os.pathsep}{dest}"])
        else:
            print(f"⚠️ Warning: Directory '{src}' does not exist, skipping.")

    # Add main script
    pyinstaller_cmd.append("main.py")

    # macOS-specific options
    if platform.system() == "Darwin":
        pyinstaller_cmd.extend([
            "--osx-bundle-identifier", "com.yourcompany.endofuniverse",
            "--target-architecture", "universal2"
        ])

    try:
        print(f"📜 Build command: {' '.join(pyinstaller_cmd)}")

        # Run PyInstaller
        result = subprocess.run(
            pyinstaller_cmd,
            check=True,
            capture_output=True,
            text=True
        )

        # Log output
        if result.stdout:
            print("\n📜 Output:")
            print(result.stdout)
        if result.stderr:
            print("\n⚠️ Warnings/Errors:")
            print(result.stderr)

        # Verify executable
        if exe_path.exists():
            print(f"\n✅ Success! Executable created at: {exe_path}")
            return True
        else:
            raise FileNotFoundError(f"Failed to generate executable: {exe_path}")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        cleanup_build_files(build_dir, dist_dir, spec_file)
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        cleanup_build_files(build_dir, dist_dir, spec_file)
        return False

def get_version(config_file):
    """Read version from config.json."""
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get("version", "unknown")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"⚠️ Warning: Could not read version from {config_file}. Using 'unknown'. Error: {e}")
        return "unknown"

def cleanup_build_files(build_dir, dist_dir, spec_file):
    """Remove build artifacts."""
    print("\n🧹 Cleaning build artifacts...")
    for path in [build_dir, dist_dir, spec_file]:
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
                print(f"🗑️ Deleted directory: {path}")
            else:
                path.unlink(missing_ok=True)
                print(f"🗑️ Deleted file: {path}")

if __name__ == "__main__":
    success = build_exe()
    if not success:
        print("\n\033[31mBuild failed, cleaned up all generated files\033[0m")
        sys.exit(1)
    print("\n\033[32mBuild succeeded!\033[0m")
    sys.exit(0)