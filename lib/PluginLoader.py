import os
import importlib.util
import json

class PluginLoader:
    def __init__(self, plugin_dir, config_path):
        self.plugin_dir = plugin_dir
        self.config_path = config_path
        self.SKIP_MODULES = {"CommandHandler", "__init__"}

    def _generate_config(self):
        if not os.path.exists(self.config_path):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump({}, f, indent=4)

        with open(self.config_path, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = {}

        current_plugins = {
            file[:-3]
            for file in os.listdir(self.plugin_dir)
            if file.endswith(".py") and file[:-3] not in self.SKIP_MODULES
        }

        removed = [key for key in config if key not in current_plugins]
        for key in removed:
            print(f"[PluginLoader] Removing orphaned plugin entry: {key}")
            del config[key]

        for name in current_plugins:
            if name not in config:
                config[name] = {"enabled": True}

        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)

    def load_plugins(self):
        self._generate_config()

        with open(self.config_path, "r") as f:
            config = json.load(f)

        plugins = []

        for file in os.listdir(self.plugin_dir):
            if file.endswith(".py"):
                name = file[:-3]
                if name in self.SKIP_MODULES:
                    continue

                if config.get(name, {}).get("enabled", False):
                    full_path = os.path.join(self.plugin_dir, file)
                    spec = importlib.util.spec_from_file_location(name, full_path)
                    module = importlib.util.module_from_spec(spec)
                    try:
                        spec.loader.exec_module(module)
                        plugins.append(module)
                    except Exception as e:
                        print(f"[PluginLoader] Failed to load plugin {name}: {e}")

        return plugins
