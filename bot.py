import datetime
from hashlib import new
import discord
import json
import random
import os


print("#####################################")
print("##請著名來源,亨哥保有解釋權力##")
print("#####################################")


#設定
with open ("config.json",mode="r",encoding="utf-8") as filt:
    data = json.load(filt)
前輟 = data["prefix"]
op_id = data["owner_id"]
TOKEN = data["token"]
MAX = data["max"]
MIN = data["min"]
NEW = data["new"]



client = discord.Client()

@client.event   
async def on_ready():
    print('機器人已啟動，目前使用的bot：',client.user)
    status_w = discord.Status.online
    activity_w = discord.Activity(type=discord.ActivityType.watching, name=f"{前輟}help")
    await client.change_presence(status= status_w, activity=activity_w)

@client.event
async def on_message(message):
#help
    if message.content == f"{前輟}help":
        await message.delete()
        embed = discord.Embed(title="指令清單", description=f"前輟是{前輟}", color=0x04f108)
        embed.add_field(name=f"{前輟}help", value="操作手冊")
        embed.add_field(name=f"{前輟}new", value="創建帳號")
        embed.add_field(name=f"{前輟}sign", value="簽到(冷卻時間的計算為每天08:00重製)")
        embed.add_field(name=f"{前輟}me", value="看你有多少錢")
        embed.add_field(name=f"{前輟}money id", value="看別人有多少錢")
        embed.add_field(name=f"{前輟}info", value="關於")
        await message.channel.send(content=None, embed=embed)
#info
    if message.content == f"{前輟}info":
        await message.delete()
        embed = discord.Embed(title="關於", description=f"前輟是{前輟}", color=0x04f108)
        embed.add_field(name="每次簽到最高", value=f"{MAX}$")
        embed.add_field(name="每次簽到最低", value=f"{MIN}$")
        embed.add_field(name="關於此機器人:", value="來自開源: https://github.com/HansHans135/sign")
        await message.channel.send(content=None, embed=embed)
#創建
    if message.content == f"{前輟}new":
      await message.delete()
      filepath = f"money/{message.author.id}.json"
      if os.path.isfile(filepath):
          await message.channel.send(f"{message.author.mention}你已經建立過帳號了!")
      else:
          with open (f"money/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
            data = {"last_time":"0","money":NEW,"g":"0"}
            json.dump(data,filt)
            money = data['money']
          await message.channel.send(f"{message.author.mention}帳號建立完成,你目前有`{money}`元")

#簽到
    if message.content == f"{前輟}sign":
        await message.delete()
        await message.channel.send("查詢中...")
        filepath = f"money/{message.author.id}.json"
        if os.path.isfile(filepath):
            today = datetime.date.today()
            with open (f"money/{message.author.id}.json",mode="r+",encoding="utf-8") as filt:
                data = json.load(filt)
                print(data['money'])
                last_time = data['last_time']
            if str(today) == str(last_time):
                await message.channel.send(f"{message.author.mention}你今天已經簽到過了")
            else:
                with open (f"money/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
                    data = json.load(filt)
                    print(data['money'])
                    upmoney = random.randrange(int(MIN),int(MAX))
                    newmoney = int(upmoney) + int(data['money'])
                data['money'] = newmoney
                with open (f"money/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
                    json.dump(data,filt)
                data['last_time'] = str(today)
                with open (f"money/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
                    json.dump(data,filt)
                await message.channel.send(f"{message.author.mention}本日簽到獎勵:`{upmoney}`元\n你目前有`{newmoney}`元")
        else:
            await message.channel.send(f"{message.author.mention}你沒有帳號,請用`{前輟}!new`創建一個")
#查詢
    if message.content == f"{前輟}me":
        with open (f"money/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
            data = json.load(filt)
        await message.channel.send(f"{message.author.mention}你目前有`{data['money']}`元")

    if message.content.startswith(f'{前輟}money'):
      await message.delete()
      tmp = message.content.split(" ",2)
      if len(tmp) == 1:
        await message.channel.send("你查誰的錢啦？")
      else:
        with open (f"money/{tmp[1]}.json",mode="r",encoding="utf-8") as filt:
            data = json.load(filt)
        await message.channel.send(f"{message.author.mention}id`{tmp[1]}`他現在有`{data['money']}`元")
#give
    if message.content.startswith(f'{前輟}give'):
        if message.author.id == int(op_id):
          await message.delete()
          tmp = message.content.split(" ",2)
          崁入一 = tmp[1]
          tmp = message.content.split(f"{崁入一} ",2)
          崁入二 = tmp[1]
          #亨哥0126
          if len(tmp) == 1:
            await message.channel.send(f"{前輟}give id 錢")
          else:
              filepath = f"money/{崁入一}.json"
              if os.path.isfile(filepath):
                with open (f"money/{崁入一}.json",mode="r",encoding="utf-8") as filt:
                    data = json.load(filt)
                data['money'] = int(崁入二)
                with open (f"money/{崁入一}.json",mode="w",encoding="utf-8") as filt:
                    json.dump(data,filt)
                with open (f"money/{崁入一}.json",mode="r",encoding="utf-8") as filt:
                    data = json.load(filt)
                await message.channel.send(f"已將id:`{崁入一}`設為`{data['money']}`元")
              else:
                await message.channel.send(f"找不到關於id:`{崁入一}`的帳號")
        else:
            await message.channel.send(f"{message.author.mention}你沒有權限")

#查別人
    if message.content.startswith(f'{前輟}money'):
      await message.delete()
      tmp = message.content.split(" ",2)
      if len(tmp) == 1:
        await message.channel.send("你查誰的錢啦？")
      else:
        filepath = f"money/{tmp[1]}.json"
        if os.path.isfile(filepath):
            with open (f"money/{tmp[1]}.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
            await message.channel.send(f"{message.author.mention}id`{tmp[1]}`他現在有`{data['money']}`元")
        else:
            await message.channel.send("未找到這筆資料")

client.run(TOKEN)