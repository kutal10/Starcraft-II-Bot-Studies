import sc2
from sc2 import run_game,maps,Race,Difficulty
from sc2.ids.unit_typeid import UnitTypeId
from sc2.player import Bot,Computer
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, CYBERNETICSCORE, STALKER, STARGATE , VOIDRAY , WARPGATE
from sc2.ids.ability_id import AbilityId
from sc2.ids.buff_id import BuffId
from sc2.ids.upgrade_id import UpgradeId
 
import random


class SentdeBot(sc2.BotAI):

    def __init__(self):
        self.ITERATIONS_PER_MINUTE = 165
        self.MAX_WORKERS = 65

    async def on_step(self,iteration):
        self.iteration = iteration
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.build_assimilators()
        await self.expand()
        await self.offensive_force_buildings()
        await self.build_offensive_force()
        await self.attack()
        await self.upgrade_gateway()

    async def build_workers(self):
        nexii = self.townhalls
        for each in nexii:
            if self.units(UnitTypeId.PROBE).amount < self.MAX_WORKERS:
                if self.supply_workers < 16 * nexii.amount and each.is_idle:
                    if self.can_afford(UnitTypeId.PROBE):
                        each.train(UnitTypeId.PROBE)

    async def build_pylons(self):
        if self.supply_left < 5 and not self.already_pending(UnitTypeId.PYLON):
            nexuses = self.structures(UnitTypeId.NEXUS).ready
            if nexuses.exists:
                if self.can_afford(UnitTypeId.PYLON):
                    await self.build(UnitTypeId.PYLON, near=nexuses.first)

    async def build_assimilators(self):

        if self.townhalls.exists:
            nexus = self.townhalls.random

        vitem = self.vespene_geyser.closer_than(15,nexus)
        for vas in vitem: 
            if not self.can_afford(UnitTypeId.ASSIMILATOR):
                break
            worker = self.select_build_worker(vas.position)
            if worker is None:
                break
            if not self.units(ASSIMILATOR).closer_than(1.0,vas).exists:
                self.do(worker.build(ASSIMILATOR,vas))

    async def expand(self):
        if self.townhalls.amount < 3 and self.can_afford(UnitTypeId.NEXUS):
            await self.expand_now()

    async def offensive_force_buildings(self):

        if self.structures(UnitTypeId.PYLON).ready.exists:

            pylon = self.structures(UnitTypeId.PYLON).ready.random

            if self.structures(UnitTypeId.GATEWAY).ready.exists and self.structures(UnitTypeId.CYBERNETICSCORE).amount == 0:
                if self.can_afford(UnitTypeId.CYBERNETICSCORE) and not self.already_pending(UnitTypeId.CYBERNETICSCORE):
                    await self.build(UnitTypeId.CYBERNETICSCORE, near=pylon)

            elif len(self.structures(UnitTypeId.GATEWAY)) < ((self.iteration / self.ITERATIONS_PER_MINUTE)/2):
                if self.can_afford(UnitTypeId.GATEWAY) and not self.already_pending(UnitTypeId.GATEWAY):
                    await self.build(UnitTypeId.GATEWAY, near=pylon)

            if self.structures(UnitTypeId.CYBERNETICSCORE).ready.exists:
                if len(self.structures(UnitTypeId.STARGATE)) < ((self.iteration / self.ITERATIONS_PER_MINUTE)/2):
                    if self.can_afford(UnitTypeId.STARGATE) and not self.already_pending(UnitTypeId.STARGATE):
                        await self.build(UnitTypeId.STARGATE,near=pylon)
    
    async def upgrade_gateway(self):
        if self.structures(UnitTypeId.CYBERNETICSCORE).ready.exists and self.can_afford(AbilityId.RESEARCH_WARPGATE) and self.already_pending_upgrade(UpgradeId.WARPGATERESEARCH) == 0:
            ccore = self.structures(UnitTypeId.CYBERNETICSCORE).ready.first
            ccore.research(UpgradeId.WARPGATERESEARCH)

    async def build_offensive_force(self):
        for gw in self.structures(UnitTypeId.GATEWAY).ready.idle:
            if not self.units(UnitTypeId.STALKER).amount > self.units(UnitTypeId.VOIDRAY).amount:
                if self.can_afford(UnitTypeId.STALKER) and self.supply_left > 0:
                    self.do(gw.train(UnitTypeId.STALKER))

        for wg in self.structures(UnitTypeId.WARPGATE).ready.idle:
            if not self.units(UnitTypeId.STALKER).amount > self.units(UnitTypeId.VOIDRAY).amount:
                if self.can_afford(UnitTypeId.STALKER) and self.supply_left > 0:
                    self.do(wg.train(UnitTypeId.STALKER))

        for sg in self.structures(UnitTypeId.STARGATE).ready.idle:
            if self.can_afford(UnitTypeId.VOIDRAY) and self.supply_left > 0:
                self.do(sg.train(VOIDRAY))

    def find_target(self,state): 
        if len(self.enemy_units) > 0:
            return random.choice(self.enemy_units)
        elif len(self.enemy_structures) > 0:
            return random.choice(self.enemy_structures)
        else:
            return self.enemy_start_locations[0]

    async def attack(self):

        aggressive_units = {STALKER: [15,5],
                           VOIDRAY: [8,3]}

        for UNIT in aggressive_units:
            if self.units(UNIT).amount > aggressive_units[UNIT][0] and self.units(UNIT).amount > aggressive_units[UNIT][1]:
                for s in self.units(UNIT).idle:
                    self.do(s.attack(self.find_target(self.state)))

            elif self.units(UNIT).amount > aggressive_units[UNIT][1]:
                if len(self.enemy_units) > 0:
                    for s in self.units(UNIT).idle:
                        self.do(s.attack(random.choice(self.enemy_units)))

run_game(maps.get("CatalystLE"), [
    Bot(Race.Protoss, SentdeBot()),
    Computer(Race.Zerg, Difficulty.VeryHard)
], realtime=False,)
