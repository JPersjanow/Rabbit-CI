import socket
import time

class MachineConnector:
    def __init__(self, machine_address='localhost'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_address = (machine_address, 5005)
        print(f"SERVER IP: {self.server_address[0]} | SERVER PORT: {self.server_address[1]}")

        self.sock.bind(self.server_address)

        self.message = ""
        self.send_message = ""
    
    def start_connector(self):
        self.sock.listen(1)

        while True:
            print(f"Waiting for connection")
            # time.sleep(10)
            connection, clinet_address = self.sock.accept()
            try:
                print(f"Connection established from: {clinet_address}")

                while True:
                    data = connection.recv(16)
                    self.message = data
                    print(f"Received {data}")
                    if data:
                        print("Sedning info back to client")
                        connection.send(b"YOU ARE CONNECTED")
                    else:
                        break

                    if self.send_message != "":
                        connection.send(bytes(self.send_message))
            except Exception as e:
                print(e)
            finally:
                connection.close()