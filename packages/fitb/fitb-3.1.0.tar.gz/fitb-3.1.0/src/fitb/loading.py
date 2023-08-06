import logging

from .extension_point import ExtensionPoint

log = logging.getLogger()


def load_from_module(extension_point, module_name, extension_function_name='__extend__', propagate_exceptions=False):
    """Load an ExtensionPoint from a Python module.

    This imports a module and scans it for immediate sub-modules, i.e. those modules nested directly under the first
    module. It imports each sub-module and looks for a callable object by name (by default "__extend__"). If the
    callable is found, it's called with an `ExtensionPoint` as the only argument.

    This is primarily intended to load extensions from *namespace packages*, but it's not limited to them. Since
    namespace packages can be extended by different packages, this makes them useful for plugins.

    Args:
        extension_point: An `ExtensionPoint` instance to populate. This is what is passed to the extension callables.
        module_name: The name of the module to scan for sub-modules.
        extension_function_name: The name of the function/callable to look for in the scanned sub-modules.
        propagate_exceptions: Whether exceptions generated during importing and extension invocation should be
            propagated.

    Returns: The `ExtensionPoint` object passed as the first argument.
    """
    import importlib
    import pkgutil

    exception_signature = () if propagate_exceptions else (Exception,)

    module = importlib.import_module(module_name)

    for info in pkgutil.iter_modules(module.__path__):
        ext_module_name = f'{module_name}.{info.name}'
        try:
            ext_module = importlib.import_module(ext_module_name)
            ext_func = getattr(ext_module, extension_function_name, None)
            if ext_func is not None:
                ext_func(extension_point)
        except exception_signature:
            log.exception(f"Unable to load extension {ext_module_name}")

    return extension_point


def load_from_pkg_resources(namespace):
    """Discover ExtensionPoints using pkg_resources.

    This uses pkg_resources to scan the entry-points for `namespace`. Each dotted entrypoint name should have two parts.
    The first will be `namespace` and the second will be assumed to be the name of the entry point to which it belongs.

    Each discovered entry point should be a callable that takes a single argument of an ExtensionPoint. The extension
    should populate the ExtensionPoint appropriately, e.g. by calling `ExtensionPoint.add()`.

    Args:
        namespace: The pkg_resources namespace to scan.

    Returns: An iterable of ExtensionPoints.
    """
    import pkg_resources
    from stevedore import ExtensionManager

    for entry_point_name in pkg_resources.get_entry_map(namespace):
        toks = entry_point_name.split('.')
        if len(toks) == 1:
            # This happens for e.g. console_scripts
            continue

        # TODO: Do we need to extend for the case of an entry_point_name with more than two tokens? We could return a
        # tree of ExtensionPoint instead of just a flat mapping.

        assert toks[0] == namespace

        extension_point = ExtensionPoint(toks[1])

        manager = ExtensionManager(
            '.'.join(toks),
            on_load_failure_callback=_log_extension_loading_failure)

        for extension in manager:
            extension.plugin(extension_point)

        yield extension_point


def _log_extension_loading_failure(_mgr, extension_point, err):
    # We have to log at the `error` level here as opposed to, say, `info`
    # because logging isn't configure when we reach here. We need this infor to
    # print with the default logging settings.
    log.error('Plugin load failure: extension-point="%s", err="%s"',
              extension_point, err)
