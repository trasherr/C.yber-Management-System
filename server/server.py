# server
import socket
import server_func as sf
import PySimpleGUI as sg
import threading
import time
from win32api import GetSystemMetrics as gsys

c=[]
######################### Connection #################################

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = "127.0.0.1"  # ip of socket
port=8080           # port no of socket

s.bind((host,port)) # creating socket

s.listen(5)         # listening for connections
print("listening...")

#######################################################################

def recieve():
    while True:
        connection, addr = s.accept()  # Establish connection with client.
        print('Got connection from', addr)
        connection.send("Thank you for connecting".encode())
        thread=threading.Thread(target=server,args=(connection,))
        thread.start()

def serverGUI():

    sg.theme("DarkBlack")
    layout=[
        [sg.Text("Welcome to Cafe Management System",font="Ariel 32")],
        [sg.Frame(layout=[
            [sg.Text("",size=(2,2))],
            [sg.Text("",size=(2,2)),sg.Multiline(key="orders",size=(30,30)),sg.Text("",size=(2,2))],
            [sg.Text("",size=(2,2))]
        ],title="Orders"
        ),
        sg.Frame(layout=[
            [sg.Text("")],
            [sg.Text("",size=(10,2)),sg.Button("Add Item",size=(10,2),font="Ariel 12"),sg.Text("",size=(10,2))],
            [sg.Text("",size=(10,2)),sg.Button("Exit",size=(10,2),font="Ariel 12"),sg.Text("",size=(10,2))],
            [sg.Text("")]
        ], title="Options"
        )]
    ]
    window=sg.Window('Server',layout, size=(gsys(0), gsys(1)),element_justification='c')
    while True:
        ord = sf.s_orders()
        event,values=window.Read()
        #print(ord)
        window["orders"].update(ord)
        if(event=="Exit" or event == sg.WIN_CLOSED):
            if (sg.popup_ok_cancel("Are you sure you want to exit ? ", keep_on_top=True)=="OK"):
                break
    window.Close()
    exit(1)


def server(c):
    while True :


        ########################### Menu ##############################
        print ("menu")

        menu=c.recv(32).decode()
        print(menu)
        ###################### Login ########################

        if menu=='Login':

            auth=c.recv(1024).decode()
            print(auth)
            authenticate=sf.authenticate(auth)
            print(authenticate)
            c.send(str(authenticate).encode())
            if(authenticate!="Incorrect Username or Password"):
                while True:
                    log_choice=c.recv(128).decode()

                    if (log_choice == 'Order'):
                        drinks, d_cost, food, f_cost = sf.order()

                        time.sleep(0.5)
                        c.send(str(drinks).encode())
                        time.sleep(0.5)
                        print('drinks', drinks)
                        c.send(str(food).encode())
                        time.sleep(0.5)
                        print('food', food)
                        c.send(str(d_cost).encode())
                        time.sleep(0.5)
                        print('d_cost', d_cost)
                        c.send(str(f_cost).encode())
                        time.sleep(0.5)
                        print('f_cost', f_cost)

                        cus_dets=c.recv(1024).decode()
                        ordered=c.recv(2048).decode()
                        if(cus_dets!='No' and ordered!='Orders'):
                            sf.ordering(cus_dets,ordered)

                        continue

                    elif (log_choice == 'Order History'):
                        cus_dets=c.recv(256).decode()
                        history=sf.order_history(cus_dets)
                        c.send(str(history).encode())
                        continue

                    elif (log_choice=='View Details'):
                        auth = c.recv(1024).decode()
                        print(auth)
                        authenticate = sf.authenticate(auth)
                        c.send(str(authenticate).encode())
                        continue

                    elif(log_choice == 'Edit Details'):
                        edit_det=c.recv(1024).decode()
                        sf.edit(edit_det)
                        continue

                    elif (log_choice == 'Change Password'):
                        while True:
                            curr_pass=str(c.recv(1024).decode())
                            if curr_pass=='error code 913372':
                                break
                            check=sf.authenticate(curr_pass)
                            print (check)
                            if(check=="Incorrect Username or Password"):
                                c.send("False".encode())
                                continue

                            else:
                                c.send("True".encode())
                                new_pass = str(c.recv(1024).decode())
                                print(new_pass)
                                sf.chng_pass(new_pass, curr_pass)
                                break
                        continue

                    elif (log_choice == 'Feedback'):
                        feed=str(c.recv(4096).decode())
                        print("feed = ", feed)
                        sf.feedback(feed)
                        continue

                    elif (log_choice == 'Loggout' or log_choice==sg.WIN_CLOSED):
                        out=bool(c.recv(128).decode())
                        print("logg out = ",out)
                        if out == True:
                            print("Logging out")
                            break
                        else:
                            continue
                    break
        ######################################################

        ###################### Create account ########################

        elif menu=='Create Account':
            while True:
                usr=c.recv(32).decode()
                print(usr)
                if usr!="cancel code 913372":
                    check=sf.check(usr)
                    c.send(str(check).encode())
                    if check=="true":
                        print("Creating acc")
                        crd=c.recv(1024).decode()
                        print (crd)
                        if (crd != "return code 913372"):
                            new_acc=sf.new_acc(crd)
                            c.send(new_acc.encode())
                            break
                    else :
                        continue
                else:
                    break
        ##############################################################

        elif menu == 'Exit' or menu == sg.WIN_CLOSED:
            ext=bool(c.recv(32).decode())
            print("Exit = ")
            if (ext=='Cancel'):
                print(ext)
                break
            else:
                print(ext)

        ######################## Menu end #############################
        print(menu)
        cont=bool(c.recv(8).decode())
        print("cont = ",cont)

        if cont==True:
            continue
        if cont==False:
            c.close() # Close
            break

threading.Thread(target=serverGUI()).start()
threading.Thread(target=recieve()).start()