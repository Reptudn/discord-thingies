import requests
import time
import json
from discord import SyncWebhook, Color
import discord
import schedule

#https://dash.fortnite-api.com/

shopURL = 'https://fortnite-api.com/v2/shop/br/combined'
webhookURL = '' # hier muss die webhook url rein noch

webhook = SyncWebhook.from_url(webhookURL)

def dailyShop():
    shop = getShop()
    daily = shop['data']['daily']['entries']
    
    for i in daily:
        embed = discord.Embed(title=i['devName'].replace('[VIRTUAL]', '').replace('MtxCurrency', '').replace('1 x', '').replace('for', '')[:-4], description=i['items'][0]['description'], url='https://discord.com/invite/fortnite')
        embed.add_field(name='Price', value=i['finalPrice'])
        embed.set_thumbnail(url=i['items'][0]['images']['icon'])
        embed.set_footer(text=time.ctime())
        
        rarity = i['items'][0]['rarity']['value']
        embed.add_field(name='Rarity', value=str(rarity).capitalize())
        if(rarity == 'rare'):
            embed.color = Color.blue()
        elif(rarity == 'uncommon'):
            embed.color = Color.green()
        elif(rarity == 'common'):
            embed.color = Color.greyple()
        elif(rarity == 'legendary'):
            embed.color = Color.gold()
        elif(rarity == 'epic'):
            embed.color = Color.purple()
        else:
            pass

        webhook.send(embed=embed)

def getShop(): #json shop response
    return requests.get(shopURL).json()

#show the daily shop once when webhook is being started
dailyShop()  

schedule.every().day.at('02:03').do(dailyShop) #send the daily webhook every day at 3mins after shop refresh to give the api some time to also refresh

while True:
    time.sleep(86400) # sleep one day if scheduling is not working
    dailyShop()
