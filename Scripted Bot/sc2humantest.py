import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Human


class ScriptedBot(sc2.BotAI):
    async def on_step(self, iteration):
        # what to do every step
        await self.distribute_workers()  # in sc2/bot_ai.py


run_game(maps.get("CatalystLE"), [
    Human(Race.Protoss),
    Bot(Race.Zerg, ScriptedBot())
], realtime=False)