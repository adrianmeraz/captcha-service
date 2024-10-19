from importlib.resources import files
from pathlib import Path

from py_aws_core.utils import import_all_package_modules

from src.layers.containers import Container
from src.layers.logs import get_logger

logger = get_logger()


def autowire_modules(package: str):
    modules = [fp for fp in files(package).iterdir() if all([fp.is_file, fp.name.endswith('.py'), not fp.name.startswith('__')])]
    imports = [f'{package}.{Path(fp.name).stem}' for fp in modules]
    Container().wire(modules=imports)
    logger.info(f'Autowired modules: {', '.join(imports)}')


autowire_modules(package='src.lambdas')

import_all_package_modules(__name__)  # Registers routes of lambda handlers
