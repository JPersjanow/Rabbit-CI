from multiprocessing.connection import Listener
from multiprocessing import Process
#library for passing variables through processes
import guli

address = ('127.0.0.1', 5005)

def print_msg(msg):
    print(msg)

def rec_msg(conn):
    msg = conn.recv()
    guli.GuliVariable("msg").setValue(msg)
    

if __name__ == '__main__':
    listener = Listener(address, authkey=b"pass")
    conn = listener.accept()
    
    
    while True:
        proc_get = Process(target=print_msg, args=(guli.GuliVariable("msg").get(),))
        proc_print = Process(target=rec_msg, args=(conn,))
        proc_get.start()
        proc_print.start()
        proc_get.join()
        proc_print.join()
        if guli.GuliVariable("msg").get() == "close":
            conn.close()
            break
    




