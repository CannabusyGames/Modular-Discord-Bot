def register(bot):
    @bot.command()
    async def greet(ctx):
        await ctx.send("Hello! I'm your chat companion.")
