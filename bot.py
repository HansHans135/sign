import datetime
from hashlib import new
import discord
import json
import random
import os
import random, string
import requests

      
print("#####################################")
print("##請著名來源,亨哥保有解釋權力##")
print("#####################################")


#設定
with open ("config.json",mode="r",encoding="utf-8") as filt:
    data = json.load(filt)
PREFIX = data["prefix"]
op_id = data["owner_id"]
TOKEN = data["token"]
MAX = data["max"]
MIN = data["min"]
NEW = data["new"]
V_NOW = "4.2.4"

r=requests.get('https://raw.githubusercontent.com/HansHans135/sign/main/now.json')
V_GET = r.json()
V_NEW = V_GET["v"]


client = discord.Client()

@client.event   
async def on_ready():
    print('機器人已啟動，目前使用的bot：',client.user)
    status_w = discord.Status.online
    activity_w = discord.Activity(type=discord.ActivityType.watching, name=f"{PREFIX}help")
    await client.change_presence(status= status_w, activity=activity_w)
    
    print("版本檢查中...")
    if V_NOW == V_NEW:
        print(f"版本檢查完成\n目前為最新版本:{V_NEW}")
    else:
        print(f"目前不是最新版本\n是否需要下載更新?[y/n]\n(目前:{V_NOW},最新:{V_NEW})")
        i = 1
        while i == 1:
            a = input("你的選擇[y/n]:")
            if a == "y" or a == "n":
                if a == "y":
                    print("下載中...")
                    url = "https://raw.githubusercontent.com/HansHans135/sign/main/bot.py"
                    myfile = requests.get(url)
                    open('bot.py', 'wb').write(myfile.content)
                    print(f"下載完成!!重啟`bot.py`即可生效")
                    i = 0
                if a == "n":
                    print(f"已取消下載")
                    i = 0
            else:
                print("請輸入正確的回答")
            
        print(f"版本檢查完成\n目前:{V_NOW},最新:{V_NEW}")
        

@client.event
async def on_message(message):
#help
    if message.content == f"{PREFIX}help":
        await message.delete()
        embed = discord.Embed(title="指令清單", description=f"前輟是{PREFIX}", color=0x04f108)
        embed.add_field(name=f"{PREFIX}help", value="操作手冊")
        embed.add_field(name=f"{PREFIX}new", value="創建帳號")
        embed.add_field(name=f"{PREFIX}sign", value="簽到")
        embed.add_field(name=f"{PREFIX}me", value="看你有多少錢")
        embed.add_field(name=f"{PREFIX}money id", value="看別人有多少錢")
        embed.add_field(name=f"{PREFIX}to id 錢", value="轉帳給別人")
        embed.add_field(name=f"{PREFIX}get 代碼", value="兌換代碼")
        embed.add_field(name=f"{PREFIX}info", value="關於")
        embed.add_field(name=f"{PREFIX}up", value="檢查版本")
        await message.channel.send(content=None, embed=embed)
#info
    if message.content == f"{PREFIX}info":
        await message.delete()
        embed = discord.Embed(title="關於", description=f"前輟是{PREFIX}", color=0x04f108)
        embed.add_field(name="目前版本", value=f"v {V_NOW}")
        embed.add_field(name="初始金額", value=f"v {NEW}")
        embed.add_field(name="每次簽到最高", value=f"{MAX}$")
        embed.add_field(name="每次簽到最低", value=f"{MIN}$")
        embed.add_field(name="關於此機器人:", value="來自開源: https://github.com/HansHans135/sign")
        await message.channel.send(content=None, embed=embed)
#創建
    if message.content == f"{PREFIX}new":
      await message.delete()
      filepath = f"money/{message.author.id}.json"
      if os.path.isfile(filepath):
          await message.channel.send(f"{message.author.mention}你已經建立過帳號了!")
      else:
          with open (f"money/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
            data = {"last_time":"0","money":NEW}
            json.dump(data,filt)
            money = data['money']
          await message.channel.send(f"{message.author.mention}帳號建立完成,你目前有`{money}`元")

#簽到
    if message.content == f"{PREFIX}sign":
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
            await message.channel.send(f"{message.author.mention}你沒有帳號,請用`{PREFIX}!new`創建一個")
#查詢
    if message.content == f"{PREFIX}me":
        with open (f"money/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
            data = json.load(filt)
        await message.channel.send(f"{message.author.mention}你目前有`{data['money']}`元")

    if message.content.startswith(f'{PREFIX}money'):
      await message.delete()
      tmp = message.content.split(" ",2)
      if len(tmp) == 1:
        await message.channel.send("你查誰的錢啦？")
      else:
        with open (f"money/{tmp[1]}.json",mode="r",encoding="utf-8") as filt:
            data = json.load(filt)
        await message.channel.send(f"{message.author.mention}id`{tmp[1]}`他現在有`{data['money']}`元")
#set
    if message.content.startswith(f'{PREFIX}set'):
        if message.author.id == int(op_id):
          await message.delete()
          tmp = message.content.split(" ",2)
          崁入一 = tmp[1]
          tmp = message.content.split(f"{崁入一} ",2)
          崁入二 = tmp[1]
          #亨哥0126
          if len(tmp) == 1:
            await message.channel.send(f"格式:{PREFIX}set id 錢")
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
            
            
#to
    if message.content.startswith(f'{PREFIX}to'):
      await message.delete()
      tmp = message.content.split(" ",2)
      id = tmp[1]
      tmp = message.content.split(f"{id} ",2)
      money = tmp[1]
          #亨哥0126
      if len(tmp) == 1:
        await message.channel.send(f"{PREFIX}to id 錢")
      else:
          filepath = f"money/{id}.json"
          if os.path.isfile(filepath):
            with open (f"money/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
                if int(data["money"]) > int(money):
                    if int(money) > 0:
                        if int(message.author.id) == int(id):
                            await message.channel.send(f"{message.author.mention}你為何要轉給自己")
                        else:
                            TO = int(data["money"]) - int(money) 
                            with open (f"money/{id}.json",mode="r",encoding="utf-8") as filt:
                                data = json.load(filt)
                            data['money'] = int(data["money"]) + int(money)
                            with open (f"money/{id}.json",mode="w",encoding="utf-8") as filt:
                                json.dump(data,filt)
                            with open (f"money/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
                                data = json.load(filt)
                            data["money"] = int(TO)
                            with open (f"money/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
                                json.dump(data,filt)
                            await message.channel.send(f"{message.author.mention}轉帳成功!請通知 <@{id}> 查收")
                    else:
                        await message.channel.send(f"{message.author.mention}我不知道這個錢如何轉")
                else:
                    await message.channel.send(f"{message.author.mention}你付不出這筆錢.w.")
          else:
            await message.channel.send(f"找不到關於id:`{id}`的帳號")


#查別人
    if message.content.startswith(f'{PREFIX}money'):
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
            
    if message.content.startswith(f'{PREFIX}code'):
        if message.author.id == int(op_id):
          await message.delete()
          tmp = message.content.split(" ",2)
          if len(tmp) == 1:
            await message.channel.send(f"格式:{PREFIX}code 錢")
          else:
             CODE = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
             data = {"money":tmp[1]}
             with open (f"code/{CODE}.json",mode="w",encoding="utf-8") as filt:
                    json.dump(data,filt)
             await message.channel.send(f"代碼為:||{CODE}||")
        else:
            await message.channel.send(f"{message.author.mention}你沒有權限")
            
            
    if message.content.startswith(f'{PREFIX}get'):
      await message.delete()
      tmp = message.content.split(" ",2)
      if len(tmp) == 1:
        await message.channel.send("你要兌換甚麼啦？")
      else:
        filepath = f"code/{tmp[1]}.json"
        if os.path.isfile(filepath):
            with open (f"code/{tmp[1]}.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
            UP = data["money"]
            with open (f"money/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
            data['money'] = int(data["money"]) + int(UP)
            with open (f"money/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
                json.dump(data,filt)
            fileTest = f"code/{tmp[1]}.json"
            os.remove(fileTest)
            await message.channel.send(f"{message.author.mention}成功使用`{tmp[1]}`兌換`{UP}`元")
        else:
            await message.channel.send("未找到這個代碼或是已被兌換")
            
    if message.content == f"{PREFIX}up":
        if V_NOW == V_NEW:
            await message.channel.send(f"{message.author.mention}目前`簽到功能`為最新版本\n目前:{V_NOW},最新:{V_NEW}")
        else:
            await message.channel.send(f"{message.author.mention}目前`簽到功能`不是最新版本\n請重啟機器人更新版本\n目前:{V_NOW},最新:{V_NEW}")



            
client.run(TOKEN)

