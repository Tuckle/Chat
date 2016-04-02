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
        choice=GetInputFromStartMenu()
        if(choice == 1):
            StopServer()
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

def CheckCredentials(connection_string, address_string):
    name = Receive(connection_string)
    password = Receive(connection_string)
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("SELECT username, password FROM Members WHERE username='%s'" % (name))
        data = c.fetchall()
        c.close()
        conn.close()
        
        if len(data) == 0 or data[0][1] != password:
            return False
        return True
    except Exception:
        return False

def CreateNewUser(connection_string, address_string):
    username = Receive(connection_string)
    password = Receive(connection_string)
    realname = Receive(connection_string)

    if len(username) == 0 or len(password) == 0 or len(realname) == 0:
        return 2 #basic check gone wrong

    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("SELECT username, password FROM Members WHERE username='%s';", (username))
        data = c.fetchall()
        if len(data) != 0:
            c.close()
            conn.close()
            return 4 #username already exists
        c.execute("INSERT into Members values('%s', '%s', '%s', '%s');", address_string, username, password, realname)
        c.commit()
        c.close()
        conn.close()
        return 1 #username added successfuly
    except Exception:
        return 3 #not being able to check in database

def CheckCredential(connection_string,address_string):
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

def CreateDataBase():#option to create a database on the host and use that database
    dbpath = "users.db"
    try:
        db = open(dbpath, "w")#creating database if not exists
        db.close()

        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Members(ip TEXT, username TEXT, password TEXT, realname TEXT);")
        c.execute("CREATE TABLE IF NOT EXISTS Online(username TEXT, ip TEXT, id TEXT);")
        c.commit()
        c.close()
        conn.close()
    except Exception:
        pass

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