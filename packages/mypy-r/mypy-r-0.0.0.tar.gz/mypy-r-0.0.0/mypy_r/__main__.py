import os
import sys

from mypy.__main__ import main as mypy_main

def main(x, stdout, stderr):
    root = '.'
    packages = {}

    for path, _, files in os.walk(root):

        if '__init__.py' in files:
            packages[path] = True

    for pkg_path in packages.keys():
        parent = pkg_path.rsplit('/', 1)[0]
        if parent in packages.keys():
            packages[pkg_path] = False

    package_roots = [pkg_path for (pkg_path, is_pkg_root) in packages.items() if is_pkg_root]

    cli_args = sys.argv.copy()

    for package in package_roots:
        pkg_path = package
        if package.startswith(f'{root}/'):
            pkg_path = package[len(f'{root}/'):]

        sys.argv = cli_args.copy()
        sys.argv.append(pkg_path)
        arg_str = ' '.join(sys.argv[1:])

        stdout.write(f'mypy {arg_str}\n')
        stdout.flush()
        mypy_main(x, stdout, stderr)

def console_script():
    main(None, sys.stdout, sys.stderr)

if __name__ == '__main__':
    main(None, sys.stdout, sys.stderr)
