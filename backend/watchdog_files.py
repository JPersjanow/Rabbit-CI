import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from multiprocessing.connection import Client
from multiprocessing import Process, Event
import socket
import guli
import os

from tools.config_reader import ConfigReader
from tools.xml_tools import return_xml_attribute_value
from server import MachineConnector

guli.GuliVariable("on_modified").setValue("false")

def start_connector():
    machine_address = 'localhost'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (machine_address, 5005)
    print(f"SERVER IP: {server_address[0]} | SERVER PORT: {server_address[1]}")
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_address)
    # sock.setblocking(0)
    sock.listen(1)
    while True:
        print(f"Waiting for connection")
        time.sleep(10)
        connection, clinet_address = sock.accept()
        try:
            print(f"Connection established from: {clinet_address}")

            while True:
                time.sleep(5)
                # data = connection.recv(1024)
                # print(f"Received {data}")
                # if data:
                #     print("Sedning info back to client")
                #     connection.send(b"YOU ARE CONNECTED")
                #     continue
                # else:
                #     print("Waiting for client info")

                if guli.GuliVariable("on_modified").get() == "true":
                    print("CHANGED!")
                    guli.GuliVariable("on_modified").setValue("false")

                    connection.send(b"/K ping wp.pl")

                        

        except Exception as e:
            print(e)
        finally:
            print("CLOSED")
            connection.close()
            break

def on_created(event):
    print(f"{event.src_path} has been created")
    guli.GuliVariable("on_created").setValue(event.src_path)


def on_deleted(event):
    print(f"{event.src_path} deleted")
    guli.GuliVariable("on_created").setValue(event.src_path)


def on_modified(event):
    guli.GuliVariable("on_modified").setValue("true")


def on_moved(event):
    print(f"moved {event.src_path} to {event.dest_path}")
    guli.GuliVariable("on_created").setValue(event.src_path)


if __name__ == "__main__":

    config = ConfigReader()

    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(
        patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path = config.kanbans_directory
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    mc = Process(target=start_connector)
    
    try:
        my_observer.start()
        mc.start()
            
    except KeyboardInterrupt:
        my_observer.stop()
        mc.join()
        my_observer.join()