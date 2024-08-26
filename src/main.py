from opcua import Server, ua
import time
import threading

server = Server()
server.set_endpoint("opc.tcp://192.168.8.14:4840/freeopcua/server/")
server.set_server_name("OPC UA Simulation Server")

uri = "http://examples.freeopcua.github.io"
idx = server.register_namespace(uri)

# Get the Server node (NodeId 2253)
server_node = server.get_node(ua.ObjectIds.Server)

event_gen_1 = server.get_event_generator(ua.ObjectIds.BaseEventType, server_node)
event_gen_1.event.Severity = 500
event_gen_1.event.Message = ua.LocalizedText("Event 1 from Server Node")
event_gen_1.event.SourceName = "Event1"

event_gen_2 = server.get_event_generator(ua.ObjectIds.BaseEventType, server_node)
event_gen_2.event.Severity = 200
event_gen_2.event.Message = ua.LocalizedText("Event 2 from Server Node")
event_gen_2.event.SourceName = "Event2"


def trigger_event_1():
    while True:
        event_gen_1.trigger()
        print("Event 1 triggered from Server node (i=2253)")
        time.sleep(80)


def trigger_event_2():
    while True:
        event_gen_2.trigger()
        print("Event 2 triggered from Server node (i=2253)")
        time.sleep(110)

server.start()
print(f"Server started at {server.endpoint}")

try:
    thread_1 = threading.Thread(target=trigger_event_1)
    thread_2 = threading.Thread(target=trigger_event_2)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

finally:
    server.stop()
    print("Server stopped")
