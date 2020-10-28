# server
import socket
import server_func as sf
import PySimpleGUI as sg
import threading
import time
import sys
from win32api import GetSystemMetrics as gsys

######################## Global Variables ############################

ad=[]
qt=False

######################### Connection #################################

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = "127.0.0.1"  # ip of socket
port=8080           # port no of socket

s.bind((host,port)) # creating socket

s.listen(5)         # listening for connections
print("listening...")

#######################################################################

def recieve():
    global c,qt,thread
    th = threading.Thread(target=serverGUI)
    th.start()
    while qt==False:
        connection, addr = s.accept()  # Establish connection with client.
        print('Got connection from', addr)
        connection.send("Thank you for connecting".encode())
        thread=threading.Thread(target=server,args=(connection,))
        thread.start()
        ad.append(str(addr))


def serverGUI():
    global ad,qt
    sf.order_menu()
    sg.theme("DarkBlack")
    layout=[
        [sg.Text("")],
        [sg.Text("")],
        [sg.Text("Welcome to Cafe Management System",font="Ariel 32")],
        [sg.Text("")],
        [sg.Frame(layout=[
            [sg.Text("",size=(2,2))],
            [sg.Text("",size=(2,2)),sg.Multiline(key="orders",size=(30,30)),sg.Text("",size=(2,2))],
            [sg.Text("",size=(2,2))]
        ],title="Orders"
        ),sg.Text("",size=(1,1)),
        sg.Frame(layout=[
            [sg.Text("", size=(2, 2))],
            [sg.Text("", size=(2, 2)), sg.Multiline(key="-con-", size=(30, 30)), sg.Text("", size=(2, 2))],
            [sg.Text("", size=(2, 2))]
        ], title="Connections"
            ),sg.Text("",size=(1,1)),
        sg.Frame(layout=[
            [sg.Text("",size=(2,4))],
            [sg.Text("",size=(5,2)),sg.Button("Add Food Item",size=(20,2),font="Ariel 16"),sg.Text("",size=(5,2))],
            [sg.Text("")],
            [sg.Text("")],
            [sg.Text("", size=(5, 2)), sg.Button("Add Drink", size=(20, 2), font="Ariel 16"),
             sg.Text("", size=(5, 2))],
            [sg.Text("")],
            [sg.Text("")],
            [sg.Text("", size=(5, 2)), sg.Button("Remove Item", size=(20, 2), font="Ariel 16"),
             sg.Text("", size=(5, 2))],
            [sg.Text("")],
            [sg.Text("")],
            [sg.Text("",size=(5,2)),sg.Button("Exit",size=(20,2),font="Ariel 16"),sg.Text("",size=(5,2))],
            [sg.Text("",size=(2,4))],
        ], title="Options"
        )]
    ]
    window=sg.Window('Server',layout, size=(gsys(0), gsys(1)),element_justification='c',finalize=True)
    while True:
        ord = sf.s_orders()
        addr=sf.add(ad)
        window["orders"].update(ord)
        window["-con-"].update(addr)

        event, values = window.Read(timeout=5)

        if  event == "Remove Item":

            drinks,d_cost,food,f_cost=sf.order()
            rm = sg.Window('Remove Item', keep_on_top=True, size=(int(gsys(0) / 1.8), int(gsys(1) / 1.5)), element_justification='c')
            layout=[
                [sg.Text("")],
                [sg.Text("Remove Item",font="Ariel 20")],
                [sg.Text("")],
                [sg.Frame(layout=[
                *[[sg.Text("",size=(2,1)),sg.Button(f"{drinks[i]}",font='Ariel 16',size=(15,1)),sg.Text("",size=(2,1))]for i in range (0,len(drinks))],
                *[[sg.Text("", font='Ariel 16',size=(2,1)), ] for i in range(0, 10 - len(drinks))]
                ],title="Drinks"),
                    sg.Frame(layout=[
                        *[[sg.Text("",size=(2,1)),sg.Button(f"{food[i]}", font='Ariel 16',size=(15,1)),sg.Text("",size=(2,1))] for i in range(0, len(food))],
                        *[[sg.Text("", font='Ariel 16',size=(2,1)),] for i in range(0, 10 - len(food))]
                    ], title="Food")
                    ],
                [sg.Text("")],
                [sg.Cancel(font="Ariel 20",size=(15,2))],
                [sg.Text("")],
            ]
            while True:
                button, val = rm.Layout(layout).Read()
                if button != sg.WIN_CLOSED and button !="Cancel" :
                    if(sg.popup_ok_cancel("Are you sure you want to remove this item ! ",keep_on_top=True)=="OK"):
                        sf.rm_items(button)
                        sg.popup_ok("Item Removed ! ", keep_on_top=True)
                else:
                    break
            rm.Close()

        if event == "Add Drink":
            drinks = sg.Window('New Drinks', keep_on_top=True, size=(int(gsys(0) / 2), int(gsys(1) / 2)),
                             element_justification='c')
            layout = [
                [sg.Text("")],
                [sg.Text("New Drink",size=(16,3),font="Ariel 16")],
                [sg.Text("")],
                [sg.Text("Name", size=(10, 2), font="Ariel 16"), sg.InputText("Item Name", font="Ariel 16")],
                [sg.Text("")],
                [sg.Text("Cost", size=(10, 2), font="Ariel 16"), sg.InputText("50", font="Ariel 16")],
                [sg.Text("")],
                [sg.Submit(font="Ariel 20", size=(8, 2)), sg.Cancel(font="Ariel 20", size=(8, 2))]
            ]
            button, val = drinks.Layout(layout).Read()
            if button == "Submit":
                sf.add_items("New drinks", val[0], val[1])
            drinks.Close()

        if  event == "Add Food Item":
            food = sg.Window('New Food Item', keep_on_top=True, size=(int(gsys(0) / 2), int(gsys(1) / 2)), element_justification='c')
            layout=[
                [sg.Text("")],
                [sg.Text("New Food Item",size=(16,3),font="Ariel 16")],
                [sg.Text("")],
                [sg.Text("Name",size=(10,2),font="Ariel 16"),sg.InputText("Item Name",font="Ariel 16")],
                [sg.Text("")],
                [sg.Text("Cost", size=(10, 2), font="Ariel 16"), sg.InputText("00", font="Ariel 16")],
                [sg.Text("")],
                [sg.Submit(font="Ariel 20",size=(8,2)),sg.Cancel(font="Ariel 20",size=(8,2))]
            ]
            button, val = food.Layout(layout).Read()
            if button == "Submit":
                sf.add_items("New Food Item",val[0],val[1])
            food.Close()

        if (event == "Exit" or event == sg.WIN_CLOSED):
            if (sg.popup_ok_cancel("Are you sure you want to exit ? ", keep_on_top=True) == "OK"):
                break

    window.Close()
    qt=True

    sys.exit(1)


def server(c):
    global qt
    while qt==False :

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

recieve()