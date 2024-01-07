import random, json
from aiogram import *
from aiogram.filters import *
from aiogram.types import *
from mydata import *


bot = Bot(token=TOKEN)
dp = Dispatcher()

    
def update_data(data: dict, name: str):
    with open("gamers.json", "w") as f:
        users[name] = data
        json.dump(users, f)


        
def get_data():
    with open("gamers.json", "r") as f:
        users = json.load(f)
        return users

    
def get_user(message: Message):
    name = message.from_user.username
    return get_data()[name]


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    name = message.from_user.username
    if name not in users:
        user = {"is_game":False,
                "game":0,
                "wins":0,
                "dream_digit":0,
                "attempts": 10}
        update_data(user, name)
        print(user, "start")
    else:
        user = get_user(message)
    if user["is_game"]:
        await message.answer("""Ву уже в игре!""")
        return 0
    user["game"] += 1
    user["is_game"] = True
    user["dream_digit"] = random.randint(1, 100)
    user["attempts"] = 10
    update_data(user, name)
    await message.answer("""Давай сыграем в угадай число!
                         
я загадал число от 1 до 100
попробуй его отгадать!
                         

если хочешь выйти из игры напиши /cancel""")
    


@dp.message(Command(commands=["statistik"]))
async def process_statistik_command(message:Message):
    users = get_data()
    sp = [f"{i} - {j['wins']} побед {j['game']} всего сыгранно" for i, j in users.items()]
    await message.answer("\n".join(sp))
@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer("""доступные команды:
/start - начать игру
/cancel - выйти из игры
/statistik - ваша статистика""")
    

@dp.message(Command(commands=["cancel"]))
async def process_cancel_command(message: Message):
    user = get_user(message)
    if not user["is_game"]:
        await message.answer("Вы не начинали игру")
        return 0
    user["is_game"] = False
    update_data(user, message.from_user.username)
    await message.answer(f"""Вы вышли из игры :(
загаданное число: {user['dream_digit']}
Если хотите еще поиграть введите /start :)""")
    


@dp.message()
async def process_echo_message(message:Message):
    try:
        name = message.from_user.username
        user = get_user(message)
        text = int((message.text))
        
    except:
        await message.answer(text="""сообщение должно быть числом или коммандой""")
        return 0


    
    if not user["is_game"]:
        return 0

    
    elif user["attempts"] == 0:
        user["is_game"] = False
        await message.answer(text=f"""Попытки кончились, вы проиграли!
Загаданное число: {user["dream_digit"]}
если хотите поиграть еще, то набирайте комманду /start :)""")
        user["is_game"] = False

        
    elif text < user["dream_digit"]:
        user["attempts"] -= 1
        await message.answer(text=f"""Загаданное число больше!
- 1 попытка
осталось: {user["attempts"]}""")

        
    elif text > user["dream_digit"]:
        user["attempts"] -= 1
        await message.answer(text=f"""Загаданное число меньше!
- 1 попытка
осталось: {user["attempts"]}""")

        
    elif text == user["dream_digit"]:
        user["is_game"] = False
        user["wins"] += 1
        await message.reply(text=f"""ВЫ УГАДАЛИ!!!

Загаданное число: {user["dream_digit"]}
Всего попыток осталось: {user["attempts"]}""")

        
    update_data(user, name)

    
users = get_data()
dp.run_polling(bot)
