import socket
import time
from multiprocessing import Process, Event

class MachineConnector(Process):
    def __init__(self, change_event: Event, machine_address='localhost'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_address = (machine_address, 5005)
        print(f"SERVER IP: {self.server_address[0]} | SERVER PORT: {self.server_address[1]}")

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.server_address)
        self.sock.setblocking(0)

        self.message = ""
        self.send_message = ""
        Process.__init__(self, target=self.start_connector, args=(change_event,))
    
    def change_send_msg(self, msg: str):
        print("Changing send msg")
        self.send_message = msg

    def start_connector(self, change_event: Event):
        self.sock.listen(1)
        while True:
            print(f"Waiting for connection")
            # time.sleep(10)
            connection, clinet_address = self.sock.accept()
            try:
                print(f"Connection established from: {clinet_address}")

                while True:
                    print(f"SERVER :{self.send_message}")
                    time.sleep(10)

                    if change_event.set():
                        self.change_send_msg("ping wp.pl")

                    # data = connection.recv(1024)
                    # self.message = data
                    # print(f"Received {data}")
                    # if data:
                    #     print("Sedning info back to client")
                    #     connection.send(b"YOU ARE CONNECTED")
                    #     continue
                    # else:
                    #     print("Waiting for client info")

                    if self.send_message != "":
                        print(f"SENDING {self.send_message}")
                        connection.send(bytes(self.send_message))
                    else:
                        print("NO CHANGE")
                        continue

            except Exception as e:
                print(e)
            finally:
                print("CLOSED")
                connection.close()
                break