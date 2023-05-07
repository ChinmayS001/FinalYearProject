from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from Block import *
from Blockchain import *
from hashlib import sha256
import os
from tkinter import ttk
import time
import requests
from keras.models import load_model
from Agent import *
import math
import numpy as np
import random
from collections import deque
import sys
import matplotlib.pyplot as plt
from Block import *

main = Tk()
main.title("Effective Management for Blockchain-Based Agri-Food Supply Chains Using Deep Reinforcement Learning")
main.geometry("1300x1200")

global filename
compute_time = []
purchase_arr = []
sold_arr = []
rewards = []
qrewards = []
extension_rewards = []
urlg = "http://localhost:5000/blocks"
urlp = "http://localhost:5000/blockchain"
blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
        
    fileinput.close()
    for i in blockchain.chain:
        print(i.index)


res = requests.get(urlg)
# print(res.headers['content-type'])
# print(res.json())
obj = res.json()
#print(obj)
if obj != []:
    if len(blockchain.chain) == 1:
        print("Less than One")
        rem = obj[1:]
        #print("got",rem)
        for i in range(len(rem)):
            b = Block(rem[i]["index"],[rem[i]["transactions"]],rem[i]["timestamp"],rem[i]["previous_hash"],rem[i]["nonce"])
            blockchain.chain.append(b)
    
        #print(obj," ",blockchain.chain[len(blockchain.chain)-1].index," ",obj[len(obj)-1]['index'])
        print("Initial Load",blockchain)
        blockchain.save_object(blockchain,'blockchain_contract.txt')


    elif obj[len(obj)-1]['index'] != blockchain.chain[len(blockchain.chain)-1].index:
        rem = obj[blockchain.chain[len(blockchain.chain)-1].index+1:]
        print("got",rem)
        for i in range(len(rem)):
            b = Block(rem[i]["index"],[rem[i]["transactions"]],rem[i]["timestamp"],rem[i]["previous_hash"],rem[i]["hash"],rem[i]["nonce"])
            blockchain.chain.append(b)
        
        #print(obj," ",blockchain.chain[len(blockchain.chain)-1].index," ",obj[len(obj)-1]['index'])
        print("Initial Load",blockchain.chain[0])
        blockchain.save_object(blockchain,'blockchain_contract.txt')
        print("Initial Load after save",blockchain.chain[0])


def saveASCDetails():
    global filename
    global compute_time
    
    '''commit2'''
    res = requests.get(urlg)
    # print(res.headers['content-type'])
    # print(res.json())
    print("The Blockchain before save asc details",blockchain)
    obj = res.json()
    #print(obj)
    if obj != []:
        if len(blockchain.chain) == 1:
            print("Less than One")
            rem = obj[1:]
            #print("got",rem)
            for i in range(len(rem)):
                b = Block(rem[i]["index"],[rem[i]["transactions"]],rem[i]["timestamp"],rem[i]["previous_hash"],rem[i]["nonce"])
                blockchain.chain.append(b)
        
            #print("98",obj," ",blockchain.chain[len(blockchain.chain)-1].index," ",obj[len(obj)-1]['index'])
            print("The Blockchain after save asc details",type(blockchain),blockchain)
            blockchain.save_object(blockchain,'blockchain_contract.txt')


        elif obj[len(obj)-1]['index'] != blockchain.chain[len(blockchain.chain)-1].index:
            rem = obj[blockchain.chain[len(blockchain.chain)-1].index+1:]
            #print("remaining Blockchain",rem)
            for i in range(len(rem)):
                b = Block(rem[i]["index"],[rem[i]["transactions"]],rem[i]["timestamp"],rem[i]["previous_hash"],rem[i]["hash"],rem[i]["nonce"])
                blockchain.chain.append(b)
            
            print(obj," ",blockchain.chain[len(blockchain.chain)-1].index," ",obj[len(obj)-1]['index'])
            print("The Blockchain after save asc details",type(blockchain),blockchain)
            blockchain.save_object(blockchain,'blockchain_contract.txt')

        '''commit2'''

    text.delete('1.0', END)
    pid = tf1.get()
    pname = tf2.get()
    desc = tf3.get()
    usertype = userlist.get()
    if len(pid) > 0 and len(pname) > 0 and len(desc) > 0:
        start = time.time()
        data = pid+"#"+pname+"#"+desc+"#"+usertype
        blockchain.add_new_transaction(data)
        hash = blockchain.mine()
        b = blockchain.chain[len(blockchain.chain)-1]
        text.insert(END,"Blockchain Previous Hash : "+str(b.previous_hash)+"\nBlock No : "+str(b.index)+"\nCurrent Hash : "+str(b.hash)+"\n")
        text.insert(END,"Details saved in blockchain\n\n")
        blockchain.save_object(blockchain,'blockchain_contract.txt')
        tf1.delete(0, END)
        tf2.delete(0, END)
        tf3.delete(0, END)
        end = time.time()
        compute_time.append((end - start))
        

        print("original Object",blockchain,"Chain",blockchain.chain[0])
        print()
        ch = blockchain.chain
        q = blockchain.get_dict()
        p = q
        chainD = []
        print("Completely before and after",p)
        for i in p["chain"]:
            chainD.append(i.get_dict())
        p["chain"] = chainD
        
        print("Converted to dictionary",p,"It's Chain",p["chain"][0])
        print()
        print(blockchain,"Chain",blockchain.chain[0])
        print()
        response = requests.post(urlp, json=p)
        blockchain.chain = ch
        #print(response.content)
    else:
        text.insert(END,"Please fill all details")
        

def getProduct():
    text.delete('1.0', END)
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            arr = data.split("#")
            text.insert(END,"Available Product ID : "+arr[0]+"\n")
            text.insert(END,"Product Storage Hash ID : "+str(b.hash)+"\n\n")
    print(blockchain)

def getASCDetails():
    text.delete('1.0', END)
    pid = tf1.get()
    flag = False
    '''commit2'''
    res = requests.get(urlg)
    print("The Blockchain before get asc details",type(blockchain.chain[0]),blockchain)
    # print(res.headers['content-type'])
    # print(res.json())
    obj = res.json()
    #print(obj)
    if obj != []:
        if len(blockchain.chain) == 1:
            print("Less than One")
            rem = obj[1:]
            #print("got",rem)
            for i in range(len(rem)):
                b = Block(rem[i]["index"],[rem[i]["transactions"]],rem[i]["timestamp"],rem[i]["previous_hash"],rem[i]["nonce"])
                blockchain.chain.append(b)
        
            #print(obj," ",blockchain.chain[len(blockchain.chain)-1].index," ",obj[len(obj)-1]['index'])
            print("The Blockchain after get asc details",type(blockchain.chain[0]),blockchain)
            blockchain.save_object(blockchain,'blockchain_contract.txt')


        elif obj[len(obj)-1]['index'] != blockchain.chain[len(blockchain.chain)-1].index:
            rem = obj[blockchain.chain[len(blockchain.chain)-1].index+1:]
            print("got",rem)
            for i in range(len(rem)):
                b = Block(rem[i]["index"],[rem[i]["transactions"]],rem[i]["timestamp"],rem[i]["previous_hash"],rem[i]["hash"],rem[i]["nonce"])
                blockchain.chain.append(b)
            
            print(obj," ",blockchain.chain[len(blockchain.chain)-1].index," ",obj[len(obj)-1]['index'])
            print("The Blockchain after get asc details",type(blockchain.chain[0]),blockchain)
            blockchain.save_object(blockchain,'blockchain_contract.txt')

        '''commit2'''
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            arr = data.split("#")
            if arr[0] == pid:
                text.insert(END,"Product ID    : "+arr[0]+"\n")
                text.insert(END,"Product Name  : "+arr[1]+"\n")
                text.insert(END,"Description   : "+arr[2]+"\n")
                text.insert(END,"User Type     : "+arr[3]+"\n\n")
                flag = True
                
    if flag == False:
        text.insert(END,"No records found for given ID")
    

def formatQuantity(qty):
    return str(qty)

def getStockQuantity():
    vector = []
    index = 0 
    with open('Dataset/agriculture_stock.csv', "r") as fileData:  
        for line in fileData:
            if index > 0:
                line = line.strip('\n')
                line = line.strip()
                arr = line.split(",")
                value = arr[5]
                value = value[1:len(value)-1]
                vector.append(float(value))
            index = 1
    return vector 

def calculateSigmoid(gamma_value):
    if gamma_value < 0:
        return 1 - 1/(1 + math.exp(gamma_value))
    else:
        return 1/(1 + math.exp(-gamma_value))
    

def getAgentState(values, index, total):
    data = index - total + 1
    block = values[data:index + 1] if data >= 0 else -data * [values[0]] + values[0:index + 1]
    result = []
    for i in range(total - 2):
        result.append(calculateSigmoid(block[i + 1] - block[i]))
    return np.array([result])

def DRLSimulation():
    global purchase_arr
    global sold_arr
    global rewards
    global qrewards
    text.delete('1.0', END)
    windowSize = 10
    episodeCount = 1000
    windowSize = int(windowSize)
    episodeCount = int(episodeCount)
    count = 0
    agent = Agent(windowSize)
    quantity = getStockQuantity()
    length = len(quantity) - 1
    batchSize = 32
    modelName = 'models/model_ep500'
    model = load_model(modelName)
    windowSize = model.layers[0].input.shape.as_list()[1]
    state = getAgentState(quantity, 0, windowSize + 1)
    cuttent_Quantity = 0
    agent.inventory = []
    purchase_arr.clear()
    sold_arr.clear()
    rewards.clear()
    qrewards.clear()
    qreward = 0
    for t in range(length):
        action = agent.act(state)
        nextState = getAgentState(quantity, t + 1, windowSize + 1)
        rewardValue = 0
        if action == 1: # buy
            agent.inventory.append(quantity[t])
            text.insert(END,"Start Producing Stock : " + formatQuantity(quantity[t])+"\n")
            purchase_arr.append(quantity[t])
        
        elif action == 2 and len(agent.inventory) > 0:
            old_quantity = agent.inventory.pop(0)
            rewardValue = max(quantity[t] - old_quantity, 0)
            qreward = max(quantity[t] - old_quantity, 0) - 15
            cuttent_Quantity = old_quantity - quantity[t] 
            if  old_quantity > quantity[t]:
                text.insert(END,"You can Sale sufficient stock available : " + formatQuantity(quantity[t]) + "| Current Available : " + formatQuantity(old_quantity)+" | After Sale Available : " + formatQuantity(old_quantity - quantity[t])+"\n")
                sold_arr.append(old_quantity - quantity[t])
            else:
                text.insert(END,"You can Sale sufficient stock available : " + formatQuantity(quantity[t]) + "| Current Available : " + formatQuantity(old_quantity)+" | After Sale Available : " + formatQuantity(quantity[t] - old_quantity)+"\n")
                sold_arr.append(quantity[t] - old_quantity)
        done = True if t == length - 1 else False
        if rewardValue != 0:
            rewards.append(rewardValue)
            qrewards.append(qreward)
        agent.memory.append((state, action, rewardValue, nextState, done))
        state = nextState
        if done:
            text.insert(END,"\n--------------------------------\n")
            text.insert(END,"Current Available Quantity : " + formatQuantity(cuttent_Quantity)+"\n")
            print("--------------------------------")
    purchase_arr = np.asarray(purchase_arr)       
    sold_arr = np.asarray(sold_arr)         
    plt.figure(figsize=(10,6))
    plt.grid(True)
    plt.xlabel('Days')
    plt.ylabel('Purchase/Sales Count')
    plt.plot(purchase_arr, 'ro-', color = 'green')
    plt.plot(sold_arr, 'ro-', color = 'blue')
    plt.legend(['Available Stock', 'Sold Stock'], loc='upper left')
    #plt.xticks(wordloss.index)
    plt.title('Stock of Factory & Retailers by using DR-SCM')
    plt.show()    

def rewardGraph():
    plt.figure(figsize=(10,6))
    plt.grid(True)
    plt.xlabel('Episodes')
    plt.ylabel('Reward Values')
    plt.plot(rewards, 'ro-', color = 'green')
    plt.plot(qrewards, 'ro-', color = 'blue')
    plt.plot(extension_rewards, 'ro-', color = 'yellow')
    plt.legend(['DR-SCM Rewards', 'QLearning Rewards','Extension MultiAgent Rewards'], loc='upper left')
    #plt.xticks(wordloss.index)
    plt.title('Stock of Factory & Retailers by using DR-SCM')
    plt.show()        

def graph():
    X = []
    for i in range(len(compute_time)):
        X.append("Block "+str((i+1)))
    height = compute_time
    bars = X
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.title("Blockchain Hashes Computation Graph")
    plt.show()

def runMultiAgent(current_reward):
    global extension_rewards
    windowSize = 10
    episodeCount = 1000
    windowSize = int(windowSize)
    episodeCount = int(episodeCount)
    count = 0
    agent = Agent(windowSize)
    quantity = getStockQuantity()
    length = len(quantity) - 1
    batchSize = 32
    modelName = 'models/model_ep500'
    model = load_model(modelName)
    windowSize = model.layers[0].input.shape.as_list()[1]
    state = getAgentState(quantity, 0, windowSize + 1)
    cuttent_Quantity = 0
    agent.inventory = []
    multi_agent = True
    purchase_arr = []
    sold_arr = []
    while multi_agent == True:
        for t in range(length):
            action = agent.act(state)
            nextState = getAgentState(quantity, t + 1, windowSize + 1)
            rewardValue = 0
            if action == 1: # buy
                agent.inventory.append(quantity[t])
                purchase_arr.append(quantity[t])
        
            elif action == 2 and len(agent.inventory) > 0:
                old_quantity = agent.inventory.pop(0)
                rewardValue = max(quantity[t] - old_quantity, 0)
                cuttent_Quantity = old_quantity - quantity[t] 
                if  old_quantity > quantity[t]:
                    sold_arr.append(old_quantity - quantity[t])
                else:
                    sold_arr.append(quantity[t] - old_quantity)
            done = True if t == length - 1 else False
            print(str(rewardValue)+" "+str(current_reward))
            if rewardValue > current_reward and multi_agent == True:
                extension_rewards.append(rewardValue)
                multi_agent = False
            agent.memory.append((state, action, rewardValue, nextState, done))
            state = nextState

def extensionSimulation():
    global rewards, extension_rewards
    start = 0
    text.delete('1.0', END)
    while start < len(rewards):
        runMultiAgent(rewards[start])
        start = start + 1
    text.insert(END,"Reward earned by Extension Multiagent: "+str(extension_rewards))
    

font = ('times', 15, 'bold')
title = Label(main, text='Effective Management for Blockchain-Based Agri-Food Supply Chains Using Deep Reinforcement Learning')
title.config(bg='bisque', fg='purple1')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 13, 'bold')

l1 = Label(main, text='Product ID :')
l1.config(font=font1)
l1.place(x=50,y=100)

tf1 = Entry(main,width=20)
tf1.config(font=font1)
tf1.place(x=180,y=100)

l2 = Label(main, text='Product Name :')
l2.config(font=font1)
l2.place(x=50,y=150)

tf2 = Entry(main,width=20)
tf2.config(font=font1)
tf2.place(x=180,y=150)

l3 = Label(main, text='Description :')
l3.config(font=font1)
l3.place(x=50,y=200)

tf3 = Entry(main,width=80)
tf3.config(font=font1)
tf3.place(x=180,y=200)

l3 = Label(main, text='User Type :')
l3.config(font=font1)
l3.place(x=50,y=250)

user = ['Providers','Farmers','Processors','Distributors','Retailers','Consumers']
userlist = ttk.Combobox(main,values=user,postcommand=lambda: userlist.configure(values=user)) 
userlist.place(x=180,y=250)
userlist.current(0)
userlist.config(font=font1)  

saveButton = Button(main, text="Save ASC Details in Blockchain", command=saveASCDetails)
saveButton.place(x=50,y=300)
saveButton.config(font=font1)

verifyButton = Button(main, text="Get ASC Details from Blockchain", command=getASCDetails)
verifyButton.place(x=330,y=300)
verifyButton.config(font=font1)

drlButton = Button(main, text="Deep Reinforcement Learning Simulation", command=DRLSimulation)
drlButton.place(x=625,y=300)
drlButton.config(font=font1)

extButton = Button(main, text="Extension Asynchronous MultiAgent Simulation", command=extensionSimulation)
extButton.place(x=985,y=300)
extButton.config(font=font1)

rewardsButton = Button(main, text="Rewards Graph", command=rewardGraph)
rewardsButton.place(x=50,y=350)
rewardsButton.config(font=font1)

graphButton = Button(main, text="Blockchain Computation Graph", command=graph)
graphButton.place(x=330,y=350)
graphButton.config(font=font1)

getButton = Button(main, text="Get All Blockchain Products ID", command=getProduct)
getButton.place(x=625, y=350)
getButton.config(font=font1)

font1 = ('times', 13, 'bold')
text=Text(main,height=15,width=120)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=400)
text.config(font=font1)

main.config(bg='cornflower blue')
main.mainloop()
