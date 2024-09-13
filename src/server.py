import asyncio
from asyncua import ua
from asyncua.server import Server as OPCUAServer, EventGenerator
import pathlib
import json


class Server:
    def __init__(self):
        self.server_endpoint = None
        self.server_name = None
        self.server = None
        self.server_node = None

    def read_settings(self):
        parent = pathlib.Path(__file__).parent.parent
        server_file = parent / "server.json"

        with open(server_file, 'r') as file:
            settings = json.load(file)
            self.server_endpoint = settings['server_endpoint']
            self.server_name = settings['server_name']

            print(f"Settings read: {settings}")

    async def init_server(self):
        self.server = OPCUAServer()

        await self.server.init()
        self.server.set_endpoint(self.server_endpoint)
        self.server.set_server_name(self.server_name)
        self.server_node = self.server.nodes.server

        print(f"Server started at {self.server_endpoint}")

    async def create_event(self, event_name, event_message, event_severity, event_reacurring):
        event_type = await self.server_node.add_object_type(0, event_name)
        await event_type.add_property(0, 'MyIntProperty', ua.Variant(0, ua.VariantType.Int32))
        await event_type.add_property(0, 'MyBoolProperty', ua.Variant(True, ua.VariantType.Boolean))

        event_gen = await self.server.get_event_generator(event_type, self.server_node)
        event_gen.event.Message = ua.LocalizedText(event_message)
        event_gen.event.Severity = int(event_severity)

        print(f"Event created: {event_name}, Message: {event_message}, Severity: {event_severity}")









