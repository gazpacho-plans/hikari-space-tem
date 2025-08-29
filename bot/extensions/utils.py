import hikari                      # discord api
import lightbulb                   # slash command framework
import platform

loader = lightbulb.Loader()

# ping slash command
@loader.command
class ping(
    lightbulb.SlashCommand,
    name="ping",
    description="Ping the bot",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond("Pong! 🏓")

# bot info slash command
@loader.command
class botinfo(
    lightbulb.SlashCommand,
    name="botinfo",
    description="Get information about the bot",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        embed = hikari.Embed(title="Bot Information",)        
        embed.add_field("System", platform.system(), inline=True)
        embed.add_field("Python Version", platform.python_version(), inline=True)
        await ctx.respond(embed=embed)
        