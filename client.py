import socket
from threading import Thread
from tkinter import *

# nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)
        
        self.pls = Label(self.login,
					text = "Please login to continue",
					justify = CENTER,
					font = "Helvetica 14 bold")
        self.pls.place( relheight = 0.15,
                        relx = 0.2,
                        rely = 0.07)

        self.labelName = Label(self.login,
							text = "Name: ",
							font = "Helvetica 12")
        self.labelName.place(   relheight = 0.2,
							    relx = 0.1,
							    rely = 0.2)

        self.entryName = Entry(self.login,
							font = "Helvetica 14")
        self.entryName.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.2)
        self.entryName.focus()

        self.go = Button(self.login,
						text = "CONTINUE",
						font = "Helvetica 14 bold",
						command = lambda: self.goAhead(self.entryName.get()))
        self.go.place(  relx = 0.4,
					    rely = 0.55)
        
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        #self.name = name
        self.layout(name)
        rcv = Thread(target=self.receive)
        rcv.start()

    def layout(self, name):
        self.name = name
        # deiconify() raises the chat window and gives it the focus after toplevel window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#d6c4f2")

        self.labelHead = Label(self.Window, bg="#d6c4f2", fg="black", text=self.name, font="Helvetica 13 bold", pady=5)
        self.labelHead.place(relwidth=1)

        self.line = Label(self.Window, width=450, bg="#f5f0cb")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textArea = Text(self.Window, width=20, height=2, bg="#cbdff5", fg="black", font="Helvetica 14", padx=5, pady=5)
        self.textArea.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBottom = Label(self.Window, bg="#cbdff5", height=80)
        self.labelBottom.place(relwidth=1, rely=0.825)

        self.entryMsg = Entry(self.labelBottom, bg="#dcf5cb", fg="black", font="Helvetica 13")
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom, text="Send", font="Helvetica 10 bold", width=20, fg="#fad1af", bg="#5e6b91", command=lambda:self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        self.textArea.config(cursor="arrow")

        # since scrollbar is for the textArea and is NOT a direct componnet of a class, that is why there's no self
        scrollbar = Scrollbar(self.textArea)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textArea.yview)

    def sendButton(self, msg):
        self.textArea.config(state=DISABLED) # making textArea READ-ONLY
        self.msg = msg
        self.entryMsg.delete(0, END) # deleting ALL text on entryMsg
        send = Thread(target=self.write)
        send.start()

    def show_message(self, message):
        self.textArea.config(state=NORMAL)
        self.textArea.insert(END, message+"\n\n")
        self.textArea.config(state=DISABLED)
        # ensures you see the END of the text (most recent msgs)
        self.textArea.see(END)

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.show_message(message)
            except:
                print("An error occured!")
                client.close()
                break

    def write(self):
        self.textArea.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode('utf-8'))
            self.show_message(message) # placing your text on textArea
            break

g = GUI()

# def write():
#     while True:
#         message = '{}: {}'.format(nickname, input(''))
#         client.send(message.encode('utf-8'))

# receive_thread = Thread(target=receive)
# receive_thread.start()
# write_thread = Thread(target=write)
# write_thread.start()