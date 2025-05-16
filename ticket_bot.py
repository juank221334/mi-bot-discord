import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot listo como {bot.user}')

@bot.slash_command(name="ticket", description="Crear un ticket para unirte al clan, staff o como aliado")
async def ticket(ctx):
    embed = discord.Embed(
        title="¿Qué deseas hacer?",
        description="Selecciona una opción del menú para crear tu ticket.",
        color=0x00ffcc
    )
    view = TicketView()
    await ctx.respond(embed=embed, view=view)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Select(
            placeholder="Selecciona una opción",
            options=[
                discord.SelectOption(label="Join Clan", description="Unirte al clan", emoji="🎯"),
                discord.SelectOption(label="Join Staff", description="Postularte para staff", emoji="👥"),
                discord.SelectOption(label="Ally", description="Alianza con el clan", emoji="🤝"),
            ],
            custom_id="ticket_select"
        ))

@bot.event
async def on_socket_response(payload):
    if payload.get("t") == "INTERACTION_CREATE":
        data = payload["d"]
        if data["data"]["component_type"] == 3:
            selected = data["data"]["values"][0]
            user = data["member"]["user"]["id"]
            guild_id = data["guild_id"]
            channel_name = f"{selected.lower().replace(' ', '-')}-{user}"
            guild = bot.get_guild(int(guild_id))
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.get_member(int(user)): discord.PermissionOverwrite(read_messages=True)
            }
            channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)
            await channel.send(f"Hola <@{user}>, has creado un ticket para **{selected}**. ¡El equipo te atenderá pronto!")
