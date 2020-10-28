# server functions
import datetime as dt

drinks=[]
d_cost=[]
food=[]
f_cost=[]

def order_menu():
    global drinks,food,d_cost,f_cost
    with open ("menu.dat","r") as file:
        data=file.readlines()
        drinks = eval(data[0])
        d_cost = eval(data[1])
        food = eval(data[2])
        f_cost = eval(data[3])

def order():
    return drinks,d_cost,food,f_cost

def ordering(cus_dets,ordered):
    ordered=eval(ordered)
    orders=cus_dets+f"\n{dt.datetime.now().strftime('%H:%M:%S / %Y-%m-%d')}"
    total=0

    for i in range (0,len(ordered)):
        for k in range (0,len(drinks)):
            if (ordered[i]==drinks[k]):
                orders=orders+f"\n{drinks[k]} {d_cost[k]} "
                total=total+int(d_cost[k])

        for k in range(0, len(food)):
            if (ordered[i]==food[k]):
                orders=orders+f"\n{food[k]} {f_cost[k]}"
                total = total + int(f_cost[k])

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
    print(crd)
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

def s_orders():
    his=""
    temp=""
    flag=2
    with open ("orders.dat","r") as file:
        data=file.readlines()
        for line_read in data:

            if "Username" in line_read:
                flag=1

            elif "Total" in line_read :
                flag=0

            if len(line_read)!=0:
                temp = f"{temp}  {line_read}"

            if flag == 0 :
                his=f"{temp}\n{his}"
                flag=2
                temp=""

    return his

def order_history(cus_dets):
    flag=False
    his=''
    with open("orders.dat", "r") as file:
        data = file.readlines()
        for line in data:
            det=str(line)
            print (det)

            if cus_dets in det :
                flag = True
                his = '\n=================' + his

            elif 'Total' in det:
                his =  f'\n{det}\n----------------'+his
                his = '\n\n=================' + his
                flag = False

            elif ( flag == True and cus_dets not in det):
                if("Name ::" not in det):
                    his=f'\n{det}'+his
    if his=='':
        return "No Orders"
    else:
        return his[:2000]

def add(addr):
    add_str=""
    for i in range (0,len(addr)):
        add_str=addr[i]+"\n"+add_str
    return add_str

def add_items(o,n,c):
    global drinks, food, d_cost, f_cost
    if o=="New Food Item" and len(food) < 10:
        food.append(n)
        f_cost.append(c)
        flag=1
    elif o=="New drinks" and len(drinks) < 10:
        drinks.append(n)
        d_cost.append(c)
        flag = 1

    if flag==1:
        temp=str(drinks)+"\n"+str(d_cost)+"\n"+str(food)+"\n"+str(f_cost)
        fout = open("menu.dat","wt")
        fout.write(temp)
        fout.close()

def rm_items(item):

    global drinks,food,d_cost,f_cost
    for i in range (0,len(drinks)):
        if item==drinks[i]:
            drinks.remove(drinks[i])
            d_cost.remove(d_cost[i])

    for i in range (0,len(food)):
        if item==food[i]:
            food.remove(food[i])
            f_cost.remove(f_cost[i])

    temp=str(drinks)+"\n"+str(d_cost)+"\n"+str(food)+"\n"+str(f_cost)
    fout = open("menu.dat","wt")
    fout.write(temp)
    fout.close()