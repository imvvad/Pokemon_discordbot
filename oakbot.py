import os
import csv
import discord
import pandas as pd
from discord.ui import Select, Modal, InputText
from discord.ext import commands


class DifficultySelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="⭐︎6"),
        ]
        super().__init__(
            placeholder="レイド難易度を選択するのだ",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        modal = PokemonNameModal(title="レイドボスポケモン検索")
        await interaction.response.send_modal(modal)


class PokemonNameModal(Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="調べたいポケモンの名前を入力するのだ!"))

    async def callback(self, interaction: discord.Interaction):
        # print(f"Submitted !!!")
        # print(f"Self Instance: {self}")
        # print(f"Entered Pokemon name: {self.children[0]}")
        pokemon_name = self.children[0].value.lower()
        # print(f"Entered Pokemon name: {pokemon_name}")
        # info = pokemon_info.get(pokemon_name, None)
        info = find_pokemon_info(pokemon_name)
        if info:
            print(f"検索対象： {pokemon_name} \n検索結果： {info}")
            await interaction.response.send_message(
                f"検索対象： {pokemon_name} \n検索結果：{info}"
            )
        else:
            print(f"pokemon not found.")
            await interaction.response.send_message("該当するポケモンが見つからなかったのだ")

    # pokemon_name = InputText(label='Enter Pokemon Name!')

    # async def on_submit(self, interaction: discord.Interaction):
    #     pokemon_name = self.pokemon_name.value.lower()
    #     info = pokemon_info.get(pokemon_name, None)
    #     if info:
    #         await interaction.response.send_message(f'Information for {pokemon_name}: {info}')

    #     else:
    #         await interaction.response.send_message(f'Pokemon not found.')


def find_pokemon_info(pokemon_name):
    refined_pokemon_info = ""
    for key, value in pokemon_info.items():
        if pokemon_name.lower() in key.lower():          
            refined_pokemon_info += f"{value}"
            print(f"added {value}")
            # refined_pokemon_info = '\n'.join(refined_pokemon_info, f"{key}: {value}")
    if refined_pokemon_info:
        refined_pokemon_info = refined_pokemon_info.replace(', ','\n').replace('{','\n').replace('}','').replace('\'','').replace('Name:','【ポケモン名】\n').replace('テラスタイプ:','【テラスタイプ】\n').replace('対戦時限定技:','【当レイド限定】\n').replace('技:','【技】\n').replace('特性:','【特性】\n').replace('難易度:','【難易度】\n')
        # print(f"refined output : {refined_pokemon_info}")
        return refined_pokemon_info
    else:
        return None


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
async def hello(ctx):
    await ctx.respond("Hello!")


@bot.slash_command(
    name="raid",
    # description="Start a raid by choosing a difficulty and entering a pokemon name.",
    description="レイド相手のポケモンのデータをチェックできるのだ",
    guild_ids=GUILD_IDS,
)
async def raid(ctx):
    print("/raid command called")
    view = discord.ui.View()
    view.add_item(DifficultySelect())
    # await ctx.respond("Select the raid difficulty:", view=view)
    await ctx.respond("難易度を選択するのだ:", view=view)

def load_pokemon_raid_data(filename):
    pokemon_data = {}
    try:
        with open(filename, newline="", encoding="utf-8") as csvfile:
            render = csv.DictReader(csvfile)
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
    return pokemon_data


pokemon_info = load_pokemon_raid_data("pokemon_6_star_raid_info_updated.csv")


token = os.getenv("OAK_BOT_TOKEN")
bot.run(token)
