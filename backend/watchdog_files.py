import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from multiprocessing.connection import Client
import guli
import os

from tools.config_reader import ConfigReader
from tools.xml_tools import return_xml_attribute_value

config = ConfigReader()

def send(cmd):
    address = ('127.0.0.1', 5005)
    conn = Client(address, authkey=b"pass")
    try:
        conn.send(str(cmd))
    except Exception as e:
        print(e)
    finally:
        conn.close()


def on_created(event):
    print(f"{event.src_path} has been created")
    guli.GuliVariable("on_created").setValue(event.src_path)


def on_deleted(event):
    print(f"{event.src_path} deleted")
    guli.GuliVariable("on_created").setValue(event.src_path)


def on_modified(event):
    print(f"{event.src_path} has been modified")
    command = return_xml_attribute_value(xml_file=event.src_path, attribute_name="cmd")
    print(f"Sending command {command}")
    guli.GuliVariable("on_modified").setValue("true")


def on_moved(event):
    print(f"moved {event.src_path} to {event.dest_path}")
    guli.GuliVariable("on_created").setValue(event.src_path)


if __name__ == "__main__":
    
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

    path = config.jobs_directory
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()

    
    try:
        while True:
            print(guli.GuliVariable("on_modified").get())
            if guli.GuliVariable("on_modified").get() == "true":
                print("OK!")
                send(cmd="hello")
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()