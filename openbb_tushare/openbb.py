"""openbb_tushare OpenBB Platform extension."""
from pathlib import Path
from typing import List, Optional, Union

from openbb_core.app.static.app_factory import BaseApp as _BaseApp
from openbb_core.app.static.app_factory import create_app as _create_app
from openbb_core.app.static.package_builder import \
    PackageBuilder as _PackageBuilder

_this_dir = Path(__file__).parent.resolve()
_PackageBuilder(_this_dir).auto_build()


def build(
    modules: Optional[Union[str, List[str]]] = None,
    lint: bool = True,
    verbose: bool = False,
) -> None:
    """Build extension modules.

    Parameters
    ----------
    modules : Optional[List[str]], optional
        The modules to rebuild, by default None
        For example: "/news" or ["/news", "/crypto"]
        If None, all modules are rebuilt.
    lint : bool, optional
        Whether to lint the code, by default True
    verbose : bool, optional
        Enable/disable verbose mode
    """
    _PackageBuilder(_this_dir, lint, verbose).build(modules)


try:
    # pylint: disable=import-outside-toplevel
    from openbb_tushare.package.__extensions__ import Extensions as _Extensions

    obb: Union[_BaseApp, _Extensions] = _create_app(_Extensions)  # type: ignore
    sdk = obb
except (ImportError, ModuleNotFoundError):
    print("Failed to import extensions.")
    obb = sdk = _create_app()  # type: ignore
