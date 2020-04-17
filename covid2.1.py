from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import os
import getpass
import datetime
from time import sleep
import matplotlib.pyplot as plt

#Web scraping
import requests
import lxml.html as lh

def plotting():
     
     logpath=r"C:\\Users\\"+str(user_name)+"\\documents\\clog.txt"
     count=[]
     i_count=[]
     timestamp=[]
     reader=open(logpath,"r")
     for ele in reader:
            ele=ele.split()        
            count.append(ele[0].replace(',',""))
            i_count.append(ele[1].replace(',',""))
            timestamp.append(datetime.datetime.fromtimestamp(float(ele[2])))
     reader.close()
     plt.plot(timestamp,i_count,color="blue")
     plt.plot(timestamp,count,color="red")
     plt.gcf().autofmt_xdate()
     plt.show()

def logger(confirmed, india):
     
    date=datetime.datetime.now().timestamp()
    #date=date.strftime("%d-%m-%y %H-%M-%S")
    logpath="C:\\Users\\"+str(user_name)+"\\documents\\clog.txt"
    data=[]
    log_reader=open(logpath,"r")
    for ele in log_reader:
         data.append(str(ele).strip())
    log_reader.close()
    data.append(confirmed+"  "+india+"  "+str(date))
    log_writer=open(logpath,"w")
    for ele in data:
        log_writer.write(str(ele))
        log_writer.write("\n")
    log_writer.close()

def preloadlog():
  try:
    global logpath1
    global country_name
    global country_count
    global new_count
    
    if os.path.getsize(logpath1)==0:
        return    
    read=open(logpath1,"r")
    file = read.readlines()
    status.configure(text="Last updated "+file[0])  
    for i in range(2,len(file)):
        data=file[i].split()
        country_name.append(data[0])
        country_count.append(data[1])
        new_count.append(data[2])
        tree.insert("",index=END,values=(data[1],data[2]),text=data[0])
    read.close()
  except:
    status.configure(text="Sorry, could not process prelog")
    
def web_scrapper():
  try:
    global country_name
    global country_count
    global new_count
    tree.delete(*tree.get_children())
    country_name=[]
    country_count=[]
    new_count=[]
    
    status.configure(text="Please wait, loading" )      
    progress['value'] = 0
    window.update_idletasks()         
    progress['value'] = 10
    window.update_idletasks() 
    url='https://www.worldometers.info/coronavirus/#countries'
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')     
    predata_writer=open(logpath1,"w")
    predata_writer.write(str(datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S"))+"\n")
    for ele in tr_elements:
         name=ele.text_content()           
         name=name.split()         
         if name[1].replace(',',"").isdigit():
                country_name.append(name[0])
                country_count.append(name[1])            
                new_count.append(name[2])
                predata_writer.write(name[0]+" "+name[1]+" "+name[2]+"\n") 
         else:                
                country_name.append(name[0]+" "+name[1])
                country_count.append(name[2])
                new_count.append(name[3])  
                predata_writer.write(name[0]+name[1]+" "+name[2]+" "+name[3]+"\n") 
    predata_writer.close()                      
    for i in range(1,len(country_name)):
        tree.insert("",index=END,values=(country_count[i],new_count[i]),text=country_name[i])
    progress['value'] = 40
    window.update_idletasks()     
    confirmed = doc.xpath('.//div[@class="maincounter-number"]')
    data=[]
    for ele in confirmed:
         data.append(ele.text_content().strip())
    confirmed=data[0]        
    progress['value'] = 80
    window.update_idletasks()     
    india=country_name.index("India")
    l3=confirmed
    l4=country_count[india]
    title2=l3.center(text_width," ")+l4.center(text_width," ")
    values.configure(text=title2)
    status.configure(text="")
    logger(confirmed, str(name[1]))    
    progress['value'] = 100
    window.update_idletasks()     
    sleep(1)        
    progress['value'] = 0
    window.update_idletasks() 

  except:
    progress['value'] = 0
    window.update_idletasks()
    sleep(2)
    preloadlog()
    status.configure(text="Network error!!, please try again")    
    return
        
def search(event):
    global country_name
    global country_count
    global new_count
    
    tree.delete(*tree.get_children()) 
    search_element = event.widget.get()
    search_element = search_element.strip().lower()    
    for i in range(0,len(country_name)):
        if search_element in country_name[i].strip().lower():
            tree.insert("",index=END,values=(country_count[i],new_count[i]),text=country_name[i])
              
user_name=getpass.getuser()
logpath="C:\\Users\\"+str(user_name)+"\\documents\\clog.txt"
logpath1="C:\\Users\\"+str(user_name)+"\\documents\\clogtemp.txt"
if not os.path.exists(logpath):
   
    write=open(logpath,"w")
    write.close()
    write=open(logpath1,"w")
    write.close()
    print("log file created")
  
country_name=[]
country_count=[]
new_count=[]
window=Tk()
window.title("Covid-Tracker")
text_width=20

search_label=Label(window,text="Search by country:")
search_box=Entry(window)
search_box.bind('<Key>',search)

l1="Global Cases"
l2="India Cases"
l3="--"
l4="--"
title1=l1.center(text_width," ")+l2.center(text_width," ")
title2=l3.center(text_width," ")+l4.center(text_width," ")
title=Label(window, text=title1)
values=Label(window, text=title2)
status=Label(window,text="Status not available")
progress = Progressbar(window, orient = HORIZONTAL,length = 100, mode = 'determinate') 
refresh_button=Button(window,text="Refresh",command=web_scrapper)
plot_button=Button(window,text="Plot",command=plotting)
tree = Treeview(window, height=7,column=("first","second"))
tree.heading("#0",text="Country")
tree.column("#0", width=50)
tree.heading("first",text="TotalCases")
tree.column("first", width=50)
tree.heading("second",text="New Cases")
tree.column("second", width=50)
search_label.pack(padx=5,pady=5)
search_box.pack(fill='x',padx=5,pady=5)
vsb = Scrollbar(window, orient="vertical", command=tree.yview)
vsb.pack(side='right')
tree.configure(yscrollcommand=vsb.set)
tree.pack(fill=tk.BOTH, padx=5,pady=5)
#tree.insert("", index="end", text="main branch")
#display=Listbox(window, height=7, width=45)
#display.pack(padx=5,pady=5)
preloadlog()
title.pack(padx=5,pady=5)
values.pack(padx=5,pady=5)
status.pack(anchor=CENTER)
refresh_button.pack(side='left',anchor=CENTER,padx=5,pady=5)
plot_button.pack(side='right',anchor=CENTER,padx=5,pady=5)
progress.pack(anchor=CENTER,padx=5,pady=5)
window.resizable(0,0)
window.mainloop()