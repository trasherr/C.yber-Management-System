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
port=8014           # port no of socket

s.settimeout(1)

s.bind((host,port)) # creating socket

s.listen(5)         # listening for connections

#######################################################################

def recieve():
    global c,qt
    th = threading.Thread(target=serverGUI)     # GUI thread
    th.start()                                  # Starting GUI thread
    while True:
        try :
            connection, addr = s.accept()  # Establish connection with client.
            print('Got connection from', addr)
            ad.append(str(addr))           # connection added to address list
            connection.send("Thank you for connecting".encode())
            thread=threading.Thread(target=server,args=(connection,addr,))
            thread.start()
        except socket.timeout:
            if qt==True:
                sys.exit(1)

########################## Server GUI ##################################

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
            [sg.Text("",size=(3,2)),sg.Image(r"listen.gif", size=(1,1), key="-listen-")],
            [sg.Text("", size=(2, 2)), sg.Multiline(key="-con-", size=(30, 29)), sg.Text("", size=(2, 2))],
            [sg.Text("", size=(2, 2))]
        ], title="Connections"
            ),sg.Text("",size=(1,1)),
        sg.Frame(layout=[
            [sg.Text("")],
            [sg.Text("")],
            [sg.Text("",size=(5,2)),sg.Button("Add Food Item",size=(20,2),font="Ariel 16"),sg.Text("",size=(5,2))],
            [sg.Text("")],
            [sg.Text("", size=(5, 2)), sg.Button("Add Drink", size=(20, 2), font="Ariel 16"),
             sg.Text("", size=(5, 2))],
            [sg.Text("")],
            [sg.Text("", size=(5, 2)), sg.Button("Remove Item", size=(20, 2), font="Ariel 16"),
             sg.Text("", size=(5, 2))],
            [sg.Text("")],
            [sg.Text("", size=(5, 2)), sg.Button("Check Feedback", size=(20, 2), font="Ariel 16"),
             sg.Text("", size=(5, 2))],
            [sg.Text("")],
            [sg.Text("",size=(5,2)),sg.Button("Exit",size=(20,2),font="Ariel 16"),sg.Text("",size=(5,2))],
            [sg.Text("")],
            [sg.Text("")],
            [sg.Text("")]
        ], title="Options"
        )]
    ]
    window=sg.Window('Server',layout, size=(gsys(0), gsys(1)),element_justification='c',finalize=True)
    while True:
        ord = sf.s_orders()
        addr=sf.add(ad)
        window["orders"].update(ord)
        window["-con-"].update(addr)
        window.FindElement("-listen-").UpdateAnimation("listen.gif",time_between_frames=80)

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
            button,val = rm.Layout(layout).Read()
            if button != sg.WIN_CLOSED and button !="Cancel" :
                if(sg.popup_ok_cancel("Are you sure you want to remove this item ! ",keep_on_top=True)=="OK"):
                    sf.rm_items(button)
                    sg.popup_ok("Item Removed ! ", keep_on_top=True)

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

        if event =="Check Feedback":
            fed=sf.read_feedback()
            feed=sg.Window("Feedback",size=(int(gsys(0)/2),int(gsys(1)/1.5)), keep_on_top=True,element_justification="c" )
            layout=[
                [sg.Text("")],
                [sg.Text("Feedback",font="Ariel 20")],
                [sg.Text("")],
                [sg.Multiline(f"{fed}",font="Ariel 12",size=(50,20))],
                [sg.Text("")],
                [sg.Button("Back",size=(10,2),font="Ariel 16")]
            ]
            button=feed.Layout(layout).Read()
            feed.Close()

        if (event == "Exit" or event == sg.WIN_CLOSED):
            if (sg.popup_ok_cancel("Are you sure you want to exit ? ", keep_on_top=True) == "OK"):
                break

    window.Close()
    qt=True

####################################################################################

############################## Server Function ##############################################

def server(c,addr):
    global qt
    while qt==False :

        ########################### Menu ##############################

        menu=c.recv(32).decode()

        ###################### Login ########################

        if menu=='Login':

            auth=c.recv(1024).decode()

            authenticate=sf.authenticate(auth)

            c.send(str(authenticate).encode())
            if(authenticate!="Incorrect Username or Password"):
                while True:
                    log_choice=c.recv(128).decode()

                    if (log_choice == 'Order'):
                        drinks, d_cost, food, f_cost = sf.order()

                        time.sleep(0.5)
                        c.send(str(drinks).encode())
                        time.sleep(0.5)

                        c.send(str(food).encode())
                        time.sleep(0.5)

                        c.send(str(d_cost).encode())
                        time.sleep(0.5)

                        c.send(str(f_cost).encode())
                        time.sleep(0.5)

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

                            if(check=="Incorrect Username or Password"):
                                c.send("False".encode())
                                continue

                            else:
                                c.send("True".encode())
                                new_pass = str(c.recv(1024).decode())
                                sf.chng_pass(new_pass, curr_pass)
                                break
                        continue

                    elif (log_choice == 'Feedback'):
                        feed=str(c.recv(4096).decode())
                        if (feed!='return code 913372'):
                            sf.feedback(feed)
                        continue

                    elif (log_choice == 'Logout' or log_choice==sg.WIN_CLOSED):
                        out=bool(c.recv(128).decode())

                        if out == True:
                            break
                        else:
                            continue
                    break
        ######################################################

        ###################### Create account ########################

        elif menu=='Create Account':
            while True:
                usr=c.recv(32).decode()
                if usr!="cancel code 913372":
                    check=sf.check(usr)
                    c.send(str(check).encode())
                    if check=="true":

                        crd=c.recv(1024).decode()

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
            if (ext=='Cancel'):
                break
            else:
                ad.remove(str(addr))

        ######################## Menu end #############################
        cont=bool(c.recv(8).decode())

        if cont==True:
            continue
        if cont==False:
            c.close() # Close connection
            sys.exit        

#########################################################################

recieve()