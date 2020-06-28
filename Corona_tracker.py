from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter as tk
import os
import getpass
import datetime
from time import sleep
import matplotlib.pyplot as plt
import sys
import pandas as pd
import time
    
def plotting():
    global filtered_data
    plt.rcdefaults()
    x=filtered_data[0][1:]
    y=filtered_data[1][1:]
    x.reverse()
    y.reverse()
    plt.barh(x,y,label="Confirmed")
    x=filtered_data[0][1:]
    y=filtered_data[2][1:]
    x.reverse()
    y.reverse()
    plt.barh(x,y,color="red",label="Active")
    plt.ylabel("State")
    plt.xlabel("Confirmed/active cases")
    plt.legend()
    #plt.tick_params(axis ='x', rotation =90) 
    plt.show()

    
def load_tree():
    global filtered_data
    
    state=filtered_data[0]
    confirmed=filtered_data[1]
    active=filtered_data[2]
    length=len(state)   
    tree.delete(*tree.get_children())
    for i in range(1,length):
        tree.insert("",index=END,values=(confirmed[i],active[i]),text=state[i])
    
    
def search(event):
    global filtered_data
    
    tree.delete(*tree.get_children()) 
    search_element = event.widget.get()
    search_element = search_element.strip().lower()    
    for i in range(0,len(filtered_data[0])):
        if search_element in filtered_data[0][i].strip().lower():
            tree.insert("",index=END,values=(filtered_data[1][i],filtered_data[2][i]),text=filtered_data[0][i])
            
def load_data():
    progress['value'] = 10
    global messageflag
    if messageflag==1:
        window.update_idletasks()     
        messageanswer=messagebox.askquestion("Alert!!","Do you want to refresh the page?")
    else:
        messageanswer="yes"
    if messageanswer=="yes":
        global filtered_data
        progress['value'] = 20
        window.update_idletasks() 
        date=str(datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S"))
        URL='https://api.covid19india.org/csv/latest/state_wise.csv'               
    
        data=pd.read_csv(URL)
        progress['value'] = 50
        window.update_idletasks() 
        required_columns=['State', 'Confirmed','Active']
        state=list(data['State'])
        confirmed=list(data['Confirmed'])
        active=list(data['Active'])
        val=state.index('Andhra Pradesh')
        l3=str(confirmed[val])
        val=state.index('Total')
        l4=str(confirmed[val])
        
        title2=l3.center(text_width," ")+l4.center(text_width," ")
        
        values.config(text=title2)
    
        time.sleep(1)
        progress['value'] = 100
        window.update_idletasks() 
        progress['value'] = 0
        window.update_idletasks() 
        filtered_data.append(state)
        filtered_data.append(confirmed)
        filtered_data.append(active)
        status.config(text="Last updated "+date)
        load_tree()
 
filtered_data=[]
window=Tk()
window.title("Covid-Tracker INDIA")
text_width=20
#window.geometry("300x400")
search_label=Label(window,text="Search by State")
search_box=Entry(window)
search_box.bind('<Key>',search)
frame=Frame(window)
l1="Andhra Cases"
l2="India Cases"
l3="--"
l4="--"
title1=l1.center(text_width," ")+l2.center(text_width," ")
title2=l3.center(text_width," ")+l4.center(text_width," ")
title=Label(window, text=title1)
values=Label(window, text=title2)
status=Label(window,text="Status not available")
progress = Progressbar(frame, orient = HORIZONTAL,length = 100, mode = 'determinate') 
refresh_button=Button(frame,text="Refresh",command=load_data)
plot_button=Button(frame,text="Plot",command=plotting)
tree = Treeview(window,column=("first","second"))
tree.heading("#0",text="State")
tree.column("#0", width=100)
tree.heading("first",text="Confirmed")
tree.column("first", width=50)
tree.heading("second",text="Active")
tree.column("second", width=50)
search_label.pack(padx=5,pady=5)
search_box.pack(fill='x',padx=5,pady=5)
vsb = Scrollbar(window, orient="vertical", command=tree.yview)
vsb.pack(side='right')
tree.configure(yscrollcommand=vsb.set)
tree.pack(expand=TRUE,fill=tk.BOTH, padx=5,pady=5) 

title.pack(fill=tk.BOTH,padx=5,pady=5)
values.pack(fill=tk.BOTH,padx=5,pady=5)
status.pack(anchor=CENTER)
refresh_button.pack(expand=TRUE,fill='x',side='left',anchor=CENTER,padx=5,pady=5)
plot_button.pack(expand=TRUE,fill='x',side='right',anchor=CENTER,padx=5,pady=5)
progress.pack(expand=TRUE,fill='x',anchor='center',padx=5,pady=5)
frame.pack(fill='x',expand=TRUE)
#window.iconbitmap('corona-virus.ico')
try:
    messageflag=0
    load_data()
    date=str(datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S"))
    status.config(text="Last updated: "+date)
    
except:
    status.config(text="could not load data")
messageflag=1    
window.mainloop()


