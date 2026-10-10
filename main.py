import discord 
from discord.ext import commands 
from config import token 
from logic import Pokemon, Wizard,Fighter
import random


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True


bot = commands.Bot(command_prefix='!', intents=intents)


# Pokémon seviyeleri
seviyeler = {}


@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')


@bot.command()
async def go(ctx):
    author = ctx.author.name  # Komutu çağıran kullanıcının adını alır
    if author not in Pokemon.pokemons:  # Bu kullanıcı için zaten bir Pokémon olup olmadığını kontrol ederiz
        chance = random.randint(1, 3)  # 1 ile 3 arasında rastgele bir sayı oluştururuz
        # Rastgele sayıya göre bir Pokémon nesnesi oluştururuz
        if chance == 1:
            pokemon = Pokemon(author)  # Standart bir Pokémon oluştururuz
        elif chance == 2:
            pokemon = Wizard(author)  # Wizard türünde bir Pokémon oluştururuz
        elif chance == 3:
            pokemon = Fighter(author)  # Fighter türünde bir Pokémon oluştururuz
        await ctx.send(await pokemon.info())  # Pokémon hakkında bilgi göndeririz
        image_url = await pokemon.show_img()  # Pokémon görüntüsünün URL'sini alırız
        if image_url:
            embed = discord.Embed()  # Gömülü bir mesaj (embed) oluştururuz
            embed.set_image(url=image_url)  # Gömülü mesaja görüntüyü ekleriz
            await ctx.send(embed=embed)  # Görüntülü gömülü mesajı göndeririz
        else:
            await ctx.send("Pokémon görüntüsü yüklenemedi.")  # Görüntü yüklenemezse hata mesajı veririz
    else:
        await ctx.send("Zaten bir Pokémon oluşturmuşsun.")  # Kullanıcıya zaten bir Pokémon oluşturduğunu bildiririz

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None  # Mesajda belirtilen kullanıcıyı alırız
    if target:  # Kullanıcının belirtilip belirtilmediğini kontrol ederiz
        # Hem saldırganın hem de hedefin Pokémon sahibi olup olmadığını kontrol ederiz
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]  # Hedefin Pokémon'unu alırız
            attacker = Pokemon.pokemons[ctx.author.name]  # Saldırganın Pokémon'unu alırız
            result = await attacker.attack(enemy)  # Saldırıyı gerçekleştirir ve sonucu alırız
            await ctx.send(result)  # Saldırı sonucunu göndeririz
        else:
            await ctx.send("Savaş için her iki tarafın da Pokémon sahibi olması gerekir!")  # Katılımcılardan birinin Pokémon'u yoksa bilgilendiririz
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")  # Saldırmak için kullanıcıyı etiketleyerek belirtmesini isteriz


# Pokémon besleme komutu
@bot.command()
async def besle(ctx):

    author = ctx.author.name

    if author in seviyeler:
        seviyeler[author] += 1

        await ctx.send(
            f"🍎 Pokémonun beslendi!\n"
            f"⭐ Yeni seviye: {seviyeler[author]}"
        )

    else:
        await ctx.send("Önce !go yazarak Pokémon oluşturmalısın!")


# Seviye gösterme komutu
@bot.command()
async def seviye(ctx):

    author = ctx.author.name

    if author in seviyeler:
        await ctx.send(
            f"⭐ Pokémon seviyen: {seviyeler[author]}"
        )

    else:
        await ctx.send("Henüz Pokémonun yok!")


# Nadir Pokémon bulma sistemi
@bot.command()
async def yakala(ctx):

    sans = random.randint(1,10)

    if sans == 10:
        await ctx.send(
            "🎉 Tebrikler! Nadir Pokémon buldun! ⭐"
        )

    else:
        await ctx.send(
            "Normal bir Pokémon buldun!"
        )



@bot.command()
async def info(ctx):
    # Kullanıcının kayıtlı bir Pokémon'u olup olmadığını sözlükte arıyoruz
    if ctx.author.name in Pokemon.pokemons:
        # Kayıtlıysa, ilgili Pokémon nesnesini değişkene atıyoruz
        pok = Pokemon.pokemons[ctx.author.name]
        
        # Pokémon'un info metodunu çağırıp çıkan sonucu Discord sohbetine gönderiyoruz
        # (Not: info() metodu metin döndürüyorsa ctx.send ile gönderilir)
        bilgi = pok.info()
        await ctx.send(bilgi)
    else:
        await ctx.send("Henüz bir Pokémon'a sahip değilsin! Önce kendine bir Pokémon oluştur.")



@bot.command()
async def feed(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        response = await pokemon.feed()
        await ctx.send(response)
    else:
        await ctx.send("henüz pokemonunuz yok !go ile bir tane alın!!")

bot.run(token)