# server functions
import datetime as dt

drinks=['Coffee','Masala Tea','Green Tea','Coca Cola','Pepsi','Sprite']
d_cost=['50','20','40','50','50','50']
food=['Momos','Spring Roll','Burger','Soup']
f_cost=['30','30','35','25']

def order():
    return drinks,d_cost,food,f_cost

def ordering(cus_dets,ordered):
    ordered=eval(ordered)
    orders=cus_dets+f"\n{dt.datetime.now().strftime(' %H:%M:%S / %Y-%m-%d ')}"
    total=0

    for i in range (0,len(ordered)):
        for k in range (0,len(drinks)):
            if (ordered[i]==drinks[k]):
                orders=orders+f"\n{drinks[k]} {d_cost[k]} "
                total=total+int(d_cost[i])

        for k in range(0, len(food)):
            if (ordered[i]==food[k]):
                orders=orders+f"\n{food[k]} {f_cost[k]}"
                total = total + int(d_cost[k])

    orders = orders + f"\nTotal :: {total}"
    with open("orders.dat","a+") as file:
        file.seek(0)
        file.write("\n\n")
        file.write(orders)

def authenticate(auth):

    # Spliting data into lines
    auth=str(auth)
    with open("usr.dat", "r") as file:
        data = file.readlines()
        for line in data:
            det=str(line)
            print (det)

            # checking data in each line

            for i in range (0,len(auth)):
                if det[i]==auth[i]:
                    match=True

                else :
                    match=False
                    break

            if match==True :
                return str(det)

        if match==False:
            return "Incorrect Username or Password"

def check(usr):
    with open("usr.dat", "r") as file:
        data = file.readlines()
        for line in data:
            det = str(line)
            print(det)

            # checking data in each line

            for i in range(0, len(usr)):
                if det[i] == usr[i]:
                    match = True

                else:
                    match = False
                    break

            if match == True and det[len(usr)]==':':
                return 'false'

        if match == False:
            return "true"


def new_acc(crd):
    with open("usr.dat","a+") as file:
        file.seek(0)
        file.write("\n")
        file.write(crd)
        return "True"

def edit(edit_det):

    auth=us_pass(edit_det)
    current_det=authenticate(auth)

    fin = open("usr.dat", "rt")
    data = fin.read()
    data = data.replace(str(current_det), str(edit_det+'\n'))
    fin.close()
    fin = open("usr.dat", "wt")
    fin.write(data) # overrite the input file with the resulting data
    fin.close()


def us_pass(edit_det):
    temp=edit_det
    for j in range (0,2):
        for i in range(0,len(temp)):
            if (temp[i]+temp[i+1]=='::'):
                temp=temp[i+2:]
                break
            else :
                if (j == 0):
                    uname=temp[0:i+1]
                elif(j == 1):
                    passwd = temp[0:i + 1]

    return (uname+'::'+passwd+'::')

def chng_pass(new_pass,curr_pass):
    fin = open("usr.dat", "rt")
    data = fin.read()
    data = data.replace(str(curr_pass), str(new_pass))
    fin.close()
    fin = open("usr.dat", "wt")
    fin.write(data)  # overrite the input file with the resulting data
    fin.close()

def feedback(feed):
    with open("feedback.dat","a+") as file:
        file.seek(0)
        file.write("\n")
        file.write(feed)

def order_history(cus_dets):
    flag=False
    his=''
    with open("orders.dat", "r") as file:
        data = file.readlines()
        for line in data:
            det=str(line)
            print (det)

            if cus_dets in det:
                flag = True
            if 'Total' in det:
                flag = False

            if ( flag == True and cus_dets not in det):
                if("Name ::" not in det):
                    his=his+f'\n{det}'
    if his=='':
        return "No Orders"
    else:
        return his