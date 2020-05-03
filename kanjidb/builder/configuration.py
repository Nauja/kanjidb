__all__ = ["Configuration"]
import os
import yaml
from kanjidb import loader


DEFAULT_PLUGINS = ["kanjistream", "kanjidic2", "jsonwriter"]

DEFAULT_CONFIG_YML = "config.yml"


class Configuration:
    def __init__(self, *, targets, output=None, verbose=None):
        self.run = []
        self.targets = targets
        self.output = output
        self.verbose = verbose

    def template_config(self):
        """Build the default configuration.

        This is for first use of KanjiDB to initialize
        a YAML configuration file.

        Generate a configuration with all default parameters
        for default active plugins (see `DEFAULT_PLUGINS`).

        :return: default JSON config dict
        """
        modules = loader.load_plugin_modules(DEFAULT_PLUGINS)

        return {
            "run": [{_: modules[_].Plugin().template_config} for _ in DEFAULT_PLUGINS]
        }

    def load(self, stream=None, *, default=DEFAULT_CONFIG_YML):
        """Load configuration from YAML input.

        :param stream: filelike or str object
        :param default: default filename
        """
        # Filelike object
        if hasattr(stream, "read"):
            config = yaml.safe_load(stream)
        # If invalid filename
        elif not os.path.isfile(stream):
            if not default:
                raise FileNotFoundError(stream)

            # Generate configuration file for first time
            config = self.template_config()
            with open(default, "w+") as f:
                yaml.safe_dump(config, stream=f)
        # If valid filename
        else:
            with open(stream, "r") as f:
                config = yaml.safe_load(f)

        self.run = self._load_steps(config["run"])

        print("Configuration loaded")

    def _load_steps(self, steps):
        result = []

        for step in steps:
            modules = loader.load_plugin_modules(step.keys())
            for name, config in step.items():
                plugin = modules[name].Plugin()
                result.append(plugin)

                c = plugin.template_config
                c.update(plugin.required_config)
                c.update(config)

                plugin.configure(global_config=self, plugin_config=c)

        return result
