import os
import shutil
import subprocess
from argparse import ArgumentParser


def configure(version):
    autodesk_dir = os.environ.get("MAYA_LOCATION", "C:/Program Files/Autodesk")
    print(autodesk_dir)
    if not os.path.isdir(autodesk_dir):
        raise ValueError("Invalid Autodesk directory: {0}".format(autodesk_dir))
    cmake = subprocess.run(['cmake',
                            '.',
                            '-B'
                            './build',
                            f'-DMAYA_LOCATION={autodesk_dir}',
                            f'-DMAYA_VERSION={version}'])
    return cmake.returncode


def build(*args):
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--ver", default=2020, type=int, help="Maya version")
    args = arg_parser.parse_args(*args)
    if os.path.isdir("./build"):
        print("Removing old build...")
        shutil.rmtree("./build")
    err = configure(args.ver)
    print(f"Building for Maya {args.ver}...")
    if err:
        return
    cmake_build = subprocess.run(['cmake', '--build', './build'])
    return cmake_build.returncode


if __name__ == "__main__":
    build(os.sys.argv[1:])
