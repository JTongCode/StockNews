import discord
from discord.ext import commands
from discord import app_commands

from google import genai
from google.genai import types
from google.genai import Client


class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
        try:
            #discord server id
            guild = discord.Object(id='Your Server ID')
            
            #syncing the guild object to the discord server                    
            synced = await self.tree.sync(guild=guild)       
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        
        #print error if unable to sync
        except Exception as e:
            print(f'Error syncing commands: {e}')            
        
        
intents = discord.Intents.default()
intents.message_content = True
bot = Client(command_prefix="!", intents=intents)   

#discord server id
GUILD_ID = discord.Object(id='Your Server ID')                    


#slash command initiation
@bot.tree.command(name="find_news", description="Finds latest daily news", guild=GUILD_ID)

#slash command function
async def findNews(interaction: discord.Interaction):                                          
    await interaction.response.send_message("Gathering sources...")
    
    #Gemini API key
    gemini = genai.Client(api_key='Your Gemini API Key')               
    
    answer = gemini.models.generate_content(
        model='gemini-2.5-flash',
        contents=types.Part.from_text(text='Can you look into some trends(around 5 topics, can be good or bad news) in stocks for just today and create a short summary about each one. '
                'Limit to just the US markets, include any federal regulations changes like interest rates if relevant. '   
                'Also state why it happened and what to expect in the future and Aim to keep explanations concise, put a brief and bolded title for each point. ' 
                'After each topic, can you also add the link to the website where you gathered this information. Keep it under a strict 2000 characters limit(including spaces, periods, astrix, etc).'
                ),
        config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]                              
        )
    )
    
    #utilized discord embed to surpass 2k character limit
    response = discord.Embed(description=answer.text)                                           
        
    await interaction.followup.send(embed=response)


#discord bot Token
bot.run('Your Discord Bot Token')            
