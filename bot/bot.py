import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from dateBase import Database

intents = discord.Intents().all()

bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()


@bot.command(name='додати')
async def add_task(ctx, *task_name):
    db = Database('task.db')
    db.create_or_insert(' '.join(task_name))

    await ctx.send(f'Завдання {max(db.get_all_id())} додано: {" ".join(task_name)}')


@bot.command(name='всі_завдання')
async def list_tasks(ctx):
    db = Database('task.db')
    tasks = db.get_all_tasks()

    if not tasks:
        await ctx.send('Немає завдань.')
    else:
        tasks_list = "\n".join([f"{task[0]}. {task[1]} ({task[2]})" for task in tasks])
        await ctx.send(f'Завдання:\n{tasks_list}')


@bot.command(name='виконано')
async def mark_completed(ctx, task_id: int):
    db = Database('task.db')

    if task_id not in db.get_all_id():
        await ctx.send(f'Завдання з ідентифікатором {task_id} не існує.')
        return


@bot.command(name='редагувати')
async def edit_task(ctx, task_id: int, *, new_title: str):
    db = Database('task.db')

    if task_id not in db.get_all_id():
        await ctx.send(f'Завдання з ідентифікатором {task_id} не існує.')
        return

    success = db.edit_task_title(task_id, new_title)

    if success:
        await ctx.send(f'Завдання з ідентифікатором {task_id} відредаговано. Нова назва: {new_title}')
    else:
        await ctx.send('Виникла помилка при виконанні операції.')


@bot.command(name='видалити')
async def delete_task(ctx, task_id: int):
    db = Database('task.db')

    if task_id not in db.get_all_id():
        await ctx.send(f'Завдання з ідентифікатором {task_id} не існує.')
        return

    success = db.delete_task(task_id)

    if success:
        await ctx.send(f'Завдання з ідентифікатором {task_id} видалено.')
    else:
        await ctx.send('Виникла помилка при виконанні операції.')


bot.run(os.getenv('token'))
