import discord
import re

try:

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    intents.members = True  # Enable guild members intent

    client = discord.Client(intents=intents)

    @client.event
    async def on_message(message):
        print("Message received")
        if message.author == client.user:
            return

        await process_message(message)

    @client.event
    async def on_message_edit(before, after):
        print("Message edited")
        if after.author == client.user:
            return

        await process_message(after)

    async def process_message(message):
        # Define the regular expression patterns for Twitter and X URLs
        twitter_pattern = re.compile(r'(https?://twitter\.com/\S+)')
        x_pattern = re.compile(r'(https?://x\.com/\S+)')

        # Check if the message contains a Twitter or X URL
        twitter_match = twitter_pattern.search(message.content)
        x_match = x_pattern.search(message.content)

        if twitter_match:
            original_url = twitter_match.group(1)
            rest_of_url = re.search(r'https?://twitter\.com(\S+)', message.content).group(1)
            new_content = f'https://fxtwitter.com{rest_of_url}'
            print(f"Sending new message: {new_content}")
            await message.channel.send(new_content)

        elif x_match:
            original_url = x_match.group(1)
            rest_of_url = re.search(r'https?://x\.com(\S+)', message.content).group(1)
            new_content = f'https://fxtwitter.com{rest_of_url}'
            print(f"Sending new message: {new_content}")
            await message.channel.send(new_content)

    @client.event
    async def on_ready():
            print(f'We have logged in as {client.user.name}')

    @client.event
    async def on_member_join(member):
        # Customize the welcome message as needed
        welcome_channel = member.guild.system_channel  # Change to the desired channel
        welcome_message = f'Hi {member.mention}! Welcome to the server! 🎉'
            
        if welcome_channel:
             await welcome_channel.send(welcome_message)

    @client.event
    async def on_member_remove(member):
        # Customize the goodbye message as needed
        goodbye_channel = member.guild.system_channel  # Change to the desired channel
        goodbye_message = f'Goodbye {member.display_name}! We will miss you! 😢'
            
        if goodbye_channel:
            await goodbye_channel.send(goodbye_message)

    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    client.run('YOUR_BOT_TOKEN')

except Exception as e:
    print(f"An error occurred: {e}")