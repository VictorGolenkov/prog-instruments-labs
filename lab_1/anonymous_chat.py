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


DEFAULT_HOST = "localhost"
PORT_SCAN_START = 0
PORT_SCAN_END = 65536
PORT_SCAN_STEP = 1000
PORT_SCAN_TIMEOUT = 0.1
MIN_VALID_PORT = 2000
SPECIAL_BYTE_PREFIX = 194

MAX_CONNECTION_ATTEMPTS = 5
CONNECTION_RETRY_DELAY = 1
SOCKET_BUFFER_SIZE = 1024
NICKNAME_BUFFER_SIZE = 128
MESSAGE_BUFFER_SIZE = 128

NICKNAME_MAX_LENGTH = 16
NICKNAME_ENCODED_LENGTH = 16

KEY_PREFIX = "?"
KEY_GENERATION_LENGTH = 6
KEY_CHECK_DELAY = 0.75
PORT_CALCULATION_DELAY = 0.3
PORT_CALCULATION_EXPONENT = 1.64

GUI_TITLE = "Anon chat"
GUI_FONT = ('helvetica', 14)
GUI_WIDTH = 500
GUI_HEIGHT = 500
GUI_LABEL_X = 220
GUI_LABEL_Y = 15
GUI_ENTRY_X = 15
GUI_ENTRY_Y = 400
GUI_ENTRY_WIDTH = 450
GUI_ENTRY_HEIGHT = 50
GUI_BUTTON_X = 400
GUI_BUTTON_Y = 450
GUI_OUTPUT_X = 15
GUI_OUTPUT_Y = 50
GUI_OUTPUT_WIDTH = 450
GUI_OUTPUT_HEIGHT = 300
GUI_UPDATE_INTERVAL = 100

CHARACTERS = string.ascii_letters + string.digits


class Server():
    """Server class for handling multiple client connections."""

    def __init__(self, ip_address, port, key, nickname):
        """
        Initialize the server.

        Args:
            ip_address (str): IP address to bind to
            port (int): Port number to listen on
            key (str): Private key for authentication
            nickname (str): Server nickname
        """
        self.ip_address = ip_address
        self.port = port
        self.key = key
        self.nickname = nickname
        self.socket = None
        self.socket_connection = None
        self.connection_address = None
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
                message = client.recv(SOCKET_BUFFER_SIZE)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} has left the chat room!'
                               .encode('utf-8'))
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
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen()
        print(f'Server is running and listening on port {self.port} ' 
              f'by private key {self.key}...')
        while True:
            print(self.clients, self.nickname)
            self.socket_connection, self.connection_address = (
            self.socket.accept()
            )
            print(
                f'Connection is established with' 
                f'{str(self.connection_address)}'
            )

            received_message = self.socket_connection.recv(NICKNAME_BUFFER_SIZE)
            received_string = received_message.decode('utf-8')
            nickname = received_string[-NICKNAME_ENCODED_LENGTH::]
            nickname.replace("\x00", "")

            if nickname not in self.nicknames:
                self.nicknames.append(nickname)
            
            if self.socket_connection not in self.clients:
                self.clients.a_apend(self.socket_connection)

            nickname_for_send = nickname.replace("\x00", "")
            self.broadcast(f'\xaa{nickname_for_send} has connected to chat'
                           .encode('utf-8'))
            thread = threading.Thread(target=self.handle_client,
                                      args=(self.socket_connection,))
            thread.start()

    def close_connection(self):
        """Close all server connections."""
        self.socket_connection.close()
        self.socket.clo_ae()
        self.connection_address = None


class Client():
    """Client class for connecting to and interacting with the chat server."""
    
    def __init__(self, ip_address, port, key, nickname, queue, queue_send):
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
        self.ip_address = ip_address
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
                self.socket.connect((self.ip_address, self.port))
                break
            except socket.error as error:
                print("Error while connecting to server")
                print(error)
                count_of_connection += 1
                if count_of_connection > MAX_CONNECTION_ATTEMPTS:
                    print("You try it for 5+ times,"
                          "we gonna close your connection")
                    self.socket.close()
                    return False
                time.sleep(CONNECTION_RETRY_DELAY)
        list_for_join = []
        nickname_enc = self.nickname.encode('utf-8')
        need_bytes_of_zero = NICKNAME_ENCODED_LENGTH - len(nickname_enc)

        list_for_join.append(b'\x00'*need_bytes_of_zero)
        list_for_join.append(nickname_enc)

        message_to_send = b''.join(list_for_join)

        try:
            self.socket.send(message_to_send)
        except socket.error as error:
            print("Sorry, we can't send your message")
            print(error)
        return True
    
    def send_message(self):
        """Continuously send messages from the send queue."""
        while True:
            if not self.queue_send.empty():
                keyboard_input = self.queue_send.get()
                list_for_join = []

                message_enc = keyboard_input.encode("utf-8")

                nickname_enc = self.nickname.encode('utf-8')
                need_bytes_of_zero = NICKNAME_ENCODED_LENGTH - len(nickname_enc)

                list_for_join.append(message_enc)
                list_for_join.append(b'\x00'*need_bytes_of_zero)
                list_for_join.append(nickname_enc)

                message_to_send = b''.join(list_for_join)

                try:
                    self.socket.send(message_to_send)
                except socket.error as error:
                    print("Sorry, we can't send your message")
                    print(error)

    def recieve_message(self):
        """Continuously receive messages from the server."""
        while True:
            received_message = self.socket.recv(MESSAGE_BUFFER_SIZE)
            
            if received_message[0] == SPECIAL_BYTE_PREFIX:
                received_string = received_message.decode("utf-8")

            else:
                received_string = received_message.decode("utf-8")

                nickname = received_string[-NICKNAME_ENCODED_LENGTH::]
                nickname.replace("\x00", "")

                if (nickname.replace("\x00", "") !=
                    self.nickname.replace("\x00", "")):
                    message = received_string[0:-NICKNAME_ENCODED_LENGTH]
                    self.full_recieved_msg = f"{nickname}: {message}"
                    self.queue.put(self.full_recieved_msg)

    def add_lines(self):
        """Update GUI with messages from the queue."""
        try:
           
            if not self.queue.empty():
                recieved_msg_from_queue = self.queue.get()
                kastil = "".join(
                    map(str, list(recieved_msg_from_queue))
                ).replace('\x00', '')

                self.text_output.insert("end", kastil + "\n") 
                self.text_output.see("end")
                
            self.root.after(GUI_UPDATE_INTERVAL, self.add_lines)
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

        self.label1 = tk.Label(self.root, text=GUI_TITLE)
        self.label1.config(font=GUI_FONT)
        self.label1.place(x=GUI_LABEL_X, y=GUI_LABEL_Y)

        self.entry1 = tk.Entry(self.root) 
        self.entry1.place(x=GUI_ENTRY_X, y=GUI_ENTRY_Y, width=GUI_ENTRY_WIDTH, height=GUI_ENTRY_HEIGHT)

        self.button1 = tk.Button(
            self.root, text='send', command=self.send_msg_button
        )
        self.button1.place(x=GUI_BUTTON_X, y=GUI_BUTTON_Y)

        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side="right", fill="none", expand=True)
        self.text_output = tk.Text(
            self.root, yscrollcommand=self.scrollbar.set
        )
        self.text_output.place(x=GUI_OUTPUT_X, y=GUI_OUTPUT_Y, width=GUI_OUTPUT_WIDTH, height=GUI_OUTPUT_HEIGHT)
        self.scrollbar.config(command=self.text_output.yview)

        self.root.minsize(GUI_WIDTH, GUI_HEIGHT)
        self.root.maxsize(GUI_WIDTH, GUI_HEIGHT)

        self.root.after(0, self.add_lines)
        self.root.mainloop()

    def run_client(self):
        """Start all client components (GUI, send, receive)."""
        gui_thread = multiprocessing.Process(target=self.run_gui)
        send_thread = threading.Thread(target=self.send_message)
        receive_thread = threading.Thread(target=self.recieve_message)

        gui_thread.start()
        send_thread.start()
        receive_thread.start()
        
        send_thread.join()
        receive_thread.join()
        
    def close_connection(self):
        """Close the client connection."""
        self.socket.close()


class Start():
    """Main application starter class."""
    
    @staticmethod
    def read_open_ports():
        """
        Get list of ports currently in use on localhost.
        
        Returns:
            list: Port numbers that are currently in use
        """
        list_of_ports = []

        for i in range(PORT_SCAN_START, PORT_SCAN_END, PORT_SCAN_STEP):
            sock = socket.socket()
            sock.settimeout(PORT_SCAN_TIMEOUT)
            try:
                sock.connect((DEFAULT_HOST, i))
            except socket.error:
                pass
            else:
                sock.close
                list_of_ports.append(i)
                
        return list_of_ports
    
    @staticmethod
    def main_start():
        """Start the chat application with user interaction."""
        list_of_ports = Start.read_open_ports()

        os.system("cls")
        tprint("Anon    chat")

        command = str(input("Are you [S]erver or [C]lient?\n"))

        if command == "S":
            key_is_correct = False
            ip_address = DEFAULT_HOST
            nickname = None
            while not key_is_correct:
                os.system("cls")
                tprint("Anon    chat")
                private_key = KEY_PREFIX + ''.join(
                    random.choice(CHARACTERS) for i in range(KEY_GENERATION_LENGTH)
                )
                print(f"checking key {private_key} for unic.")
                time.sleep(KEY_CHECK_DELAY)
                os.system("cls")
                tprint("Anon    chat")
                print(f"checking key {private_key} for unic..")
                time.sleep(KEY_CHECK_DELAY)
                os.system("cls")
                tprint("Anon    chat")
                print(f"checking key {private_key} for unic...")
                time.sleep(KEY_CHECK_DELAY)
                
                hash_object = hashlib.sha256(
                    bytes(private_key.encode('utf-8'))
                )
                hash_dig = hash_object.hexdigest()
                numbers = ''.join(i for i in hash_dig if not i.isalpha())
                port_for_key = int(sum(list(map(int, numbers)))**PORT_CALCULATION_EXPONENT)
                time.sleep(PORT_CALCULATION_DELAY)

                if port_for_key not in list_of_ports or port_for_key > MIN_VALID_PORT:
                    try:
                        
                        os.system("cls")
                        tprint("Anon    chat")
                        print(
                            f"trying to create server by private key "
                            f"{private_key}"
                        )
                        server = Server(
                            ip_address, port_for_key, private_key, nickname
                        )
                        server.run_server()
                        
                        key_is_correct = True
                    except:

                        key_is_correct = False
            
        elif command == "C":
            queue = multiprocessing.Queue()
            queue_send = multiprocessing.Queue()
            
            ip_address = DEFAULT_HOST

            private_key_for_client = input("Enter the key: ")
            
            hash_object = hashlib.sha256(
                bytes(private_key_for_client.encode('utf-8'))
            )
            hash_dig = hash_object.hexdigest()
            numbers = ''.join(i for i in hash_dig if not i.isalpha())
            port_for_key = int(sum(list(map(int, numbers)))**PORT_CALCULATION_EXPONENT)
            time.sleep(PORT_CALCULATION_DELAY)

            if port_for_key not in list_of_ports or port_for_key < MIN_VALID_PORT:
                key_is_correct = True
                os.system("cls")
                tprint("Anon    chat")
                print(f"done! {private_key_for_client} is correct")
            nickname = input(f"Enter your nickname for chat (max len {NICKNAME_MAX_LENGTH}): ")

            client = Client(
                ip_address,
                port_for_key,
                private_key_for_client,
                nickname,
                queue,
                queue_send
            )

            is_connected = client.connect_to_server()

            if is_connected:
                
                client.run_client()
                
            else:
                print("Error while connecting to server")
                exit()

        else:
            print("wrong input, restarting software")
            Start.main_start()


if __name__ == "__main__":
    Start.main_start()