import discord
from discord.ext import commands
from discord import app_commands

from google import genai
from google.genai import types
from google.genai import Client

#import os

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
        try:
            guild = discord.Object(id=1126996754106171454)
            synced = await self.tree.sync(guild=guild)  #syncing the guild object to the discord server
            print(f'Synced {len(synced)} commands to guild {guild.id}')
            
        except Exception as e:
            print(f'Error syncing commands: {e}')   #print error if unable to sync
        
        
intents = discord.Intents.default()
intents.message_content = True
bot = Client(command_prefix="!", intents=intents)   #instatiates bot

GUILD_ID = discord.Object(id=1126996754106171454)   #discord server id


@bot.tree.command(name="find_news", description="Finds latest daily news", guild=GUILD_ID)     #slash command initiation
async def findNews(interaction: discord.Interaction):                                          #slash command function
    await interaction.response.send_message("Gathering sources...")
    
    gemini = genai.Client(api_key='AQ.Ab8RN6KnUe80cHaC_Uf2Xtwq4JsMJE6GLbgqkY4Ht_AvOafbEA')         #Gemini API key
    
    answer = gemini.models.generate_content(
        model='gemini-2.5-flash',
        contents=types.Part.from_text(text='Can you look into some of the largest changes(around 5 topics, but try to focus more on companies and stocks) in stocks as of today and create a short summary about each one. Limit to just the US markets, include any federal regulations changes like interest rates if relevant. '
                'Also state why it happened and what to expect in the future and Aim to keep explanations concise, put a brief and bolded title for each point. Keep it under a strict 2000 characters limit(including spaces, periods, astrix, etc).'
                ),
        config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )
    
    response = discord.Embed(description=answer.text)
    
    await interaction.followup.send(embed=response)


bot.run('MTUxNjMxODc5MzUxOTk5Mjk1Mg.GSdpg4.WtfRN3_SDJ5cjz_0Ll01tWizNz2z0UIfDF255I')            #discord bot API key