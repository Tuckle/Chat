import socket,thread,threading,sqlite3

global users
global connections
global index
global s

users = dict()
print_lock=threading.Lock()
index=0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def StopServer():
    s.close()
    return

def PrintMenu():
    menu_list=["1.Start Server","2.Exit"]
    with print_lock:
        for item in menu_list:
            print item
    return

def GetInputFromMenu():
    while True:
       with print_lock:
           try:
                choice=int(raw_input("Input your choice: "))
                if(choice<=2 and choice >=1):
                    break
                else:
                    print "Please input a valid choice!"
           except ValueError:
                print "Please input a valid choice!"
    return choice

def PrintStartMenu():
    menu_list=["1.Stop Server","2.Print online member","3.Exit"]
    with print_lock:
        for item in menu_list:
           print item
    return

def GetInputFromStartMenu():
    while True:
       with print_lock:
           try:
                choice=int(raw_input("Input your choice: "))
                if(choice<=3 and choice >=1):
                    break
                else:
                    print "Please input a valid choice!"
           except ValueError:
                print "Please input a valid choice!"
    return choice

def StartMenu():
    ok =False
    while ok is False:
        PrintStartMenu()
        choice=GetInputFromStartMenu()
        if(choice == 1):
            StopServer()
            ok=True
        elif choice ==2:
            PrintOnlineMembers()
        elif choice == 3:
            StopServer()
            ok = True
            exit()
    main()

def Encode(str):
    
    return str

def Decode(str):

    return str

def Send(connection_string,msg):
    msg=Encode(msg)
    connection_string.send(msg)

def Receive(connection_string):
    msg=connection_string.recv(16)
    msg=Decode(msg)
    return msg

def GetData(connection_string,address_string):

    return

def CheckCredentials(connection_string,address_string):
    name = Receive(connection_string)
    password = Receive(connection_string)

def CreateDataBase():
    dbpath = "users.db"
    try:
        db = open(dbpath, "w")#creating database if not exists
        db.close()

        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Members(ip TEXT, username TEXT, password TEXT, realname TEXT);")
        c.execute("CREATE TABLE IF NOT EXISTS Online(username TEXT, ip TEXT, id TEXT);")
        c.close()
        conn.close()
    except Exception:
        pass

def LogInOrSignUp(connection_string,address_string):
    msg=Receive(connection_string)
    if msg == "00000004":
        if CheckCredentials(connection_string,address_string) == True:
            Send(connection_string,"00000001")
            t=threading.Thread(target = GetData,args=(connection_string,address_string))
            t.daemon=True
            t.start()
            while True:
                pass
        else:
            Send(connection_string,"00000002")
            connection_string.close()
    elif msg == "00000005":
        error = CreateNewUser(connection_string)
        if error == 1:
            Send(connection_string,"00000006")
            connection_strgin.close()
        elif error == 2:
            Send(connection_string,"00000007")
        elif error == 3:
        

def StartSever():
    HOST=''
    PORT=50000
    s.bind((HOST,PORT))
    CreateDataBase()
    with print_lock:
        print "Sever Started!"
    t=threading.Thread(target=StartMenu,name="Start Menu")
    t.daemon=True
    t.start()
    while True:
        s.listen(1)
        connection_string,address_string=s.accept()
        t=threading.Thread(target = LogInOrSignUp,args=(connection_string,address_string))
        t.daemon=True
        t.start()

def Select(choice):
    if(choice == 1):
        t=threading.Thread(target = StartSever,name="Start Sever")
        t.start()
    elif(choice == 2):
        exit()

def main():
    PrintMenu()
    choice=GetInputFromMenu()
    Select(choice)
    
main()