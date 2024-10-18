from py_aws_core.utils import import_all_package_modules
from src.layers.containers import Container
from importlib.resources import files
from pathlib import Path

import_all_package_modules(__name__)  # Registers routes of lambda handlers


def wire_all_modules_in_package(package: str):
    container = Container()
    f = files(package)
    modules = [fp for fp in f.iterdir() if fp.is_file and fp.name.endswith('.py') and not fp.name.startswith('__')]
    imports = [f'{package}.{Path(fp.name).stem}' for fp in modules]
    container.wire(modules=imports)


wire_all_modules_in_package('src.lambdas')
