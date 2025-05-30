def register(bot, plugins):
    for plugin in plugins:
        try:
            plugin.register(bot)
        except Exception as e:
            print(f"[CommandHandler] Failed to register plugin {plugin.__name__}: {e}")
