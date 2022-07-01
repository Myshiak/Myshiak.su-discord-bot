from os import system, getenv
from requests import get
from discord import Client, Embed, Member
from discord.message import Message
from pyshorteners import Shortener
from asyncio import sleep
from random import choice
from re import findall, match
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
def isNotAllowedPhrases(text, phrases, theme):
    for i in phrases[theme]:
        if i in text:
            return True
    return False
class Client_(Client):
    spam = []
    muted_channels_list = ['823140330685202432', '824549955900932096']
    text_channel_list = []
    videos_list = []
    spamLimit = 4
    commands = ['!bot','!help','!logo']
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
        await self.get_channel("793895190653173810").send(embed=Embed(title=f'{member} joined',description=f'Welcome, {member}! Leiszgenay szerveretume, {member}!',color=0xFFFF00))
    async def on_message(self, message: Message):
        author: Member = message.author
        content: str = message.content
        print(f'[MESSAGE] Content: {content}\nAuthor: {author}\n|')
        if author == Client().user:
            return
        if content.lower() == "!bot":
            await message.channel.send(
                choice(['Да / Hes', "Ага / Agja", "Чем могу помочь? / Kei kanem lauszuent?", "Я тут / Hestem jeray"]))
        elif content == '!help':
            await message.channel.send(embed=Embed(title='Usage:',description='\n!bot\n!spam limit [number of messages]-set the spam limit(for staff)\n!info-information about the server and bot\n!avatar - avatar output\n!currency rate [currency code] - currency rate output\n!video [video\'s name] - information about a video from Myshiak.su\'s YouTube channel\n!shorten [link] - link shortening\n\n',color=0xFFFF00))
        elif content == '!info':
            roles = []
            channels = []
            voice_channels = []
            emojis = []
            categories = []
            for role in message.guild.roles:
                roles.append(str(role.name))
            for channel in message.guild.text_channels:
                channels.append(str(channel.name))
            for voice_channel in message.guild.voice_channels:
                voice_channels.append(str(voice_channel.name))
            for emoji in message.guild.emojis:
                emojis.append(emoji.name)
            for category in message.guild.categories:
                categories.append(category.name)
            del role, channel, voice_channel, emoji, category
            roles = ', '.join(roles)
            channels = ', '.join(channels)
            voice_channels = ', '.join(voice_channels)
            emojis = ', '.join(emojis)
            categories = ', '.join(categories)
            all_info = {
                'ID': message.guild.id,
                'Description': str(message.guild.description),
                'Region': str(message.guild.region).capitalize(),
                'Number of members': message.guild.member_count,
                'Roles': roles,
                'Categories': categories,
                'Text channels': channels,
                'Voice channels': voice_channels,
                'Emojis': emojis
            }
            info = Embed(title=f'Information about the server {message.guild.name}', description=f'', color=0xFFFF00)
            for i in all_info:
                info.add_field(name=i, value=all_info[i], inline=False)
            info.set_image(url=message.guild.icon_url)
            await message.channel.send(embed=info)
        elif content == '!avatar':
            e = Embed(title=f'Avatar of {message.author}', description='', color=0xFFFF00)
            e.set_image(url=message.author.avatar_url)
            await message.channel.send(embed=e)
        elif match(r'!currency rate [a-zA-Z]{3}', content.lower()):
            currency = content[15:].upper()
            try:
                await message.channel.send(
                    embed=Embed(title=f'{currency} to ruble exchange rate:', description=str(valcursed(currency)) + ' ₽',
                                color=0xFFFF00))
            except KeyError:
                await message.channel.send(f"The currency `{currency}` not found in the list")
        elif match(r'!spam limit \d+', str(content)):
            roles = {}
            for role in message.author.roles:
                roles[str(role)] = role
            if 'админ' in roles:
                limit = int(str(content).replace('!spam limit ', ''))
                if limit > 0:
                    self.spamLimit = int(str(content).replace('!spam limit ', ''))
                    await message.channel.send(embed=Embed(title='Spam limit',description=f'Spam limit: {str(content).replace("!spam limit ", "")} was successfully set!',color=0xFFFF00))
                else:
                    await message.channel.send('Spam limit should be greater than 0')
            else:
                await message.channel.send(f'{author.mention}, the command is only for staff!')
        elif match(r'!purge \d+', str(content)):
            roles = {}
            for role in message.author.roles:
                roles[str(role)] = role
            if 'админ' in roles:
                limit = int(str(content).replace('!purge ', ''))
                if limit > 0:
                    await message.channel.purge(limit=limit)
                    await message.channel.send(
                        embed=Embed(title='Purging', description=f'{limit} messages were deleted', color=0xFFFF00))
                else:
                    await message.channel.send('The argument should be greater than 0')
            else:
                await message.channel.send(f'{author.mention}, the command is only for staff!')
        elif content == '!stop':
            roles = {}
            for role in message.author.roles:
                roles[str(role)] = role
            if 'админ' in roles:
                message.channel.send('Power off...')
                quit()
            else:
                await message.channel.send(f'{author.mention}, the command is only for staff!')
        elif match(r'!shorten .+', content):
            await message.channel.send(Shortener().tinyurl.short(content[9:]))
        elif match(r'!video .+', content):
            await message.channel.send('Please wait...')
            cont = content[7:]
            self.videos_list = []
            for i in allVideos(channelId='UC2D-WeF4oMlyjlGq7hjRe9g', titles=True):
                self.videos_list.append(i)
            await message.channel.send('The list of the channel\'s videos was got')
            has = False
            for i in self.videos_list:
                if ratio(i[2].lower(), cont.lower()) > 30:
                    has = True
                    statistic = f'Name: {i[2]}\nLink: {i[0]}\nID: {i[1]}\nDate: {i[3]}\nViews: {i[4].replace("viewCount ", "")}\nLikes: {i[5].replace("likeCount ", "")}\nDislikes: {i[6].replace("dislikeCount ", "")}\nComments: {i[8].replace("commentCount ", "")}'
                    await message.channel.send(embed=Embed(title='Статистика', description=statistic, color=0xFFFF00))
                    break
            if not has:
                await message.channel.send(f'The video "{cont}" not found on the channel')
        elif match(r'!mute <#\d+>', content):
            roles = {}
            for role in message.author.roles:
                roles[str(role)] = role
            if 'админ' in roles:
                chatId = findall('\d+', message.content)[0]
                if chatId == '793895190653173810':
                    await message.channel.send('You cannot mute the channel <#793895190653173810>')
                else:
                    await message.channel.send(
                        embed=Embed(title='Mute channel', description=f'The channel <#{chatId}> was muted', color=0xFFFF00))
                    self.muted_channels_list.append(chatId)
            else:
                await message.channel.send(f'{author.mention}, the command is only for staff!')
        elif match(r'!unmute <#\d+>', content):
            roles = {}
            for role in message.author.roles:
                roles[str(role)] = role
            if 'админ' in roles:
                chatId = findall('\d+', message.content)[0]
                await message.channel.send(
                    embed=Embed(title='Unmute channel', description=f'The channel <#{chatId}> was unmuted', color=0xFFFF00))
                if chatId in self.muted_channels_list:
                    self.muted_channels_list.remove(chatId)
            else:
                await message.channel.send(f'{author.mention}, the command is only for staff!')
        elif content == '!deirlenti':
            await message.channel.send(choice(['Kei numenent? Kei hesten aktetima?', 'Szanktpeterburge hester an nebesti state']))
        else:
            self.spam.append([content, author])
            if isOneEl(self.spam, self.spamLimit):
                await message.channel.purge(limit=self.spamLimit)
                self.spam = []
            elif str(message.channel.id) in self.muted_channels_list:
                await message.delete()
            elif (str(message.content) == 'Please wait...' or str(message.content) == 'The list of the channel\'s videos was got') and str(message.author) == 'Myshiak.admin#8971':
                await sleep(1)
                await message.delete()
            else:
                notAllowedPhrases = {'sex': ['секс','трах','презерватив','презик','sex','penis','condom']}
                if findall(r'\d', content) == ['8', '8', '0', '0', '5', '5', '5', '3', '5', '3', '5']:
                    await message.channel.send('Проще позвонить, чем у кого-то занимать')
                elif 'это я' == content.lower():
                    await message.channel.send('Головка от х*я')
                elif isNotAllowedPhrases(content, notAllowedPhrases, 'sex') and str(message.author) != 'Myshiak.admin#8971':
                    e = Embed(title=str(author), description='Сейчас ' + choice(['♂boss of this gym♂', '♂dungeon master♂', '♂leatherman♂']) + ' сделает Вам' + choice(['♂gay sex♂', '♂fucking cumming♂', '♂Fisting♂'])+' за разговоры о ♂sex♂\'е', color=0xFFFF00)
                    e.set_image(url=choice(['https://media.tenor.com/images/a8e6991c5b7cef9ea1d8d4d4d7ec6de5/tenor.gif', 'https://media.tenor.com/images/26726e20154d5b8c089fab1e02e626a3/tenor.gif', 'https://media.tenor.com/images/0d15b034b3b9f551988513759fb0bf79/tenor.gif']))
                    await message.channel.send(embed=e)
                elif len(content) > 1 and content[1:].isupper():
                    await message.channel.send(choice(["Чего ты? Остынь", "Не злоупотребляй капсом"]))


if __name__ == '__main__':
    Client_().run(getenv('TOKEN'))
