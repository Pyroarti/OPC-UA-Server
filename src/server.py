import asyncio
from asyncua import ua
from asyncua.server import Server as OPCUAServer, EventGenerator
import pathlib
import json
import threading

from create_logger import setup_logger


class Server:
    def __init__(self):
        self.server_endpoint = None
        self.server_name = None
        self.server = None
        self.server_node = None
        self.myfloat = None
        self.mybool = None
        self.myint = None
        self.idx = None

        self.logger = setup_logger(__name__)


    def read_settings(self):
        parent = pathlib.Path(__file__).parent.parent
        server_file = parent / "server.json"

        with open(server_file, 'r') as file:
            settings = json.load(file)
            self.server_endpoint = settings['server_endpoint']
            self.server_name = settings['server_name']

            self.logger.info(f"Settings read: {settings}")


    async def init_server(self):
        self.server = OPCUAServer()

        await self.server.init()
        self.server.set_endpoint(self.server_endpoint)
        self.server.set_server_name(self.server_name)
        self.server_node = self.server.nodes.server

        self.logger.info(f"Server started at {self.server_endpoint}")

        uri = "http://example.URI.io"
        self.idx = await self.server.register_namespace(uri)

        myobj = await self.server.nodes.objects.add_object(self.idx, "MyObject")

        self.myfloat = await myobj.add_variable(self.idx, "MyVariable", 0.1)
        await self.myfloat.set_writable()

        self.mybool = await myobj.add_variable(self.idx, "MyBoolean", True)
        await self.mybool.set_writable()

        self.myint = await myobj.add_variable(self.idx, "MyInteger", 0)
        await self.myint.set_writable()

    async def create_event(self, event_name, event_message, event_severity, event_reacurring):
        event_type = await self.server_node.add_object_type(0, event_name)
        await event_type.add_property(0, 'MyIntProperty', ua.Variant(0, ua.VariantType.Int32))
        await event_type.add_property(0, 'MyBoolProperty', ua.Variant(True, ua.VariantType.Boolean))

        event_gen = await self.server.get_event_generator(event_type, self.server_node)
        event_gen.event.Message = ua.LocalizedText(event_message)
        event_gen.event.Severity = int(event_severity)

        print(f"Event created: {event_name}, Message: {event_message}, Severity: {event_severity}")

    async def run_server(self):
        # Initialize the server and setup address space
        await self.init_server()

        bool_state = True  # Initial state of the boolean
        int_counter = 0  # Initial value for the integer
        try:
            async with self.server:
                while True:
                    await asyncio.sleep(1)

                    # Increment the value of MyVariable (float)
                    current_value = await self.myfloat.get_value()
                    new_value = current_value + 0.1
                    await self.myfloat.write_value(new_value)

                    # Toggle the boolean value
                    bool_state = not bool_state
                    await self.mybool.write_value(bool_state)

                    # Increment the integer value
                    int_counter += 1
                    await self.myint.write_value(int_counter)

                    print(f"Updated MyVariable: {new_value}, MyBoolean: {bool_state}, MyInteger: {int_counter}")
        except KeyboardInterrupt:
            print("Server stopped by user.")
            self.server.stop()

