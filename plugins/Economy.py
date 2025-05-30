def register(bot):
    user_balances = {}

    @bot.command()
    async def balance(ctx):
        user_id = str(ctx.author.id)
        balance = user_balances.get(user_id, 0)
        await ctx.send(f"Your balance is ${balance}")

    @bot.command()
    async def earn(ctx, amount: int):
        user_id = str(ctx.author.id)
        user_balances[user_id] = user_balances.get(user_id, 0) + amount
        await ctx.send(f"You earned ${amount}. New balance: ${user_balances[user_id]}")
