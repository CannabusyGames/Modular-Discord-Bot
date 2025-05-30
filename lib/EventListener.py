import json
import asyncio
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVENT_REQUESTS_PATH = os.path.join(BASE_DIR, "event_requests.json")
PLUGINS_CONFIG_PATH = os.path.join(BASE_DIR, "..", "bin", "plugins.json")

async def handle_events(bot):
    # Clear stale requests
    with open(EVENT_REQUESTS_PATH, "w") as f:
        f.write("")

    while True:
        await asyncio.sleep(2)

        if not os.path.exists(EVENT_REQUESTS_PATH):
            continue

        try:
            with open(EVENT_REQUESTS_PATH, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    continue

            if not data:
                continue

            action = data.get("action")

            if action == "stop":
                print("Shutting down bot via event listener...")
                await bot.close()
                break

            elif action == "update_plugin_state":
                plugin = data.get("plugin")
                enabled = data.get("enabled")

                with open(PLUGINS_CONFIG_PATH, "r") as f:
                    config = json.load(f)

                if plugin in config:
                    config[plugin]["enabled"] = enabled

                    with open(PLUGINS_CONFIG_PATH, "w") as f:
                        json.dump(config, f, indent=4)

                    print(f"Updated plugin '{plugin}' state to {enabled}")

            with open(EVENT_REQUESTS_PATH, "w") as f:
                f.write("")

        except Exception as e:
            print(f"[EventListener Error]: {e}")
