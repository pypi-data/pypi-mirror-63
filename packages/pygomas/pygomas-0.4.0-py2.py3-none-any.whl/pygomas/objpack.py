import json

from loguru import logger

from .ontology import X, Y, Z, PERFORMATIVE, PERFORMATIVE_PACK_LOST, TEAM
from .config import TEAM_AXIS
from .pack import Pack, PACK_OBJPACK
from .vector import Vector3D
from spade.behaviour import CyclicBehaviour
from spade.template import Template


class ObjectivePack(Pack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_taken = False
        self.origin = Vector3D()

    def set_taken(self, is_taken):
        self.is_taken = is_taken

    async def setup(self):
        self.type = PACK_OBJPACK
        self.origin.x = self.position.x
        self.origin.y = self.position.y
        self.origin.z = self.position.z
        t = Template()
        t.set_metadata(PERFORMATIVE, PERFORMATIVE_PACK_LOST)
        self.add_behaviour(self.PackLostResponderBehaviour(), t)

        await super().setup()

    async def perform_pack_taken(self, content):
        logger.info("[{}]: Objective Taken!!".format(self.name))
        content = json.loads(content)
        team = content[TEAM]

        if team == TEAM_AXIS:
            self.is_taken = False
            self.position.x = self.origin.x
            self.position.y = self.origin.y
            self.position.z = self.origin.z
        else:
            self.is_taken = True

    class PackLostResponderBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=1000000)
            if msg:
                self.agent.is_taken = False
                content = json.loads(msg.body)
                self.agent.position.x = float(content[X])
                self.agent.position.y = float(content[Y])
                self.agent.position.z = float(content[Z])
