# client functions
import msvcrt
import PySimpleGUI as sg
from win32api import GetSystemMetrics

th=''
def set_theme(theme):
    global th
    th = theme

print("Width =", GetSystemMetrics(0))
print("Height =", GetSystemMetrics(1))


class crdent():
    uname=''
    fname=''
    lname=''
    email=''
    phone=''
    passwd=''

order=[]

def menu():
    sg.change_look_and_feel(th)
    menu = sg.Window('Main Menu', keep_on_top=True, size=(GetSystemMetrics(0),GetSystemMetrics(1)), element_justification='c') # begin with a blank form

    layout = [
        [sg.Text("\n"*int(GetSystemMetrics(1)/100))],
        [sg.Button('Login',size=(32,3), font="Ariel 32", button_color=('white','lime'))],
        [sg.Text('')],
        [sg.Button('Create Account',size=(32,3), font="Ariel 32",button_color=('white','blue'))],
        [sg.Text('')],
        [sg.Button('Exit', size=(32,3), font="Ariel 32",button_color=('white','red'))]
        ]
    button ,values  = menu.Layout(layout).Read()
    b1=button
    print (b1)
    menu.Close()
    return b1

def login():
    sg.change_look_and_feel(th)
    form = sg.Window('Main Menu', keep_on_top=True, size=(GetSystemMetrics(0),GetSystemMetrics(1)), element_justification='c')  # begin with a blank form

    layout = [
        [sg.Text("\n" * int(GetSystemMetrics(1) / 100))],
        [sg.Text('Login \n',font="Ariel 32")],
        [sg.Text("")],
        [sg.Text('Name',font="Ariel 20", size=(10, 1)), sg.InputText('Username',font="Ariel 20")],
        [sg.Text("")],
        [sg.Text('Password',font="Ariel 20", size=(10, 1)), sg.InputText('Password', password_char='*',font="Ariel 20")],
        [sg.Text('\n')],
        [sg.Submit(size=(20,2), font="Ariel 20")]
    ]

    button, values = form.Layout(layout).Read()

    us=values[0]
    pas=values[1]
    form.Close()

    comstr = us+'::'+pas+'::'
    print(comstr)
    return comstr

def create_acc():
    wrong_text=''
    sg.change_look_and_feel(th)

    layout = [
        [sg.Text("")],
        [sg.Text('Create Account \n',font='Ariel 32')],
        [sg.Text("")],
        [sg.Text('Username',font="Ariel 20", size=(10, 1)), sg.InputText('Username',font="Ariel 20")],
        [sg.Text("")],
        [sg.Text('First name',font="Ariel 20", size=(10, 1)), sg.InputText('First name',font="Ariel 20")],
        [sg.Text("")],
        [sg.Text('Last name', font="Ariel 20", size=(10, 1)), sg.InputText('Last name',font="Ariel 20")],
        [sg.Text("")],
        [sg.Text('Email', font="Ariel 20", size=(10, 1)), sg.InputText('Email',font="Ariel 20")],
        [sg.Text("")],
        [sg.Text('Phone no.', font="Ariel 20", size=(10, 1)), sg.InputText('Phone no.',font="Ariel 20")],
        [sg.Text("")],
        [sg.Text('Password', font="Ariel 20", size=(10, 1)), sg.InputText('Password', password_char='*',font="Ariel 20")],
        [sg.Text("")],
        [sg.Text('Confirm Password',font="Ariel 20", size=(10, 1)), sg.InputText('Password', password_char='*',font="Ariel 20")],
        [sg.Text("\n")],
        [sg.Submit(size=(20,2),font="Ariel 20"),sg.Cancel(size=(20,2),font="Ariel 20")]
    ]
    form = sg.Window('Create Account',layout, keep_on_top=True, size=(GetSystemMetrics(0), GetSystemMetrics(1)),element_justification='c')  # begin with a blank form
    while True :
        button, values = form.read()

        if (button == "Cancel" or button == sg.WIN_CLOSED):
            form.Close()
            return "return code 913372"

        if len(values[0]) >= 4 and len(values[1]) >= 3 and len(values[2]) >= 3 and len(values[5]) >= 8 and len(values[3]) < 50 and len(values[4]) == 10 :

            if values[5] == values[6]:
                details = values[0] + '::' + values[5] + '::' + values[1] + '::' + values[2] + '::' + values[3] + '::' + values[4]
                form.Close()
                sg.popup_ok(f"Creating Account with username {values[0]}",keep_on_top=True)
                return details

            else:
                sg.popup_ok("Password didn't match !",keep_on_top=True)

        else :
            sg.popup_ok("Username should have atleast 4 characters !\nFirst name should have atleast 3 characters !\nLast name should have atleast 3 characters !\nPhone number must be of 10 digits !\nEmail should not have more than 50 characters !\nPassword should have atleast 8 characters !",keep_on_top=True)

def exiting():
    sg.change_look_and_feel(th)
    exit_f = sg.FlexForm('Exit!')  # begin with a blank form

    layout = [
        [sg.Text('Are you sure you want to exit ? \n')],
        [sg.Button("Yes"),sg.Button("Cancel")]
    ]
    button, values = exit_f.Layout(layout).Read()
    ans=button
    exit_f.Close()
    return ans


def crdfinder(log_crd):
    temp=log_crd
    print(log_crd)

    for j in range (0,5):
        for i in range(0,len(temp)):
            if (temp[i]+temp[i+1]=='::'):
                temp=temp[i+2:]
                break
            else :
                if (j == 0):
                    crdent.uname=temp[0:i+1]
                elif(j == 1):
                    crdent.passwd = temp[0:i + 1]
                elif (j == 2):
                    crdent.fname = temp[0:i + 1]
                elif (j == 3):
                    crdent.lname = temp[0:i + 1]
                elif (j == 4):
                    crdent.email = temp[0:i + 1]


    for i in range(0, len(temp)):
        if (temp[i] == ':'):
            break
        else:
            crdent.phone = temp[0:i + 1]

#def order():


def edit():
    sg.change_look_and_feel(th)
    form = sg.Window('Edit Details', keep_on_top=True, size=(GetSystemMetrics(0),GetSystemMetrics(1)), element_justification='c')  # begin with a blank form

    layout = [
        [sg.Text("")],
        [sg.Text('Edit Details \n',font="Ariel 32")],
        [sg.Text(f'Username {crdent.uname}\n',font="Ariel 26")],
        [sg.Text("")],
        [sg.Text('First name',font="Ariel 20", size=(10, 1)), sg.InputText(f'{crdent.fname}',font="Ariel 20")],
        [sg.Text("")],
        [sg.Text('Last name',font="Ariel 20", size=(10, 1)), sg.InputText(f'{crdent.lname}',font="Ariel 20")],
        [sg.Text("")],
        [sg.Text('Email',font="Ariel 20", size=(10, 1)), sg.InputText(f'{crdent.email}',font="Ariel 20")],
        [sg.Text("")],
        [sg.Text('Phone no.',font="Ariel 20", size=(10, 1)), sg.InputText(f'{crdent.phone[:10]}',font="Ariel 20")],
        [sg.Text("\n")],
        [sg.Submit(size=(20,2),font="Ariel 20")]
    ]
    while True:
        button, values = form.Layout(layout).Read()

        fname = values[0]
        lname = values[1]
        email = values[2]
        phone_no=values[3]
        print(fname,lname,email,phone_no)


        if len(fname)>=3 and len(lname)>=3  and len(phone_no)==10 and len(email)<50:

            details = crdent.uname + '::' + crdent.passwd + '::' + fname + '::' + lname + '::' + email + '::' + phone_no
            print(f" {crdent.fname} || {crdent.lname} || {crdent.email} || {crdent.phone} ")
            sg.popup_ok("Details Changed !",keep_on_top=True)
            form.Close()
            return details
        else:
            sg.change_look_and_feel(th)
            wrong_a = sg.FlexForm('Error !')  # begin with a blank form

            layout = [
                [sg.Text("First name should have atleast 3 characters !\nLast name should have atleast 3 characters !\nPhone number must be of 10 digits !\nEmail should not have more than 50 characters !\n")],
                [sg.Button('OK')]
            ]
            button,values= wrong_a.Layout(layout).Read()
            wrong_a.Close()



def view(log_crd):
    crdfinder(log_crd)

    sg.change_look_and_feel(th)
    pdet = sg.Window('View Details', keep_on_top=True, size=(GetSystemMetrics(0),GetSystemMetrics(1)), element_justification='c')  # begin with a blank form

    layout = [
        [sg.Text("")],
        [sg.Text("")],
        [sg.Text('User Details \n', font="Ariel 32", size=(50, 2),justification="c")],
        [sg.Frame(layout=[
            [sg.Text("")],
            [sg.Text(f'   Username    :: {crdent.uname}\n\n   First Name   :: {crdent.fname}\n\n   Last Name    :: {crdent.lname}\n\n   Email            :: {crdent.email}\n\n   Contact no.   :: {crdent.phone}',font="Ariel 22",size=(35,10))],
            [sg.Text("")]
                ]
            ,title='Details')],
        [sg.Text("")],
        [sg.Button(" < Back", font="Ariel 20", size=(10, 1))]
    ]
    button,values = pdet.Layout(layout).Read()
    pdet.Close()

def curr_passwd():
    sg.change_look_and_feel(th)
    passwd = sg.Window('Change Password', keep_on_top=True, size=(GetSystemMetrics(0),GetSystemMetrics(1)), element_justification='c')  # begin with a blank form

    layout = [

        [sg.Text('\nChange Password !\n\n',font="Ariel 32")],
        [sg.Text("Current Password", font="Ariel 20", size=(20, 1)), sg.InputText( password_char='*',font="Ariel 20")],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Submit(font="Ariel 20", size=(20, 1)),sg.Cancel(font="Ariel 20", size=(20, 1))]
    ]
    button, values = passwd.Layout(layout).Read()

    if button == 'Cancel' or button==sg.WIN_CLOSED:
        passwd.Close()
        return "error code 913372"

    current_passwd = values[0]
    passwd.Close()
    return crdent.uname+"::"+current_passwd+"::"

def chng_passwd(log_crd):
    sg.change_look_and_feel(th)
    passwd = sg.Window('Change Password', keep_on_top=True, size=(GetSystemMetrics(0),GetSystemMetrics(1)), element_justification='c')  # begin with a blank form

    layout = [
        [sg.Text('')],
        [sg.Text('')],
        [sg.Text('Change Password !\n\n',font='Ariel 32')],
        [sg.Text("New Password", font="Ariel 20", size=(20, 1)), sg.InputText(password_char='*',font="Ariel 20")],
        [sg.Text('')],
        [sg.Text("Confirm Password",  font="Ariel 20", size=(20, 1)), sg.InputText(password_char='*',font="Ariel 20")],
        [sg.Text('')],
        [sg.Submit(font="Ariel 20", size=(20, 1))]
    ]

    button, values = passwd.Layout(layout).Read()
    new_passwd = values[0]
    confirm_passwd = values[1]
    passwd.Close()



    if (new_passwd==confirm_passwd) :
        crdent.passwd = new_passwd
        print(new_passwd)
        print(crdent.passwd)
        print(crdent.uname + '::' + new_passwd + '::')
        return crdent.uname + '::' + new_passwd + '::'


    else:
        print("         Passwords didn't match !\n")
        print("\n         Press any key to continue !")
        msvcrt.getch()
        return chng_passwd(log_crd)

def feedback():
    fed_bck=' '
    sg.change_look_and_feel(th)
    feed = sg.Window('Feedback', keep_on_top=True, size=(GetSystemMetrics(0),GetSystemMetrics(1)), element_justification='c')  # begin with a blank form

    layout = [
        [sg.Text('')],
        [sg.Text('Feedback',font='Ariel 32')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Multiline(size=(60, 10),font='Ariel 20')],
        [sg.Button('Send',size=(20,2),font='Ariel 26'),sg.Button("Exit",size=(20,2),font='Ariel 26')]
              ]
    Button, values = feed.Layout(layout).Read()

    if (Button=='Send'):
        fed_bck=crdent.uname+'::\n'+values[0]+'\n'

    feed.Close()
    print(fed_bck)
    return fed_bck


def loggout():
    sg.change_look_and_feel(th)
    exit_f = sg.FlexForm('logout !')  # begin with a blank form

    layout = [
        [sg.Text('Are you sure you want to Logout ? \n')],
        [sg.Button("Yes"), sg.Button("Cancel")]
    ]
    button, values = exit_f.Layout(layout).Read()
    ans = button
    exit_f.Close()
    if (ans == 'Yes'):
        return True
    else:
        return False


def loggedin(log_crd):
    crdfinder(log_crd)

    sg.change_look_and_feel(th)
    options = sg.Window('View Details', keep_on_top=True, size=(GetSystemMetrics(0),GetSystemMetrics(1)), element_justification='c')  # begin with a blank form

    layout = [
        [sg.Text('')],
        [sg.Text(f'Welcome {crdent.fname} {crdent.lname} ',size=(40,2), font="Ariel 32")],
        [sg.Text('')],
        [sg.Button("Order",size=(20,3), font="Ariel 32"),sg.Button("Order History",size=(20,3), font="Ariel 32")],
        #[sg.Text('')],
        [sg.Button("View Details",size=(20,3), font="Ariel 32"),sg.Button("Edit Details",size=(20,3), font="Ariel 32")],
        #[sg.Text('')],
        [sg.Button("Change Password",size=(20,3), font="Ariel 32"),sg.Button("Feedback",size=(20,3), font="Ariel 32")],
        #[sg.Text('')],
        [sg.Button("Loggout", font="Ariel 32")]
    ]
    button,values = options.Layout(layout).Read()

    l_choice = button
    options.Close()
    return l_choice

def order(drinks,d_cost,food,f_cost):

    drinks=eval(drinks)
    food=eval(food)
    d_cost=eval(d_cost)
    f_cost=eval(f_cost)
    print(food)


    sg.change_look_and_feel(th)
    layout = [
            [sg.Text("")],
            [sg.Text("")],

            [sg.Frame(layout=[

                    *[[sg.Checkbox(f'{drinks[i]}',font='Ariel 16',size=(15,2)),sg.Text(f'{d_cost[i]}',font='Ariel 16',size=(5,2))] for i in range (0,len(drinks))],
                    * [[sg.Text("",font='Ariel 16',size=(15,2)),] for i in range(0, 10 - len(drinks))]
                       ]
                ,title='Drinks'),
            sg.Frame(layout=[
                    *[[sg.Checkbox(f'{food[i]}',font='Ariel 16',size=(15,2)),sg.Text(f'{d_cost[i]}',font='Ariel 16',size=(5,2))] for i in range (0,len(food))],
                    * [[sg.Text("",font='Ariel 16',size=(15,2)), ] for i in range(0, 10 - len(food))]
                     ]
                ,title='Food'),
                sg.Frame(layout=[
                    [sg.Text(size=(1, 1), font=('Helvetica', 12)),sg.Text(size=(15, 30), font=('Helvetica', 12), justification='left', key='-items-'),
                     sg.Text(size=(5, 30), font=('Helvetica', 12), justification='right', key='-costs-'),sg.Text(size=(1, 1), font=('Helvetica', 12))],
                    [sg.Text(size=(1, 1), font=('Helvetica', 12)),sg.Text("Total",size=(15,1), font=('Helvetica', 12), justification='left'),
                     sg.Text(size=(5, 1), font=('Helvetica', 12), justification='right', key='-OUTPUT-')]
                ]
                    , title='Order')
            ],
            [sg.Text("")],
            [sg.Button("Show Total",font='Ariel 20',size=(10,2)),sg.Button("Order",font='Ariel 20',size=(10,2)),sg.Button("Cancel",font='Ariel 20',size=(10,2))]
        ]
    order = sg.Window('Order',layout, keep_on_top=True, size=(GetSystemMetrics(0), GetSystemMetrics(1)),element_justification='c')  # begin with a blank form
    while True:
        event, values = order.Read()
        print(event, values)
        total = 0
        ordered=[]
        o_cost=[]
        items=''
        costs=''
        if event in (sg.WIN_CLOSED, 'Cancel'):
            if sg.popup_ok_cancel("Press 'OK' to go back !", keep_on_top=True) == 'OK':
                order.Close()
                return "No","Orders"

        for i in range (0,len(drinks)):
            if(values[i]==True  ):
                total=total+int(d_cost[i])
                ordered.append(drinks[i])
                o_cost.append(d_cost[i])
                print(d_cost[i])

        for j in range (0,len(food)):
            if(values[i+j+1] == True):
                ordered.append(food[j])
                o_cost.append(d_cost[j])
                total = total + int(d_cost[j])
        if event=='Order':
            if len(ordered)==0:
                sg.popup("Nothing is selected !",keep_on_top=True)
            else :
                if sg.popup_ok_cancel("Press 'OK' to confirm order !",keep_on_top=True) == 'OK':
                    order.Close()
                    cus_dets = "Username :: " + crdent.uname +"\nName :: "+crdent.fname+" " +crdent.lname
                    order.Close()
                    return cus_dets,ordered

        print('total',total)
        print('ordered',ordered)
        for i in range (0,len(ordered)):
            items=items+f"{ordered[i]}\n"
            costs=costs+f"{o_cost[i]}\n"
        order['-OUTPUT-'].update(total)
        order['-items-'].update(items)
        order['-costs-'].update(costs)
        print('items', items)
        print('costs', costs)
    order.Close()

def order_history(history):

    if (history=='flag'):
        cus_dets = "Username :: " + crdent.uname #+ "\nName ::" + crdent.fname + ' ' + crdent.lname
        return cus_dets
    else :
        sg.change_look_and_feel(th)
        his=sg.Window('Order History', keep_on_top=True, size=(GetSystemMetrics(0), GetSystemMetrics(1)),element_justification='c')
        layout=[
            [sg.Frame(layout=[
                [sg.Button("< Back",size=(10,2),font="Ariel 12")],
                [sg.Text(f"{history}",font='Ariel 12',size=(60,30))]
                ],title='Order History')
            ]
        ]
        event = his.Layout(layout).Read()
        his.Close()

def log_crd():
    return crdent.uname + '::' + crdent.passwd + '::' + crdent.fname + '::' + crdent.lname + '::' + crdent.email + '::' + crdent.phone