import discord
from discord.ext import commands
from discord import app_commands
from utils.ta import analyse_multiple_timeframes

class Analyse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="analyse", description="TA van coin op 6 timeframes")
    @app_commands.describe(coin="Bijv. kaspa, fet, link")
    async def analyse(self, interaction: discord.Interaction, coin: str):
        await interaction.response.defer()
        symbol = f"{coin.lower()}usdt"
        try:
            resultaten = analyse_multiple_timeframes(symbol)
            if not resultaten:
                await interaction.followup.send("Geen TA-data beschikbaar.")
                return
            embed = discord.Embed(title=f"Analyse: {coin.upper()}", color=0x00ffcc)
            for tf, data in resultaten.items():
                embed.add_field(
                    name=f"{tf}",
                    value=f"RSI: {data['rsi']:.2f}\nTrend: {data['trend']}\nPrijs: ${data['close']:.5f}",
                    inline=False
                )
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"Fout bij analyse: {str(e)}")

async def setup(bot):
    await bot.add_cog(Analyse(bot))