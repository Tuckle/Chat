import socket,thread,threading,sqlite3,struct

print_lock=threading.Lock()

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

def Receive(connection_string,length=16):
    msg=connection_string.recv(length)
    if not msg:
        return False
    else:
        msg=Decode(msg)
        return str(msg)

def GetData(connection_string,address_string):
    msg=Receive(connection_string,1024)
    if not msg:
        return
    return

def CheckCredentials(connection_string, address_string):
    name = Receive(connection_string)
    password = Receive(connection_string)
    print name
    print password
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

        c.execute("SELECT username, password FROM Members WHERE username='%s';" % (username))
        data = c.fetchall()
        if len(data) != 0:
            c.close()
            conn.close()
            return 4 #username already exists
        c.execute("INSERT INTO Members VALUES('%s', '%s', '%s', '%s');" % (address_string[0], username, password, realname))
        conn.commit()
        c.close()
        conn.close()
        return 1 #username added successfuly
    except Exception as error:
        return 3 #not being able to check in database

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

def LogInOrSignUp(connection_string,address_string):
    msg=Receive(connection_string)
    if not msg:
        return
    else:
        print msg
        if msg == "00000004":
            if CheckCredentials(connection_string,address_string) == True:
                Send(connection_string,"00000001")
                t=threading.Thread(target = GetData,args=(connection_string,address_string))
                t.daemon=True
                t.start()
                while t.is_alive():
                    pass
            else:
                Send(connection_string,"00000002")
                connection_string.close()
        elif msg == "00000005":
            error = CreateNewUser(connection_string,address_string)
            print error
            if error == 1:
                Send(connection_string,"00000006")
                connection_strgin.close()
            elif error == 2:
                Send(connection_string,"00000008")
            elif error == 3:
                Send(connection_string,"00000009")
            elif error ==4:
                Send(connection_string,"00000007")
            connection_string.close()

def StartSever():
    HOST=''
    PORT=40000
    global s
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
        connection_string,address_string = s.accept()
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