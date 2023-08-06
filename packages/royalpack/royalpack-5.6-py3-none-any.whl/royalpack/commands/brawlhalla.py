import asyncio
import logging
import sentry_sdk
import aiohttp
from typing import *
from royalnet.commands import *
from royalnet.utils import *
from royalnet.serf.telegram.escape import escape as tg_escape
from ..tables import Steam, Brawlhalla
from ..types import BrawlhallaRank, BrawlhallaMetal, BrawlhallaTier

log = logging.getLogger(__name__)


class BrawlhallaCommand(Command):
    name: str = "brawlhalla"

    aliases = ["bh", "bruhalla", "bruhlalla"]

    description: str = "Visualizza le tue statistiche di Dota!"

    syntax: str = ""

    def __init__(self, interface: CommandInterface):
        super().__init__(interface)
        if self.interface.name == "telegram":
            self.loop.create_task(self._updater(900))

    async def _send(self, message):
        client = self.serf.client
        await self.serf.api_call(client.send_message,
                                 chat_id=self.config["Telegram"]["main_group_id"],
                                 text=tg_escape(message),
                                 parse_mode="HTML",
                                 disable_webpage_preview=True)

    @staticmethod
    def _display(bh: Brawlhalla) -> str:
        string = f"ℹ️ [b]{bh.name}[/b]\n\n"

        if bh.rank_1v1:
            string += f"1v1: [b]{bh.rank_1v1}[/b]\n"

        return string

    async def _notify(self,
                      obj: Brawlhalla,
                      attribute_name: str,
                      old_value: Any,
                      new_value: Any):
        if attribute_name == "rank_1v1":
            old_rank: Optional[BrawlhallaRank] = old_value
            new_rank: Optional[BrawlhallaRank] = new_value
            if new_rank > old_rank:
                message = f"📈 [b]{obj.steam.user}[/b] è salito a [b]{new_value}[/b] ({obj.rating_1v1} MMR) in 1v1 su Brawlhalla! Congratulazioni!"
            elif new_rank < old_rank:
                message = f"📉 [b]{obj.steam.user}[/b] è sceso a [b]{new_value}[/b] ({obj.rating_1v1} MMR) in 1v1 su Brawlhalla."
            else:
                return
            await self._send(message)

    @staticmethod
    async def _change(obj: Brawlhalla,
                      attribute_name: str,
                      new_value: Any,
                      callback: Callable[[Brawlhalla, str, Any, Any], Awaitable[None]]):
        old_value = obj.__getattribute__(attribute_name)
        if old_value != new_value:
            await callback(obj, attribute_name, old_value, new_value)
        obj.__setattr__(attribute_name, new_value)

    async def _update(self, steam: Steam, db_session):
        BrawlhallaT = self.alchemy.get(Brawlhalla)
        log.info(f"Updating: {steam}")
        async with aiohttp.ClientSession() as session:
            bh: Brawlhalla = steam.brawlhalla
            if bh is None:
                log.debug(f"Checking if player has an account...")
                async with session.get(f"https://api.brawlhalla.com/search?steamid={steam.steamid.as_64}&api_key={self.config['Brawlhalla']['api_key']}") as response:
                    if response.status != 200:
                        raise ExternalError(f"Brawlhalla API /search returned {response.status}!")
                    j = await response.json()
                    if j == {} or j == []:
                        log.debug("No account found.")
                        return
                    bh = BrawlhallaT(
                        steam=steam,
                        brawlhalla_id=j["brawlhalla_id"],
                        name=j["name"]
                    )
                    db_session.add(bh)
                    message = f"↔️ Account {bh} connesso a {bh.steam.user}!"
                    await self._send(message)
            async with session.get(f"https://api.brawlhalla.com/player/{bh.brawlhalla_id}/ranked?api_key={self.config['Brawlhalla']['api_key']}") as response:
                if response.status != 200:
                    raise ExternalError(f"Brawlhalla API /ranked returned {response.status}!")
                j = await response.json()
                if j == {} or j == []:
                    log.debug("No ranked info found.")
                else:
                    await self._change(bh, "rating_1v1", j["rating"], self._notify)
                    metal_name, tier_name = j["tier"].split(" ", 1)
                    metal = BrawlhallaMetal[metal_name.upper()]
                    tier = BrawlhallaTier(int(tier_name))
                    rank = BrawlhallaRank(metal=metal, tier=tier)
                    await self._change(bh, "rank_1v1", rank, self._notify)
            await asyncify(db_session.commit)

    async def _updater(self, period: int):
        log.info(f"Started updater with {period}s period")
        while True:
            log.info(f"Updating...")
            session = self.alchemy.Session()
            log.info("")
            steams = session.query(self.alchemy.get(Steam)).all()
            for steam in steams:
                try:
                    await self._update(steam, session)
                except Exception as e:
                    sentry_sdk.capture_exception(e)
                    log.error(f"Error while updating {steam.user.username}: {e}")
                await asyncio.sleep(1)
            await asyncify(session.commit)
            session.close()
            log.info(f"Sleeping for {period}s")
            await asyncio.sleep(period)

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        author = await data.get_author(error_if_none=True)

        found_something = False

        message = ""
        for steam in author.steam:
            await self._update(steam, data.session)
            if steam.brawlhalla is None:
                continue
            found_something = True
            message += self._display(steam.brawlhalla)
            message += "\n"
        if not found_something:
            raise UserError("Nessun account di Brawlhalla trovato.")
        await data.reply(message)
