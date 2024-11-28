import discord
from discord.ext import commands
from tinydb import TinyDB, Query

# Подключение к базе данных
db = TinyDB('game_data.json')
Player = Query()

# Инициализация бота
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Бот {bot.user} успешно подключен!')

# Команда для проверки текущих очков
@bot.command(name='очки')
async def get_score(ctx):
    user_id = str(ctx.author.id)
    user_data = db.search(Player.user_id == user_id)
    
    if user_data:  # Если пользователь найден в базе
        score = user_data[0]['score']
        await ctx.send(f"{ctx.author.name}, у тебя {score} очков!")
    else:  # Если пользователь отсутствует в базе
        await ctx.send(f"{ctx.author.name}, у тебя пока нет очков.")

# Команда для добавления очков
@bot.command(name='добавить_очки')
async def add_score(ctx, points: int):
    user_id = str(ctx.author.id)
    user_data = db.search(Player.user_id == user_id)
    
    if user_data:
        new_score = user_data[0]['score'] + points
        db.update({'score': new_score}, Player.user_id == user_id)
    else:
        db.insert({'user_id': user_id, 'username': ctx.author.name, 'score': points})

    await ctx.send(f"{ctx.author.name}, тебе добавлено {points} очков!")

# Команда для сброса очков
@bot.command(name='сбросить_очки')
async def reset_score(ctx):
    user_id = str(ctx.author.id)
    db.update({'score': 0}, Player.user_id == user_id)
    await ctx.send(f"{ctx.author.name}, твои очки сброшены!")
