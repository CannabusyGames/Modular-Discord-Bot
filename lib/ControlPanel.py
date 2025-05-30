import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton,
    QTabWidget, QLabel
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGINS_CONFIG_PATH = os.path.join(BASE_DIR, "..", "bin", "plugins.json")
EVENT_REQUESTS_PATH = os.path.join(BASE_DIR, "event_requests.json")

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DealerBot Control Panel")
        self.setFixedSize(500, 500)

        self.tabs = QTabWidget()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tabs)

        self.init_plugin_tab()
        self.init_placeholder_tabs()

    def init_plugin_tab(self):
        plugin_tab = QWidget()
        layout = QVBoxLayout()
        plugin_tab.setLayout(layout)

        self.checkboxes = {}
        SKIP_PLUGINS = {"CommandHandler", "__init__"}

        with open(PLUGINS_CONFIG_PATH, "r") as f:
            config = json.load(f)

        for plugin, settings in config.items():
            if plugin in SKIP_PLUGINS:
                continue

            cb = QCheckBox(plugin)
            cb.setChecked(settings.get("enabled", False))
            cb.stateChanged.connect(lambda state, p=plugin: self.toggle_plugin(p, state))
            self.checkboxes[plugin] = cb
            layout.addWidget(cb)

        stop_button = QPushButton("Stop Bot")
        stop_button.clicked.connect(self.stop_bot)
        layout.addWidget(stop_button)

        self.tabs.addTab(plugin_tab, "Plugins")

    def init_placeholder_tabs(self):
        stats_tab = QWidget()
        stats_layout = QVBoxLayout()
        stats_layout.addWidget(QLabel("Bot Statistics Placeholder"))
        stats_tab.setLayout(stats_layout)
        self.tabs.addTab(stats_tab, "Stats")

        economy_tab = QWidget()
        economy_layout = QVBoxLayout()
        economy_layout.addWidget(QLabel("Economy Data Placeholder"))
        economy_tab.setLayout(economy_layout)
        self.tabs.addTab(economy_tab, "Economy")

    def toggle_plugin(self, plugin, state):
        event = {
            "action": "update_plugin_state",
            "plugin": plugin,
            "enabled": bool(state)
        }
        with open(EVENT_REQUESTS_PATH, "w") as f:
            json.dump(event, f)
        print(f"Toggle request for {plugin} to {bool(state)} sent.")

    def stop_bot(self):
        with open(EVENT_REQUESTS_PATH, "w") as f:
            json.dump({"action": "stop"}, f)
        print("Stop request sent.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ControlPanel()
    window.show()
    sys.exit(app.exec_())
