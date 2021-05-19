from requests import get
from discord import Client, File
from discord import utils
from discord.message import Message
from discord.raw_models import RawReactionActionEvent
from random import choice
from re import findall, match  # from playsound import playsound
from youtube import allVideos
from fuzzywuzzy.fuzz import ratio


def isOneEl(l: list, limit: int) -> bool:
    ct = 0
    for i in l[::-1]:
        if i == l[-1]:
            ct += 1
        else:
            break
    if ct == limit:
        return True
    else:
        return False


def valcursed(v):
    r = get('https://www.cbr-xml-daily.ru/daily_json.js')
    data = r.json()
    return data['Valute'][v]['Value']


class Client_(Client):
    spam = []
    muted_channels_list = ['контакты', 'правила']
    text_channel_list = []
    videos_list = []
    spamLimit = 4
    commands = ['!бот', "!команды", "!лого"]
    question_message_id = 813751244467470336
    roles = {
        'админ': 813123398656983090,
        'участник': 813750101968683008
    }

    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)
        try:
            if findall(r'Message id=\d+', str(message)) == [f'Message id={self.question_message_id}']:
                await message.channel.send(f'У пользователя {member} есть вопрос!')  # playsound('gs.mp3')
        except KeyError:
            print("[ERROR] role doesn't exist")
        except Exception as e:
            print(f"[ERROR] {repr(e)}")

    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)
        try:
            if findall(r"author=<User id=\d+ name='Myshiak\.su' discriminator='1940' bot=False>", str(message)) == ["author=<User id=699534617295716363 name='Myshiak.su' discriminator='1940' bot=False>"]:
                await message.add_reaction('logotype:813751137709719633')
            else:
                if findall(r'Message id=\d+', str(message)) == [f'Message id={self.question_message_id}']:
                    await message.channel.send(f'У пользователя {member} исчез вопрос!')
        except KeyError:
            print("[ERROR] role doesn't exist")
        except Exception as e:
            print(f"[ERROR] {repr(e)}")

    async def on_ready(self):
        for guild in self.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel.name)
        print('[INFO] Channel list is got')
        print(f'[INFO] logged in as @{self.user}')

    async def on_member_join(self, member):
        print(self.user)
        await member.send(f'Добро пожаловать в наш сервер, {member}! Gatgwenay emesna szergbjergte, {member}!')

    async def on_message(self, message: Message):
        author = message.author
        content: str = message.content
        print(f'[MESSAGE] Content: {content}\nAuthor: {author}\n|')
        if author == Client().user:
            return
        if content.lower() == "!бот":
            await message.channel.send(choice(['Да / Hes', "Ага / Ugju", "Чем могу помочь? / Kau kunem te jelpo?", "Я тут / Hestem jergy"]))
        elif content == '!лого':
            await message.channel.send(file=File(r'F:\Программирование на Python\Discord\Main\logotype.jpg'))
        elif content == '!команды':
            await message.channel.send('Мои команды:\n!бот\n!лого - вывести логотип\n!команды - вывести команды\n!лимит спама [число сообщений] - установить лимит спама(для админов)\n!информация - информация о сервере и боте\n!аватар - вывести аватар\n!курс валюты [код валюты] - вывести курс валюты к рублю\n\n')
        elif content == '!инфо':
            await message.channel.send('Эта функция пока не доработана')
        elif content == '!ава':
            await message.channel.send(message.author.avatar_url)
        elif match(r'!курс валюты [a-zA-Z]{3}', content.lower()):
            currency = str(findall(r'[a-zA-Z]{3}', content)[0]).upper()
            try:
                await message.channel.send(str(valcursed(currency)) + ' ₽')
            except KeyError:
                await message.channel.send(f"Валюты {currency} нет в списке")
        elif match(r'!лимит спама \d+', str(content)):
            roles = {}
            for role in message.author.roles:
                roles[str(role)] = role  # !!!можно использовать str(role.mention)
            if 'админ' in roles:
                limit = int(str(content).replace('!лимит спама ', ''))
                if limit > 0:
                    self.spamLimit = int(str(content).replace('!лимит спама ', ''))
                    await message.channel.send(f'Лимит спама: {str(content).replace("!лимит спама ", "")} успешно установлен!')
                else:
                    await message.channel.send('Лимит спама должен быть больше 0')
            else:
                await message.channel.send(f'{author.mention}, только админы могут использовать эту команду!')
        elif content == '!стоп':
            roles = {}
            for role in message.author.roles:
                roles[str(role)] = role  # !!!можно использовать str(role.mention)
            if 'админ' in roles:
                message.channel.send('Бот успешно выключен')
                quit()
            else:
                await message.channel.send(f'{author.mention}, только админы могут использовать эту команду!')
        elif match(r'!видео .+', content):
            await message.channel.send('Пожалуйста, подождите...')
            cont = content[7:]
            self.videos_list = []
            for i in allVideos(channelId='UC2D-WeF4oMlyjlGq7hjRe9g', titles=True):
                self.videos_list.append(i)
            await message.channel.send('Список видео с канала получен')
            has = False
            for i in self.videos_list:
                if ratio(i[2].lower(), cont.lower()) > 30:
                    has = True
                    statistic = f'%Статистика%\nНазвание: {i[2]}\nСсылка: {i[0]}\nID: {i[1]}\nДата: {i[3]}\nПросмотры: {i[4].replace("viewCount ", "")}\nЛайки: {i[5].replace("likeCount ", "")}\nДизлайки: {i[6].replace("dislikeCount ", "")}\nКомментарии: {i[8].replace("commentCount ", "")}'
                    await message.channel.send(statistic)
                    break
            if not has:
                await message.channel.send(f'Видео "{cont}" не найдено на канале')
        else:
            self.spam.append([content, author])
            if isOneEl(self.spam, self.spamLimit):
                await message.channel.purge(limit=self.spamLimit)
                self.spam = []
            elif str(message.channel) in self.muted_channels_list:
                await message.delete()


if __name__ == '__main__':
    Client_().run('ODEzMDk5NDQzNTkxMDUzMzk0.YDKX3g._HaytvYjQC7ATddXVCD9Xx9Zwts')
