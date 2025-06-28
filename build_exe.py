import os
import subprocess
import shutil
import platform
import sys
from pathlib import Path

def build_exe():
    # 定义目录和文件路径
    build_dir = "build"
    dist_dir = "dist"
    exe_name = "NumberConverter_v1.0.0"
    spec_file = f"{exe_name}.spec"
    exe_path = None
    if platform.system() == "Windows":
        exe_path = Path(dist_dir) / f"{exe_name}.exe"
    else:
        exe_path = Path(dist_dir) / exe_name

    # 确定图标路径（跨平台处理）
    icon_path = "assets/head.ico" if platform.system() == "Windows" else "assets/head.png"

    # 获取当前工作目录
    cwd = Path.cwd()
    
    # 检查图标文件是否存在
    icon_full_path = cwd / icon_path
    if not icon_full_path.exists():
        print(f"❌ Error: icon file '{icon_path}' doesn't exist.")
        print("Please make sure to create an assets folder in the project root and place the head.ico file inside.")
        return False
    
    print("Cleaning...")
    # 清理旧构建
    for path in [build_dir, dist_dir, spec_file]:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            print(f"Delete: {path}")

    print("\nStart building EXE file...")
    
    # 构建命令（跨平台）
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        f"--name={exe_name}",
        "--clean",
        "number_converter.py",
        f"--icon={icon_full_path}",
    ]

    # 添加资源文件（确保运行时能访问 assets 目录）
    if platform.system() == "Windows":
        pyinstaller_cmd += ["--add-data", f"{icon_path};assets"]
    else:
        pyinstaller_cmd += ["--add-data", f"{icon_path}:assets"]
    
    # macOS 特定调整
    if platform.system() == "Darwin":
        pyinstaller_cmd.append("--osx-bundle-identifier")
        pyinstaller_cmd.append("com.yourcompany.numberconverter")
    
    try:
        print("Build command:", " ".join(pyinstaller_cmd))
        
        # 运行构建命令
        result = subprocess.run(
            pyinstaller_cmd,
            check=True,
            capture_output=True,
            text=True
        )
        
        # 打印构建输出
        if result.stdout:
            print("\nOutput:")
            print(result.stdout)
        if result.stderr:
            print("\nError:")
            print(result.stderr)
        
        # 检查是否成功生成可执行文件
        if exe_path.exists():
            print(f"\n✅ Success! exe-path: {exe_path}")
            return True
        else:
            raise FileNotFoundError(f"Fail to generate exe-file: {exe_path}")
            
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"\n❌ Build failed: {str(e)}")

        # 清理生成的文件
        print("\nCleaning...")
        for path in [build_dir, dist_dir, spec_file]:
            path_obj = Path(path)
            if path_obj.exists():
                if path_obj.is_dir():
                    shutil.rmtree(path_obj)
                    print(f"Delete: {path}")
                else:
                    path_obj.unlink()
                    print(f"Delete: {path}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False




if __name__ == "__main__":
    if not build_exe():
        print("\n\033[31mBuild failed, cleaned up all generated files\033[0m")
        sys.exit(1)
    else:
        print("\n\033[32mBuild succeeded!\033[0m")
        sys.exit(0)