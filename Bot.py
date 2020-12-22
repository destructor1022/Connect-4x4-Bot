# Work with Python 3.6
import io
import discord
from PIL import Image, ImageDraw, ImageFont
from Board import Board

TOKEN = 'Nzg2NjU0OTkyNTQ3MDUzNTkw.X9JjjQ.RUMEFuoa0KnIfWRapG4wuebyOAA'

client = discord.Client()
player_count = 0
game = Board()
current_color = "Green"


def check_start_cond():
    if game.get_player_count() != 4:
        return False

    return True


def draw_piece(image, front, row, column, color):
    if front == 1:
        image.ellipse((125 * row - 25 + 125, 125 * (6 - column), 100 + 125 * row - 25 + 125, 100 + 125 * (6 - column)),
                      fill=color)
    else:
        image.ellipse((125 * row + 125, 125 * (6 - column), 100 + 125 * row + 125, 100 + 125 * (6 - column)),
                      fill=color)


@client.event
async def on_message(message):
    global player_count
    global game
    global current_color

    if message.content.startswith('^join'):
        player_count += 1
        game.add_player(message.author.id, player_count)
        await message.channel.send(game.color_to_players[game.color_order[player_count - 1]].mention + " is " + game.color_order[player_count - 1])

    if message.content.startswith('^draw'):
        txt = Image.new('RGB', (1000, 1000), (94, 174, 179))
        draw = ImageDraw.Draw(txt)
        for deep in range(2):
            for column in range(7):
                for row in range(6):
                    draw_piece(draw, deep, column, row, game.convert_color(game.board[deep][column][row]))
        with io.BytesIO() as image_binary:
            txt.save(image_binary, 'PNG')
            image_binary.seek(0)
            await message.channel.send(file=discord.File(fp=image_binary, filename='image.png'))

    if message.content.startswith("^drop"):
        word = message.content.split(' ', 2)
        if word[1] == "front" or word[1] == "back" or (word[1] == "double" and game.doubles_used[current_color] < 2):
            if 8 > int(word[2]) > 0:
                if game.id_player(current_color) == message.author.id:
                    game.drop(word[1], int(word[2]) - 1, current_color)
                    current_color = game.next_color(current_color)
                    await message.channel.send("^draw")
                    await message.channel.send("It is now " + game.mention_player(current_color) + "'s turn")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
