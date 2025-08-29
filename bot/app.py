import hikari                      # discord api
import lightbulb                   # slash command framework
import miru                        # component view framework
import os
from dotenv import load_dotenv

# load .env and validate variables
load_dotenv()
guild_id = os.environ.get("GUILD_ID")
if not guild_id:
    raise ValueError("GUILD_ID is not set")
discord_token = os.environ.get("DISCORD_TOKEN")
if not discord_token:
    raise ValueError("DISCORD_TOKEN is not set")

# create hikari bot, lightbulb client, and miru client
bot= hikari.GatewayBot(token=discord_token, logs="DEBUG")
lightbulb_client = lightbulb.client_from_app(bot, default_enabled_guilds=[int(guild_id)])
miru_client = miru.Client(bot)

# register miru for dependency injection
lightbulb_client.di.registry_for(
    lightbulb.di.Contexts.DEFAULT
    ).register_value(miru.Client, miru_client)

@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    # Load extensions
    await lightbulb_client.load_extensions("extensions.utils")
    await lightbulb_client.load_extensions("extensions.character")
    # Start clients
    #await miru_client.start()
    await lightbulb_client.start()

# hikari ping command
@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    if not event.is_human:
        return

    me = bot.get_me()
    if me.id in event.message.user_mentions_ids:
        await event.message.respond("Pong!")

@lightbulb_client.register()
class relaod(
    lightbulb.SlashCommand,
    name="reload",
    description="reload extensions"
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        try:
            await lightbulb_client.reload_extensions("extensions.character")
            await ctx.respond("Extensions reloaded successfully!")
        except Exception as e:
            await ctx.respond(f"Failed to reload extensions: {e}")

bot.run()
