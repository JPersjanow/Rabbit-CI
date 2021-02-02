from multiprocessing.connection import Client
address = ('localhost', 6000)
conn = Client(address, authkey=b"pass")
try:
    conn.send(str("DUPA"))
except Exception as e:
    print(e)
finally:
    conn.close()