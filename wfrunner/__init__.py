import argparse
import glob
import importlib
import os

from .util import _log_level, get_main_logger

__version__ = "0.0.1"
_package_name = "wfrunner"


def get_components():
    """Find a list of workflow command scripts."""
    logger = get_main_logger(_package_name)
    path = os.path.dirname(os.path.abspath(__file__))
    components = list()
    for fname in glob.glob(os.path.join(path, "*.py")):
        name = os.path.splitext(os.path.basename(fname))[0]
        if name in ("__init__", "util"):
            continue

        # leniently attempt to import module
        try:
            mod = importlib.import_module(f"{_package_name}.{name}")
        except ModuleNotFoundError as e:
            # if imports cannot be satisifed, refuse to add the component
            # rather than exploding
            logger.warn(f"Could not load {name} due to missing module {e.name}")
            continue

        # if theres a main() and and argparser() thats good enough for us.
        try:
            req = "main", "argparser"
            if all(callable(getattr(mod, x)) for x in req):
                components.append(name)
        except Exception:
            pass
    return components


def cli():
    """Run workflow entry points."""
    parser = argparse.ArgumentParser(
        'wf-glue',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-v', '--version', action='version',
        version='%(prog)s {}'.format(__version__))

    subparsers = parser.add_subparsers(
        title='workflows', description='valid commands',
        help='choose a workflow to run', dest='command')
    subparsers.required = True

    # all component demos, plus some others
    components = [
        f'{_package_name}.{comp}' for comp in get_components()]
    for module in components:
        mod = importlib.import_module(module)
        p = subparsers.add_parser(
            module.split(".")[-1], parents=[mod.argparser()])
        p.set_defaults(func=mod.main)

    logger = get_main_logger(_package_name)
    args = parser.parse_args()

    logger.info("Starting entrypoint.")
    args.func(args)