must create a .env to store credentials. 
DISCORD_TOKEN=
GUILD_ID=
OWNER_ID=

control panel is used for sending event requests and toggling plugins.

adding features is as simple as writing a stateless module and tossing it in the plugins folder, plugins are automatically registered and unregistered based on presence, and toggled based on state in plugins.json.
