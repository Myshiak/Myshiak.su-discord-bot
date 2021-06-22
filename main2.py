from os import system, getenv
system('pip install requests discord.py fuzzywuzzy')
from requests import get
from discord import Client, File, utils, Embed
from discord.message import Message
from asyncio import sleep
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
    muted_channels_list = ['823140330685202432', '824549955900932096']
    text_channel_list = []
    videos_list = []
    spamLimit = 4
    commands = ['!бот', "!команды", "!лого"]
    question_message_id = 813751244467470336
    roles = {
        'админ': 813123398656983090,
        'участник': 813750101968683008
    }
    
    
    async def on_ready(self):
        for guild in self.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel.name)
        print('[INFO] Channel list is got')
        print(f'[INFO] logged in as @{self.user}')

    async def on_member_join(self, member):
        
        await self.get_channel("793895190653173810").send(embed=Embed(title=f'{member} вступил на наш сервер', description=f'Добро пожаловать на наш сервер, {member}! Eleiśgenä Emes śeŕveŕte, {member}!', color=0xFFFF00))

    async def on_message(self, message: Message):
        author = message.author
        content: str = message.content
        print(f'[MESSAGE] Content: {content}\nAuthor: {author}\n|')
        if author == Client().user:
            return
        if content.lower() == "!бот":
            await message.channel.send(choice(['Да / Hes', "Ага / Ugju", "Чем могу помочь? / Kau kunem te luośo?", "Я тут / Hestem jeŕy"]))
        elif content == '!команды':
            await message.channel.send(embed=Embed(title='Мои команды:', description='\n!бот\n!команды-вывести команды\n!лимит спама [число сообщений]-установить лимит спама(для админов)\n!инфо-информация о сервере и боте\n!ава - вывести аватар\n!курс валюты [код валюты] - вывести курс валюты к рублю\n!видео [видео] - информация о видео с канала Myshiak.su\n\n', color=0xFFFF00))
        elif content == '!инфо':
            await message.channel.send('Эта команда находится в разработке')
        elif content == '!ава':
            e = Embed(title=f'Аватарка {message.author}', description='', color=0xFFFF00)
            e.set_image(url=message.author.avatar_url)
            await message.channel.send(embed=e)
        elif match(r'!курс валюты [a-zA-Z]{3}', content.lower()):
            currency = str(findall(r'[a-zA-Z]{3}', content)[0]).upper()
            try:
                await message.channel.send(embed=Embed(title=f'Курс валюты {currency} к рублю:', description=str(valcursed(currency)) + ' ₽', color=0xFFFF00))
            except KeyError:
                await message.channel.send(f"Валюты {currency} нет в списке")
        elif match(r'!лимит спама \d+', str(content)):
            roles = {}
            for role in message.author.roles:
                roles[str(role)] = role
            if 'админ' in roles:
                limit = int(str(content).replace('!лимит спама ', ''))
                if limit > 0:
                    self.spamLimit = int(str(content).replace('!лимит спама ', ''))
                    await message.channel.send(embed=Embed(title='Лимит спама', description=f'Лимит спама: {str(content).replace("!лимит спама ", "")} успешно установлен!', color=0xFFFF00))
                else:
                    await message.channel.send('Лимит спама должен быть больше 0')
            else:
                await message.channel.send(f'{author.mention}, только админы могут использовать эту команду!')
        elif match(r'!очистить \d+', str(content)):
            roles = {}
            for role in message.author.roles:
                roles[str(role)] = role  # !!!можно использовать str(role.mention)
            if 'админ' in roles:
                limit = int(str(content).replace('!очистить ', ''))
                if limit > 0:
                    await message.channel.purge(limit=limit)
                    await message.channel.send(embed=Embed(title='Очистка', description=f'Очищено {limit} сообщений', color=0xFFFF00))
                else:
                    await message.channel.send('Аргумент должен быть больше 0')
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
                    statistic = f'Название: {i[2]}\nСсылка: {i[0]}\nID: {i[1]}\nДата: {i[3]}\nПросмотры: {i[4].replace("viewCount ", "")}\nЛайки: {i[5].replace("likeCount ", "")}\nДизлайки: {i[6].replace("dislikeCount ", "")}\nКомментарии: {i[8].replace("commentCount ", "")}'
                    await message.channel.send(embed=Embed(title='Статистика', description=statistic, color=0xFFFF00))
                    break
            if not has:
                await message.channel.send(f'Видео "{cont}" не найдено на канале')
        elif match(r'!мут <#\d+>', content):
            roles = {}
            for role in message.author.roles:
                roles[str(role)] = role
            if 'админ' in roles:
                chatId = findall('\d+', message.content)[0]
                if chatId == '793895190653173810':
                    await message.channel.send('Вы не можете замутить основной канал')
                else:
                    await message.channel.send(embed=Embed(title='Мут канала', description=f'Канал <#{chatId}> замьючен', color=0xFFFF00))
                    self.muted_channels_list.append(chatId)
            else:
                await message.channel.send(f'{author.mention}, только админы могут использовать эту команду!')
        elif match(r'!размут <#\d+>', content):
            roles = {}
            for role in message.author.roles:
                roles[str(role)] = role
            if 'админ' in roles:
                chatId = findall('\d+', message.content)[0]
                await message.channel.send(embed=Embed(title='Размут канала', description=f'Канал <#{chatId}> размьючен', color=0xFFFF00))
                if chatId in self.muted_channels_list:
                    self.muted_channels_list.remove(chatId)
            else:
                await message.channel.send(f'{author.mention}, только админы могут использовать эту команду!')
        else:
            self.spam.append([content, author])
            if isOneEl(self.spam, self.spamLimit):
                await message.channel.purge(limit=self.spamLimit)
                self.spam = []
            elif str(message.channel.id) in self.muted_channels_list:
                await message.delete()
            elif (str(message.content) == 'Пожалуйста, подождите...' or str(message.content) == 'Список видео с канала получен') and str(message.author) == 'Hydra.su#8971':
                await sleep(1)
                await message.delete()

if __name__ == '__main__':
    Client_().run(getenv('TOKEN'))
