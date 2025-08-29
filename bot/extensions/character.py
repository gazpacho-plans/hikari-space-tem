import hikari                      # discord api
import lightbulb                   # slash command framework
import miru                        # component view framework
import json
from typing import Optional

# centralize data and prepare for db
class CharacterData:
    def __init__(self):
        self.name: Optional[str] = None
        self.faction: Optional[str] = None
        self.profession: Optional[str] = None
        self.user_id: Optional[int] = None
    
    def is_complete(self) -> bool: # check if data is filled
        return all([self.name, self.faction, self.profession, self.user_id])

    def to_dict(self) -> dict: # convert to dict
        return {
            "name": self.name,
            "faction": self.faction,
            "profession": self.profession,
            "user_id": self.user_id,
        }
    def reset(self):
        self.name = None
        self.faction = None
        self.profession = None
        self.user_id = None

# create-character command
loader = lightbulb.Loader()
@loader.command
class CreateCharacter(
    lightbulb.SlashCommand,
    name="create-character",
    description="Create your Councilor character",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, miru_client: miru.Client) -> None:
        # instance and id CharacterData
        data = CharacterData()
        data.user_id = ctx.member.id

        # load and start modal
        modal = CharacterModal(data)
        builder = modal.build_response(miru_client)
        await builder.create_modal_response(ctx.interaction)
        miru_client.start_modal(modal)
        
        # Wait for user to submit
        '''await modal.wait()
        if modal.timeout:
            await ctx.followup.create("No response: Timed out.")
            return''' # might not work
        
class CharacterModal(miru.Modal, title="Create Your Councilor"):
    def __init__(self, data: CharacterData):
        super().__init__()
        self.data = data

    # Collect name
    name = miru.TextInput(
        label="Character Name",
        placeholder="Enter your councilor's name",
        required=True
    )
    async def callback(self, ctx: miru.ModalContext) -> None:
        self.data.name = self.name.value
        await ctx.respond(f"**{self.data.name}** is looking to join a faction")

        # start faction select

'''
TODO
CHARACTER CREATION FLOW:
hikri embed or miru view
miru textSelect
for both faction and profession select (subclass templates?)

CHARACTER SHEET:
miru menu to connect to mission asignment flow

DATABASE:
figure it out
'''