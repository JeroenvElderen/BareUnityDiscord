import discord
import asyncio
import json
import os

from discord.ext import commands

DISBOARD_BOT_ID = 302050872383242240

REMINDER_CHANNEL = 1514975253908947040

DATA_FILE = "bump_timer.json"


class BumpReminder(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bump_task = None

    # -------------------------
    # JSON STORAGE
    # -------------------------

    def save_next_bump(self, timestamp):

        with open(
            DATA_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {"next_bump": timestamp},
                f
            )

    def load_next_bump(self):

        if not os.path.exists(DATA_FILE):
            return None

        try:

            with open(
                DATA_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            return data.get("next_bump")

        except Exception:
            return None

    # -------------------------
    # STARTUP RECOVERY
    # -------------------------

    @commands.Cog.listener()
    async def on_ready(self):

        if self.bump_task:
            return

        next_bump = self.load_next_bump()

        if next_bump:

            now = discord.utils.utcnow().timestamp()

            remaining = next_bump - now

            if remaining > 0:

                self.bump_task = asyncio.create_task(
                    self.bump_timer(
                        remaining
                    )
                )

                print(
                    f"Bump timer restored "
                    f"({int(remaining)}s remaining)"
                )

    # -------------------------
    # DISBOARD DETECTION
    # -------------------------

    @commands.Cog.listener()
    async def on_message(
        self,
        message
    ):

        if message.author.id != DISBOARD_BOT_ID:
            return

        if not message.embeds:
            return

        embed = message.embeds[0]

        description = (
            embed.description.lower()
            if embed.description
            else ""
        )

        if "bump done" not in description:
            return

        print("Disboard bump detected")

        # Cancel previous timer
        if self.bump_task:

            self.bump_task.cancel()

        next_bump = (
            discord.utils.utcnow().timestamp()
            + 7200
        )

        self.save_next_bump(
            next_bump
        )

        self.bump_task = asyncio.create_task(
            self.bump_timer(
                7200
            )
        )

    # -------------------------
    # TIMER
    # -------------------------

    async def bump_timer(
        self,
        seconds
    ):

        try:

            await asyncio.sleep(
                seconds
            )

            channel = self.bot.get_channel(
                REMINDER_CHANNEL
            )

            if channel:

                timestamp = int(
                    discord.utils.utcnow().timestamp()
                )

                embed = discord.Embed(
                    title="🔔 Disboard Bump Ready",
                    description=(
                        "The server can be bumped again.\n\n"
                        "Use **/bump** now."
                    ),
                    color=discord.Color.green()
                )

                embed.add_field(
                    name="Status",
                    value=(
                        f"Available "
                        f"<t:{timestamp}:R>"
                    ),
                    inline=False
                )

                await channel.send(
                    embed=embed
                )

            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)

        except asyncio.CancelledError:
            pass


async def setup(bot):

    await bot.add_cog(
        BumpReminder(bot)
    )