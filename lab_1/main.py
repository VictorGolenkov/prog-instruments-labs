"""
Anonymous Chat Application
This module implements a simple peer-to-peer chat system.
"""

import hashlib
import multiprocessing
import os
import random
import socket
import string
import threading
import time
import tkinter as tk

from art import tprint

characters = string.ascii_letters + string.digits

class Server():
    """Server class for handling multiple client connections."""
    
    def __init__(self, ip_adr, port, key, nickname):
        """
        Initialize the server.
        
        Args:
            ip_address (str): IP address to bind to
            port (int): Port number to listen on
            key (str): Private key for authentication
            nickname (str): Server nickname
        """
        self.ip_adr = ip_adr
        self.port = port
        self.key = key
        self.nickname = nickname
        self.socket = None
        self.socketConnection = None
        self.connectionAddress = None
        self.clients = []
        self.nicknames = []

    def handle_client(self, client):
        """
        Handle messages from a single client.
        
        Args:
            client (socket.socket): Client socket connection
        """
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} has left the chat room!'.encode('utf-8'))
                self.nicknames.remove(nickname)
                break

    def broadcast(self, message):
        """
        Send a message to all connected clients.
        
        Args:
            message (bytes): Message to broadcast
        """
        for client in self.clients:
            print(message)
            client.send(message)

    def run_server(self):
        """Start the server and accept incoming connections."""
        self.socket = socket.socket()
        self.socket.bind((self.ip_adr, self.port))
        self.socket.listen()
        print(f'Server is running and listening on port {self.port} by private key {self.key}...')
        while True:
            print(self.clients, self.nickname)
            self.socketConnection, self.connectionAddress = self.socket.accept()
            print(f'connection is established with {str(self.connectionAddress)}')

            receivedMsg = self.socketConnection.recv(128)

            receivedString = receivedMsg.decode('utf-8')

            nickname = receivedString[-16::]
            nickname.replace("\x00", "")

            if nickname not in self.nicknames:
                self.nicknames.append(nickname)
            
            if self.socketConnection not in self.clients:
                self.clients.append(self.socketConnection)

            nickname_for_send = nickname.replace("\x00", "")
            self.broadcast(f'\xaa{nickname_for_send} has connected to chat'.encode('utf-8'))
            thread = threading.Thread(target=self.handle_client, args=(self.socketConnection,))
            thread.start()

    def close_connection(self):
        """Close all server connections."""
        self.socketConnection.close()
        self.socket.close()
        self.connectionAddress = None


class Client():
    """Client class for connecting to and interacting with the chat server."""
    
    def __init__(self, ip_adr, port, key, nickname, queue, queue_send):
        """
        Initialize the client.
        
        Args:
            ip_address (str): Server IP address
            port (int): Server port number
            key (str): Private key for authentication
            nickname (str): Client nickname
            queue (multiprocessing.Queue): Queue for received messages
            queue_send (multiprocessing.Queue): Queue for messages to send
        """
        self.ip_adr = ip_adr
        self.port = port 
        self.key = key
        self.nickname = nickname
        self.socket = None
        self.root = None
        self.label1 = None
        self.button1 = None
        self.scrollbar = None
        self.text_output = None
        self.full_recieved_msg = ''
        self.queue = queue
        self.queue_send = queue_send
        #TODO: queue v __init__ (param) a dalshe hz

    def connect_to_server(self):
        """
        Connect to the chat server.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        self.socket = socket.socket()
        count_of_connection = 0
        while True:
            try:
                self.socket.connect((self.ip_adr, self.port))
                break
            except socket.error as error:
                print("Error while connecting to server")
                print(error)
                count_of_connection += 1
                if count_of_connection > 4:
                    print("You try it for 5+ times, we gonna close your connection")
                    self.socket.close()
                    return False
                time.sleep(1)
        list_for_join = []
        nickname_enc = self.nickname.encode('utf-8')
        need_bytes_of_zero = 16 - len(nickname_enc)

        list_for_join.append(b'\x00'*need_bytes_of_zero)
        list_for_join.append(nickname_enc)

        messageToSend = b''.join(list_for_join)

        try:
            self.socket.send(messageToSend)
        except socket.error as error:
            print("Sorry, we can't send your message")
            print(error)
        return True
    
    def send_message(self):
        """Continuously send messages from the send queue."""
        while True:
            if not self.queue_send.empty():
                keyboardInput = self.queue_send.get()
                list_for_join = []

                message_enc = keyboardInput.encode("utf-8")

                nickname_enc = self.nickname.encode('utf-8')
                need_bytes_of_zero = 16 - len(nickname_enc)

                list_for_join.append(message_enc)
                list_for_join.append(b'\x00'*need_bytes_of_zero)
                list_for_join.append(nickname_enc)

                messageToSend = b''.join(list_for_join)

                try:
                    self.socket.send(messageToSend)
                except socket.error as error:
                    print("Sorry, we can't send your message")
                    print(error)

    def recieve_message(self):
        """Continuously receive messages from the server."""
        while True:
            receivedMsg = self.socket.recv(128)
            
            if receivedMsg[0] == 194:
                receivedString = receivedMsg.decode("utf-8")

            else:
                receivedString = receivedMsg.decode("utf-8")

                nickname = receivedString[-16::]
                nickname.replace("\x00", "")

                if nickname.replace("\x00", "") != self.nickname.replace("\x00", ""):
                    message = receivedString[0:-16]
                    self.full_recieved_msg = f"{nickname}: {message}"
                    self.queue.put(self.full_recieved_msg)

    def add_lines(self):
        """Update GUI with messages from the queue."""
        try:
           
            if not self.queue.empty():
                recieved_msg_from_queue = self.queue.get()
                kastil = "".join(map(str, list(recieved_msg_from_queue))).replace('\x00', '')

                self.text_output.insert("end", kastil + "\n") 
                self.text_output.see("end")  # Scroll to the end of the Text widget
            self.root.after(100, self.add_lines)  # Schedule the next update
        except Exception as ex:
            print(ex)
    
    def send_msg_button(self):
        """Handle send button click event."""
        msg_for_send = self.entry1.get()
        self.queue.put(f'{self.nickname} : {msg_for_send}')
        self.queue_send.put(msg_for_send)
        self.entry1.delete(0, 'end')

    def run_gui(self):
        """Initialize and run the GUI."""
        self.root= tk.Tk()

        self.label1 = tk.Label(self.root, text='Anon chat')
        self.label1.config(font=('helvetica', 14))
        self.label1.place(x=220, y=15)

        self.entry1 = tk.Entry(self.root) 
        self.entry1.place(x=15, y=400, width=450, height=50)

        self.button1 = tk.Button(self.root, text='send', command=self.send_msg_button)
        self.button1.place(x=400, y=450)

        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side="right", fill="none", expand=True)
        self.text_output = tk.Text(self.root, yscrollcommand=self.scrollbar.set)
        self.text_output.place(x=15, y=50, width=450, height=300)
        self.scrollbar.config(command=self.text_output.yview)

        self.root.minsize(500, 500)
        self.root.maxsize(500, 500)

        self.root.after(0, self.add_lines)
        self.root.mainloop()

    def run_client(self):
        """Start all client components (GUI, send, receive)."""
        guiThread = multiprocessing.Process(target=self.run_gui)
        sendThread = threading.Thread(target=self.send_message)
        receiveThread = threading.Thread(target=self.recieve_message)

        guiThread.start()
        sendThread.start()
        receiveThread.start()
        

        sendThread.join()
        receiveThread.join()
        
    def close_connection(self):
        """Close the client connection."""
        self.socket.close()


class Start():
    """Main application starter class."""
    
    def main_start():
        """Start the chat application with user interaction."""
        #### read open ports ####
        list_of_ports = []

        for i in range(0, 65536, 1000):
            s = socket.socket()
            s.settimeout(0.1)
            try:
                s.connect(('127.0.0.1', i))
            except socket.error:
                pass
            else:
                s.close
                list_of_ports.append(i)
        #########################

        os.system("cls")
        tprint("Anon    chat")

        command = str(input("Are you [S]erver or [C]lient?\n"))

        if command == "S":
            key_is_correct = False
            ip_adr = "localhost"
            nickname = None
            while not key_is_correct:
                os.system("cls")
                tprint("Anon    chat")
                private_key = "?" + ''.join(random.choice(characters) for i in range(6))
                print(f"checking key {private_key} for unic.")
                time.sleep(0.75)
                os.system("cls")
                tprint("Anon    chat")
                print(f"checking key {private_key} for unic..")
                time.sleep(0.75)
                os.system("cls")
                tprint("Anon    chat")
                print(f"checking key {private_key} for unic...")
                time.sleep(0.75)
                
                hash_object = hashlib.sha256(bytes(private_key.encode('utf-8')))
                hash_dig = hash_object.hexdigest()
                numbers = ''.join(i for i in hash_dig if not i.isalpha())
                port_for_key = int(sum(list(map(int, numbers)))**1.64)
                time.sleep(0.3)

                if port_for_key not in list_of_ports or port_for_key > 2000:
                    try:
                        
                        os.system("cls")
                        tprint("Anon    chat")
                        print(f"trying to create server by private key {private_key}")
                        server = Server(ip_adr, port_for_key, private_key, nickname)
                        server.run_server()
                        
                        key_is_correct = True
                    except:

                        key_is_correct = False
            
        elif command == "C":
            queue = multiprocessing.Queue()
            queue_send = multiprocessing.Queue()
            
            ip_adr = "localhost"

            private_key_for_client = input("Enter the key: ")
            
            hash_object = hashlib.sha256(bytes(private_key_for_client.encode('utf-8')))
            hash_dig = hash_object.hexdigest()
            numbers = ''.join(i for i in hash_dig if not i.isalpha())
            port_for_key = int(sum(list(map(int, numbers)))**1.64)
            time.sleep(0.3)

            if port_for_key not in list_of_ports or port_for_key < 2000:
                key_is_correct = True
                os.system("cls")
                tprint("Anon    chat")
                print(f"done! {private_key_for_client} is correct")
            nickname = input("Enter your nickname for chat (max len 16): ")

            client = Client(ip_adr, port_for_key, private_key_for_client, nickname, queue, queue_send)

            isConnected = client.connect_to_server()

            if isConnected:
                
                client.run_client()
                
            else:
                print("Error while connecting to server")
                exit()

        else:
            print("wrong input, restarting software")
            Start.main_start()


if __name__ == "__main__":
    Start.main_start()
    
    #TODO: 1. check users by ip
    #      2. create ports for chat by some hash func
   