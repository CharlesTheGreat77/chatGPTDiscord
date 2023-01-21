import discord
import requests
import openai
import io

token = "%DISCORD TOKEN%"
client = discord.Client(intents=discord.Intents.all())
openai.api_key = "%OPENAI KEY%"
api = {"Authorization": f"Bearer {openai.api_key}"}

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('?help'):
        await message.channel.send(
        "?help: Displays this help message\n"
        "!image: Generates an image based on user context\n"
        "?question: Generates text based on user context\n"
        )

    elif message.content.startswith('!image'):
        question = message.content.replace('!image ', '')
        image = image2Discord(question)
        if image == 'error':
            await message.channel.send(f"An error occurred: {image}")
        await message.channel.send(file=discord.File(io.BytesIO(image), 'image.jpg'))

    elif message.content.startswith('?question'):
        question = message.content.replace('?question ', '')
        response = chat(question)
        if isinstance(response, str):
            await message.channel.send(response)
        else:
            for line in response:
                await message.channel.send(line)


def image2Discord(question):
    url = "https://api.openai.com/v1/images/generations"
    data = {"model": "image-alpha-001", "prompt": question, "num_images": 1, "size": "512x512", "response_format": "url"}
    response = requests.post(url, headers=api, json=data).json()
    if 'error' in response:
        image = 'error'
    else:
        image_url = response['data'][0]['url']
        response = requests.get(image_url)
        image = response.content
    return image

def chat(question):
    temperature = 0.5
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=2048, # 4000 is the maximum number of tokens for the davinci 003 GPT3 model
        n=1,
        stop=None,
        temperature=temperature,
    )
    return completions.choices[0].text


client.run(token)
