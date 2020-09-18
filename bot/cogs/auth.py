# auth.py

from discord.ext import commands


class AuthCog(commands.Cog):
    """ Cog to manage authorisation. """

    def __init__(self, bot):
        """ Set attributes. """
        self.bot = bot

    @commands.command(brief='Link a player on the backend')
    async def link(self, ctx):
        """ Link a player by sending them a link to sign in with steam on the backend. """
        if not await self.bot.isValidChannel(ctx):
            return

        is_linked = await self.bot.api_helper.is_linked(ctx.author.id)

        if is_linked:
            player = await self.bot.api_helper.get_player(ctx.author.id)
            title = self.bot.translate('already-linked').format(player.steam_profile)
        else:
            link = await self.bot.api_helper.generate_link_url(ctx.author.id)

            if link:
                # Send the author a DM containing this link
                try:
                    await ctx.author.send(self.bot.translate('dm-link').format(link))
                    title = self.bot.translate('link-sent')
                except:
                    title = self.bot.translate('blocked-dm')
            else:
                title = self.bot.translate('unknown-error')

        embed = self.bot.embed_template(description=title)
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(brief='UnLink a player on the backend')
    async def unlink(self, ctx):
        """ Unlink a player by delete him on the backend. """
        if not await self.bot.isValidChannel(ctx):
            return

        is_linked = await self.bot.api_helper.is_linked(ctx.author.id)

        if not is_linked:
            title = self.bot.translate('already-not-linked')
        else:
            await self.bot.api_helper.unlink_discord(ctx.author)
            title = self.bot.translate('unlinked')
            role_id = await self.bot.get_league_data(ctx.channel.category, 'pug_role')
            role = ctx.guild.get_role(role_id)
            await ctx.author.remove_roles(role)

        embed = self.bot.embed_template(title=title)
        await ctx.send(content=ctx.author.mention, embed=embed)
