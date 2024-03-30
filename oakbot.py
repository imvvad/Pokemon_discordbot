import os
import csv
import discord
from discord import Option
from discord.ui import Select, Modal, InputText
from discord.ext import commands

# class DifficultySelect(Select):
#     def __init__(self):
#         options = [
#             discord.SelectOption(label="⭐︎6"),
#         ]
#         super().__init__(
#             placeholder="レイド難易度を選択するのだ",
#             min_values=1,
#             max_values=1,
#             options=options,
#         )

#     async def callback(self, interaction: discord.Interaction):
#         self.view.disable_all_items()
#         modal = PokemonNameModal(title="レイドボスポケモン検索")
#         await interaction.response.send_modal(modal)

# class PokemonNameModal(Modal):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.add_item(InputText(label="調べたいポケモンの名前を入力するのだ!"))

#     async def callback(self, interaction: discord.Interaction):
#         pokemon_name = self.children[0].value.lower()
#         info = find_pokemon_info(pokemon_name)
#         if info:
#             print(f"検索対象： {pokemon_name} \n検索結果： {info}")
#             await interaction.response.send_message(
#                 f"検索対象： {pokemon_name} \n検索結果：{info}"
#             )
#         else:
#             print(f"pokemon not found.")
#             await interaction.response.send_message("該当するポケモンが見つからなかったのだ")

def find_pokemon_info(pokemon_name):
    refined_pokemon_info = ""
    for key, value in pokemon_info.items():
        if pokemon_name.lower() in key.lower():          
            refined_pokemon_info += f"{value}"
    if refined_pokemon_info:      
        return refine_output(refined_pokemon_info,pokemon_info_keys)  
    else:
        return None

def refine_output(pokemon_info,pokemon_info_keys):
    refined_pokemon_info = ""
    print(f"keys:{pokemon_info_keys}")
    refined_pokemon_info = pokemon_info.replace(', ','\n').replace('{','\n').replace('}','\n ---------------------------------------------\n').replace('\'','').replace('対戦時限定技:','【当難易度(☆6)でのみ使用】\n')
    for key in pokemon_info_keys:
        refined_pokemon_info = refined_pokemon_info.replace(f"{key}:",f"【{key}】\n")
    return refined_pokemon_info

intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True

bot = discord.Bot(intents=intents)
GUILD_IDS = [1137084951708319774]

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    # guild_id = discord.Object(id="1137084951708319774")
    # await bot.sync_commands(guild=guild_id)

@bot.slash_command(name="hello", description="Responds with Hello!")
async def hello(
    ctx: discord.ApplicationContext,
):
    await ctx.respond("Hello!")

@bot.slash_command(
    name="raid",
    # description="Start a raid by choosing a difficulty and entering a pokemon name.",
    description="レイド相手のポケモンのデータをチェックできるのだ",
    guild_ids=GUILD_IDS,
)
async def raid(
    ctx: discord.ApplicationContext,
    pokename: Option(str, required=True, description="検索したいポケモンの名前を入力するのだ"),
    #difficulty: Option(str, required=Flase, description="レイドの難易度を入力するのだ")
):
    print(f"/raid command called inputs:{pokename}")
    # view = discord.ui.View()
    # view.add_item(DifficultySelect())
    # await ctx.respond("Select the raid difficulty:", view=view)
    # await ctx.respond("難易度を選択するのだ:", view=view)
    input_pokemon_name = pokename
    info = find_pokemon_info(input_pokemon_name)
    if info:
        print(f"検索対象： {input_pokemon_name} \n検索結果： {info}")
        await ctx.response.send_message(
            f"検索対象： {input_pokemon_name} \n検索結果：{info}"
        )
    else:
        print(f"pokemon not found.")
        await ctx.response.send_message("該当するポケモンが見つからなかったのだ")

def load_pokemon_raid_data(filename):
    pokemon_data = {}
    try:
        with open(filename, newline="", encoding="utf-8") as csvfile:
            render = csv.DictReader(csvfile)
            info_keys = render.fieldnames
            for row in render:
                try:
                    pokemon_name = row["Name"].lower()
                    pokemon_data[pokemon_name] = row
                except KeyError as e:
                    print(f"KeyError: {e} not found in row: {row}")
                    continue
    except FileNotFoundError:
        print(f"file not found: {e}")
    #print(f"Loaded{len(pokemon_data)} Pokemon. Details: {pokemon_data}")
    return pokemon_data, info_keys

pokemon_info, pokemon_info_keys = load_pokemon_raid_data("pokemon_6_star_raid_info_updated.csv")

token = os.getenv("OAK_BOT_TOKEN")
bot.run(token)