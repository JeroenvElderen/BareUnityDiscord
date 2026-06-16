import discord
from discord.ext import commands

WELCOME_FORUM = 1516496171831394437


class WelcomeThreads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(
        self,
        member: discord.Member
    ):

        forum = member.guild.get_channel(
            WELCOME_FORUM
        )

        if not isinstance(
            forum,
            discord.ForumChannel
        ):
            return

        try:

            created = await forum.create_thread(
                name=f"{member.display_name}",
                content=(
                    f"# 🌱 Welcome to Bare Unity\n\n"
                    f"{member.mention}\n\n"
                    f"This is your personal onboarding thread.\n"
                    f"Follow the steps below to gain full access "
                    f"to the Bare Unity community."
                )
            )

            thread = created.thread

            # ==================================
            # EMBED 1
            # ==================================

            embed1 = discord.Embed(
                title="📜 Getting Started",
                description=(
                    "Welcome to Bare Unity.\n\n"
                    "Complete these first steps before "
                    "continuing to verification."
                ),
                color=discord.Color.blurple()
            )

            embed1.add_field(
                name="STEP 1 • Read The Bare Code",
                value=(
                    "**Channel:** <#1514975253908947037>\n\n"
                    "Please carefully read all community rules.\n\n"
                    "Bare Unity is built on:\n"
                    "• Respect\n"
                    "• Consent\n"
                    "• Privacy\n"
                    "• Authentic Naturism"
                ),
                inline=False
            )

            embed1.add_field(
                name="STEP 2 • React With ✅",
                value=(
                    "After reading the rules,\n"
                    "react with **✅** to the verification message.\n\n"
                    "This grants the **Verification** role and "
                    "unlocks the next stage."
                ),
                inline=False
            )

            embed1.add_field(
                name="STEP 3 • Submit A Verification Request",
                value=(
                    "**Forum:** <#1515796912840773672>\n\n"
                    "Create a new verification request thread.\n\n"
                    "A moderator will review your request "
                    "and contact you."
                ),
                inline=False
            )

            embed1.set_footer(
                text="Welcome Garden • Step 1 of 3"
            )

            # ==================================
            # EMBED 2
            # ==================================

            embed2 = discord.Embed(
                title="🎥 Verification Journey",
                description=(
                    "Verification helps keep Bare Unity "
                    "safe, respectful and authentic."
                ),
                color=discord.Color.orange()
            )

            embed2.add_field(
                name="STEP 4 • Moderator Contact",
                value=(
                    "A moderator will review your request.\n\n"
                    "You may be contacted to arrange a "
                    "verification appointment."
                ),
                inline=False
            )

            embed2.add_field(
                name="STEP 5 • Video Verification",
                value=(
                    "You'll attend a short private "
                    "verification session.\n\n"
                    "**Privacy Information**\n"
                    "• No recordings are made\n"
                    "• Verification is private\n"
                    "• Access is limited to staff\n"
                    "• Usually only takes a few minutes"
                ),
                inline=False
            )

            embed2.add_field(
                name="STEP 6 • Become Semi-Verified",
                value=(
                    "After successful verification "
                    "you will receive the\n"
                    "**Sapling (Semi-Verified)** role.\n\n"
                    "This unlocks the Newly Verified Garden."
                ),
                inline=False
            )

            embed2.set_footer(
                text="Verification • Step 2 of 3"
            )

            # ==================================
            # EMBED 3
            # ==================================

            embed3 = discord.Embed(
                title="🌳 Final Onboarding",
                description=(
                    "You're almost there.\n\n"
                    "Complete these final steps to become "
                    "a fully verified member."
                ),
                color=discord.Color.green()
            )

            embed3.add_field(
                name="STEP 7 • Team Introduction",
                value=(
                    "**Forum:** <#1515820692803686451>\n\n"
                    "Browse the Team Introduction forum.\n\n"
                    "**IMPORTANT:**\n"
                    "React with **🌿** to any Team Introduction "
                    "forum post.\n\n"
                    "Do NOT react to a reply message.\n"
                    "The reaction must be placed on the "
                    "forum post itself.\n\n"
                    "This grants the Self Introduction role."
                ),
                inline=False
            )

            embed3.add_field(
                name="STEP 8 • Create Your Introduction",
                value=(
                    "**Forum:** <#1515812572157444187>\n\n"
                    "Create your own introduction thread.\n\n"
                    "Suggested topics:\n"
                    "• Your naturist journey\n"
                    "• What naturism means to you\n"
                    "• What brought you to Bare Unity\n"
                    "• Your interests and hobbies"
                ),
                inline=False
            )

            embed3.add_field(
                name="🏆 FINAL STEP • Become Evergreen",
                value=(
                    "After staff review of your introduction,\n"
                    "you will receive the\n"
                    "**Evergreen (Verified)** role.\n\n"
                    "You have now completed onboarding "
                    "and gained full access to the community."
                ),
                inline=False
            )

            embed3.add_field(
                name="🌿 Community Values",
                value=(
                    "Freedom • Respect • Privacy • Consent • Nature\n\n"
                    "Thank you for helping keep Bare Unity "
                    "safe, respectful and authentic."
                ),
                inline=False
            )

            embed3.set_footer(
                text="Final Steps • Step 3 of 3"
            )

            await thread.send(embed=embed1)
            await thread.send(embed=embed2)
            await thread.send(embed=embed3)

            print(
                f"Created welcome thread for {member}"
            )

        except Exception as e:

            print(
                f"Welcome thread error: {e}"
            )


async def setup(bot):
    await bot.add_cog(
        WelcomeThreads(bot)
    )