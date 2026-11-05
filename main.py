import discord
from discord.ext import commands
import os, json, asyncio

try:
    with open("config.json") as f: CONFIG = json.load(f)
except:
    CONFIG = {}

def guardar():
    with open("config.json", "w") as f: json.dump(CONFIG, f)

def get_config(guild_id):
    gid = str(guild_id)
    if gid not in CONFIG:
        CONFIG[gid] = {
            "nombre": "Astral Bot",
            "prefix": "!",
            "color": 0x8A2BE2,
            "bienvenida": "Bienvenido {user} a {server}, ya somos {miembros}!",
            "despedida": "Se fue {user}, F...",
            "boost": "GRACIAS {user} por el boost!",
            "ip": "tu-ip-aca",
            "puerto": 19132,
            "smp": "Astral SMP",
            "canal_bienvenida": 0,
            "canal_despedida": 0,
            "canal_boost": 0,
            "rol_auto": 0,
            "rol_booster": 0,
            "palabras": [],
            "anti_links": False,
            "anti_spam": True
        }
        guardar()
    return CONFIG[gid]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=lambda b,m: get_config(m.guild.id)["prefix"] if m.guild else "!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot prendido como {bot.user}")

@bot.event
async def on_member_join(member):
    c = get_config(member.guild.id)
    if c["rol_auto"] != 0:
        rol = member.guild.get_role(c["rol_auto"])
        if rol: await member.add_roles(rol)
    if c["canal_bienvenida"] != 0:
        canal = bot.get_channel(c["canal_bienvenida"])
        if canal:
            embed = discord.Embed(title=f"Bienvenido {member.name}", description=c["bienvenida"].format(user=member.mention, server=member.guild.name, miembros=member.guild.member_count), color=c["color"])
            embed.set_thumbnail(url=member.display_avatar.url)
            await canal.send(embed=embed)

@bot.event
async def on_member_remove(member):
    c = get_config(member.guild.id)
    if c["canal_despedida"] != 0:
        canal = bot.get_channel(c["canal_despedida"])
        if canal:
            await canal.send(embed=discord.Embed(title=f"Se fue {member.name}", description=c["despedida"].format(user=member.name), color=0xFF0000))

@bot.event
async def on_member_update(before, after):
    if not before.premium_since and after.premium_since:
        c = get_config(after.guild.id)
        if c["canal_boost"] != 0:
            canal = bot.get_channel(c["canal_boost"])
            if canal:
                await canal.send(embed=discord.Embed(title="🚀 NUEVO BOOST!", description=c["boost"].format(user=after.mention), color=0xFF00FF))

@bot.command()
@commands.has_permissions(administrator=True)
async def setnombre(ctx, *, nombre):
    c = get_config(ctx.guild.id); c["nombre"]=nombre; guardar(); await ctx.send(f"✅ Nombre cambiado a **{nombre}**")

@bot.command()
@commands.has_permissions(administrator=True)
async def setcolor(ctx, color: str):
    colores = {"morado":0x8A2BE2, "rojo":0xFF0000, "verde":0x00FF00, "celeste":0x00FFFF, "rosa":0xFF00FF, "naranja":0xFFA500, "amarillo":0xFFFF00}
    c = get_config(ctx.guild.id); c["color"]=colores.get(color.lower(), 0x8A2BE2); guardar(); await ctx.send(f"✅ Color cambiado a **{color}**")

@bot.command()
@commands.has_permissions(administrator=True)
async def setbienvenida(ctx, *, texto):
    c = get_config(ctx.guild.id); c["bienvenida"]=texto; guardar(); await ctx.send(f"✅ Bienvenida: {texto}")

@bot.command()
@commands.has_permissions(administrator=True)
async def setcanal(ctx, tipo: str, canal: discord.TextChannel):
    c = get_config(ctx.guild.id)
    if tipo=="bienvenida": c["canal_bienvenida"]=canal.id
    if tipo=="despedida": c["canal_despedida"]=canal.id
    if tipo=="boost": c["canal_boost"]=canal.id
    guardar(); await ctx.send(f"✅ Canal de {tipo} puesto en {canal.mention}")

@bot.command()
@commands.has_permissions(administrator=True)
async def setrol(ctx, tipo: str, rol: discord.Role):
    c = get_config(ctx.guild.id)
    if tipo=="auto": c["rol_auto"]=rol.id
    if tipo=="booster": c["rol_booster"]=rol.id
    guardar(); await ctx.send(f"✅ Rol de {tipo} puesto en {rol.name}")

@bot.command()
@commands.has_permissions(administrator=True)
async def setip(ctx, ip, puerto: int = 19132):
    c = get_config(ctx.guild.id); c["ip"]=ip; c["puerto"]=puerto; guardar(); await ctx.send(f"✅ IP puesta: {ip}:{puerto}")

@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, nuevo):
    c = get_config(ctx.guild.id); c["prefix"]=nuevo; guardar(); await ctx.send(f"✅ Prefix nuevo: **{nuevo}**")

@bot.command()
@commands.has_permissions(administrator=True)
async def setsmp(ctx, *, nombre):
    c = get_config(ctx.guild.id); c["smp"]=nombre; guardar(); await ctx.send(f"✅ SMP: {nombre}")

@bot.command()
async def verconfig(ctx):
    c = get_config(ctx.guild.id)
    embed = discord.Embed(title=f"Config de {c['nombre']}", color=c["color"])
    embed.add_field(name="Prefix", value=c["prefix"], inline=True)
    embed.add_field(name="SMP", value=c["smp"], inline=True)
    embed.add_field(name="IP", value=f"{c['ip']}:{c['puerto']}", inline=False)
    embed.add_field(name="Bienvenida", value=c["bienvenida"], inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ip(ctx):
    c = get_config(ctx.guild.id)
    await ctx.send(embed=discord.Embed(title=f"🎮 {c['smp']}", description=f"**IP:** {c['ip']}\n**Puerto:** {c['puerto']}", color=c["color"]))

@bot.command()
async def ping(ctx):
    c = get_config(ctx.guild.id)
    await ctx.send(f"{c['nombre']} online ✅")

@bot.command()
async def koth(ctx, minutos: int = 5):
    await ctx.send(f"@everyone 🔥 KOTH ACTIVADO! Duración: {minutos} min")
    await asyncio.sleep(minutos * 60)
    await ctx.send("🏆 KOTH TERMINADO!")

bot.run(os.environ.get("TOKEN"))
