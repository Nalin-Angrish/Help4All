# This file will contain all the methods to interact with the local database

import os                       # Import all dependencies

def getOrderCount():                                # count the number of orders done till now and add 1 to get the current order number
    return str(len(os.listdir("./database/orders")) + 1)


def addOrder(name, phone, address, item, notes):           # Add order in the orders list
    count = getOrderCount()
    with open("database/orders/"+count+".txt", 'a+') as order:
        order.write(name)
        order.write("\n"+phone)
        order.write("\n"+address)
        order.write("\n"+item)
        order.write("\n"+notes)
    return count

def getOrder(number):                               # Get 'Order' object for the given order number
    return Order(str(number))

def approveOrder(number):                           # To add the approved tag to an order
    with open('database/orders/'+str(number)+'.txt', 'r+') as order:
        if("*Approved*" not in order.read()):
            order.write("\n*Approved*")



class Order(object):            # A class that can be used by our main python file for easily getting details of any order
    def __init__(self, name):
        self.data = open("database/orders/"+name+".txt", 'r').read().splitlines()

    def getName(self):                  # To get Name 
        return self.data[0]
    
    def getPhone(self):                 # To get Phone Number
        return self.data[1]

    def getAddress(self):               # To get Address
        return self.data[2]

    def getItem(self):                  # To get donated item / sent information
        return self.data[3]

    def getNotes(self):              # To get notes
        try:
            return "\n".join(self.data[4:]).replace("*Approved*", "")
        except:
            return "\n".join(self.data[4:])

    def isApproved(self):               # To check if the order is approved or not
        return ("*Approved*" in self.data)  # data should contain *Approved* if it is approved





def addNGO(name, email, phone):                 # To add an NGO's credentials in the given state
    with open("database/ngos/"+name+".txt", 'w+') as myFile:
        myFile.write(str("{},{},{}".format(name, email, phone)))

def getNGOs(): 
    final = []                                            
    for file in os.listdir("database/ngos"):                                          # This function will return a list of tuples,                                                                 
        print(file)
        with open("database/ngos/"+file, "r") as myFile:    # where each tuple would contain the name and email of one NGO and 
            final.append(tuple(myFile.read().split(",")))  # multiple tuples will hence contain for multiple NGOs 
        
    return final