import asyncio
import logging
from asyncua import ua
from asyncua.server import Server, EventGenerator

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


async def event_generator_1(myevgen: EventGenerator):
    count = 0
    while True:
        await asyncio.sleep(5)  # Wait for 5 seconds
        myevgen.event.Message = ua.LocalizedText(f"Event 1 - Count {count}")
        myevgen.event.Severity = count
        myevgen.event.MyNumericProperty = count
        myevgen.event.MyStringProperty = f"String {count}"
        await myevgen.trigger()  # Trigger the event
        print(f"Generated Event 1 at count {count}")
        count += 1


async def event_generator_2(mysecondevgen: EventGenerator):
    count = 0
    while True:
        await asyncio.sleep(10)  # Wait for 10 seconds
        await mysecondevgen.trigger(message=f"Event 2 - Count {count}")
        print(f"Generated Event 2 at count {count}")
        count += 1


async def main():
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # Use the Server node (i=2253)
    server_node = server.nodes.server

    # Creating the first custom event type
    etype = await server.create_custom_event_type(
        server_node.nodeid.NamespaceIndex, 'MyFirstEvent', ua.ObjectIds.BaseEventType,
        [('MyNumericProperty', ua.VariantType.Float),
         ('MyStringProperty', ua.VariantType.String)]
    )
    myevgen = await server.get_event_generator(etype, server_node)

    # Creating the second custom event type
    custom_etype = await server.nodes.base_event_type.add_object_type(2, 'MySecondEvent')
    await custom_etype.add_property(2, 'MyIntProperty', ua.Variant(0, ua.VariantType.Int32))
    await custom_etype.add_property(2, 'MyBoolProperty', ua.Variant(True, ua.VariantType.Boolean))
    mysecondevgen = await server.get_event_generator(custom_etype, server_node)

    # Start the server and run both event generators concurrently
    async with server:
        await asyncio.gather(
            event_generator_1(myevgen),
            event_generator_2(mysecondevgen)
        )

if __name__ == "__main__":
    asyncio.run(main())
