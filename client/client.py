#client
import socket
import client_func as cf
import PySimpleGUI as sg
import time

###################################theme browser################################
theme='DarkBlack'
sg.theme(theme)
layout = [[sg.Text('Theme Browser')],
          [sg.Text('Click a Theme color to see demo window')],
          [sg.Listbox(values=sg.theme_list(), size=(20, 12), key='-LIST-', enable_events=True)],
          [sg.Button('OK')]
          ]

window = sg.Window('Theme Browser', layout)

while True:  # Event Loop
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'OK'):
        break
    sg.theme(values['-LIST-'][0])
    theme=values['-LIST-'][0]
    cf.set_theme(theme)
    sg.popup('This is {}'.format(values['-LIST-'][0]),keep_on_top=True)

window.close()
################################################################################################

################################################################################

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    # Creating socket object
host = "127.0.0.1" # localhost
port = 8080        # Reserved port

#################################################################################

###################### Connection ###################################

s.connect((host, port))
r = s.recv(1024).decode()
print(r)

##################################################################


while True :
    cont=bool(True)
    log_crd=''
    ###################### Menu begin ########################

    menu=cf.menu()

    s.send(str(menu).encode("utf-8"))

    ###################### login ########################

    if menu=='Login':

        credentials=cf.login()

        print(credentials)
        time.sleep(0.2)
        s.send(str(credentials).encode())

        dets=str(s.recv(1024).decode())
        print(dets)
        if dets=="Incorrect Username or Password" :
            sg.change_look_and_feel(theme)
            sg.popup('Wrong Username or Password !',keep_on_top=True)

            cont=True

        else :

            log_crd=dets
            print(dets)

            while True :

                log_choice = cf.loggedin(log_crd)
                print(log_choice)
                s.send(str(log_choice).encode())

                if(log_choice=='Order'):


                    while True:
                        sg.one_line_progress_meter('Loading ...', 100, 1000, 'key', 'loading...')
                        drinks=s.recv(1024).decode()
                        sg.one_line_progress_meter('Loading ...', 200, 1000, 'key', 'loading...')
                        print('drinks',drinks)
                        sg.one_line_progress_meter('Loading ...', 250, 1000, 'key', 'loading...')

                        food=s.recv(1024).decode()
                        sg.one_line_progress_meter('Loading ...', 400, 1000, 'key', 'loading...')
                        print('food',food)
                        sg.one_line_progress_meter('Loading ...', 500, 1000, 'key', 'loading...')

                        d_cost = s.recv(1024).decode()
                        sg.one_line_progress_meter('Loading ...', 650, 1000, 'key', 'loading...')
                        print( 'd_cost',d_cost)
                        sg.one_line_progress_meter('Loading ...', 800, 1000, 'key', 'loading...')

                        f_cost = s.recv(1024).decode()
                        sg.one_line_progress_meter('Loading ...', 900, 1000, 'key', 'loading...')
                        print('f_cost',f_cost)
                        sg.one_line_progress_meter('Loading ...', 1000, 1000, 'key', 'loading...')
                        break
                    window.Close()

                    cus_dets,ordered = cf.order(drinks,d_cost,food,f_cost)
                    s.send(cus_dets.encode())
                    time.sleep(0.2)
                    s.send(str(ordered).encode())
                    continue

                elif (log_choice == 'Order History'):
                    cus_dets=cf.order_history("flag")
                    s.send(str(cus_dets).encode())
                    history=s.recv(2048).decode()
                    cf.order_history(history)
                    continue

                elif (log_choice=='View Details'):
                    s.send(str(credentials).encode())
                    log_crd=s.recv(1024).decode()
                    cf.view(log_crd)
                    continue

                elif (log_choice=='Edit Details'):
                    edit_det=cf.edit()
                    s.send(str(edit_det).encode())
                    log_crd = edit_det
                    continue

                elif (log_choice == 'Change Password'):

                        while True:
                            curr_passwd=cf.curr_passwd()
                            if curr_passwd=='error code 913372':
                                s.send(curr_passwd.encode())
                                break
                            print(curr_passwd)
                            s.send(curr_passwd.encode())
                            passwd_match=(s.recv(16).decode())
                            print(passwd_match)
                            if(passwd_match=='True'):
                                new_pass=cf.chng_passwd(log_crd)
                                log_crd=cf.log_crd()
                                credentials=new_pass
                                s.send(new_pass.encode())
                                sg.popup("Password Changed !",keep_on_top=True)
                            else:
                                sg.popup("Wrong Password !", keep_on_top=True)
                                continue

                            break

                elif (log_choice == 'Feedback'):
                    feed=cf.feedback()
                    print("Feed = ",feed)
                    s.send(str(feed).encode())
                    if (feed!='' or feed!=' '):
                        sg.popup("Feedback sent !\nThank you for your thoughts.",keep_on_top=True)
                    continue

                elif (log_choice=='Loggout' or log_choice==sg.WIN_CLOSED):

                    ext = cf.loggout()
                    s.send(str(ext).encode())

                    if (ext == True):
                        break
                    else:
                        continue

    #########################################################

    ###################### Create account ########################

    elif menu=='Create Account':

        while True:
            usr=cf.usercheck()
            print(usr)
            s.send(str(usr).encode())
            if usr!="cancel code 913372":
                check=s.recv(8).decode()
                if check == "true" :
                    details=cf.create_acc(usr)
                    s.send(str(details).encode())
                    time.sleep(0.1)
                    if (details != "return code 913372"):
                        new_acc=bool(False)
                        new_acc=bool(s.recv(1024).decode)
                        if (new_acc==True):
                            sg.popup_ok("Account Successfully created !",keep_on_top=True)
                            break

                        else :
                            sg.popup_ok("Some error occured !",keep_on_top=True)
                            break

                else :
                    sg.popup_ok("Username already taken !\nTry a different one",keep_on_top=True)
            else :
                break

    ####################################################

    ###################### Exit ########################
    elif menu=='Exit' or menu==sg.WIN_CLOSED:
        ext=cf.exiting()
        print ("ext=",ext)
        if (ext=='Cancel'):
            s.send(str(ext).encode())
            cont=True
        elif (ext == 'Yes' ):
            print("Exiting the program ! ")
            s.send(str(ext).encode())
            cont = False


    else :
        print("     Wrong Input ! ")
        cont=True
    ####################################################

    ######################## Menu end #############################

    if cont==False:
        print("false")
        s.send("False".encode())
        break

    else:
        print("send = ")
        s.send("True".encode())
        print(True)
        continue

s.close()