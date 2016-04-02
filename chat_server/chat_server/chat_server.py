import socket,thread,threading,sqlite3

global users
global connections
global index

users = dict()
print_lock=threading.Lock()
index=0

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
    while True:
        PrintStartMenu()
        GetInputFromStartMenu()

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
    if address_string not in users:
            name = Receive(connection_string)
            if name in users:
                    Send(connection_string,"00000002")
                    return 1            #Invalid name
            else:
                Send(connection_string,"00000001")
                return 0                #Good name
    else:
        return 2                        #Ip alredy loged

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

def StartSever():
    HOST=''
    PORT=50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        if CheckCredentials(connection_string,address_string) == 0:
            Send(connection_string,"00000001")
            new_dict={address_string : name}
            users.update(new_dict)
            new_dict.clear()
            with print_lock:
                print "\""+name+"\"just connected!"
            t=threading.Thread(target = GetData,args=(connection_string,address_string))
            t.daemon=True
            t.start()
        else:
            Send(connection_string,"00000003")
            connection_string.close()

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