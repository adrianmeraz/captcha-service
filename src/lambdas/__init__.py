from py_aws_core.utils import import_all_package_modules

from src.layers.containers import Container


Container().wire(packages=[__package__])  # Auto-wires all modules under package
import_all_package_modules(__package__)   # Registers routes of lambda handlers
