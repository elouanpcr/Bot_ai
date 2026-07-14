import discord
from discord.ext import commands
from model import get_class
import os, random
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("heh" * count_hxeh)

@bot.command(name="check")
async def check(ctx):

    # Verificar que el usuario haya enviado una imagen
    if len(ctx.message.attachments) == 0:
        await ctx.send("❌ Debes subir una imagen.")
        return

    # Crear carpeta si no existe
    if not os.path.exists("img"):
        os.makedirs("img")

    attachment = ctx.message.attachments[0]

    # Validar extensión
    if not attachment.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        await ctx.send("❌ Solo se permiten imágenes JPG, JPEG o PNG.")
        return

    image_path = os.path.join("img", attachment.filename)

    try:
        # Guardar imagen
        await attachment.save(image_path)

        # Realizar inferencia
        class_name, confidence_score = get_class(image_path)

        # Si la confianza es baja
        if confidence_score < 0.60:
            await ctx.send("Lo siento, no estoy seguro de lo que se muestra en la imagen.")
            return

        await ctx.send(
            f"**Predicción:** {class_name}\n"
            f"**Confianza:** {confidence_score:.2%}"
        )

    except Exception as e:
        await ctx.send("❌ Ocurrió un error al analizar la imagen.")
        print(e)
        
bot.run("MTQ2MzMwNTIzMDI3MDU5OTQxNA.GMXeBO.8i6zPPy5yNh4fy2Fae6voVWHjTeego98dJHleU")