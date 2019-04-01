plugins = []


def add_plugin(plugin):
    plugins.append(plugin)


def get_plugins():
    return tuple(plugins)
