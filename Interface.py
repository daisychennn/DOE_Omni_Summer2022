import tkinter as tk
from threading import *
from tkinter import messagebox
from PIL import ImageTk, Image
from libr.Data_Mining import ReadXML
from libr.produce_logo.imagestring import *
img = imageString # logo image

# to stop window resizing after clicking outputs
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
root.geometry("1650x700")
root.title("Big Data Analysis for Energy Application (Demo)")

def showWordCloud():
    get_path = path_entry.get()
    get_xml = xml_entry.get()
    get_name = saveImg_entry.get()
    
    get_keywords = []
    keywords = kw_entry.get()
    edit_keywords = ' '.join(keywords.split()) 
    get_keywords = edit_keywords.replace(" ,",",").replace(", ",",").split(",")
    
    get_years = [myListbox.get(i) for i in myListbox.curselection()]
    
    get_exclusions = []
    exclusions = ex_entry.get()
    edit_exclusions = ' '.join(exclusions.split())
    get_exclusions = edit_exclusions.replace(" ,",",").replace(", ",",").split(",")
    
    try:
        ReadXML(get_path, [get_xml], get_name, get_years, get_keywords, get_exclusions)
    except(FileNotFoundError,OSError):
        messagebox.showerror("Error", "Error: Check inputs for correct path or that database exists")
    except(IndexError):
        messagebox.showerror("Error", "Error: Keyword not found. Try a different year or new keyword.")
    get_xml = [get_xml]
    get_xml = get_xml[0].split('.')[0]
    
    image = ImageTk.PhotoImage(file=get_path+"/output/"+get_name+"-word-cloud.png")
    imagebox.config(image=image)
    imagebox.image = image


def showBarGraph():
    get_path = path_entry.get()
    get_xml = xml_entry.get()
    get_name = saveImg_entry.get()

    get_keywords = []
    keywords = kw_entry.get()
    edit_keywords = ' '.join(keywords.split()) 
    get_keywords = edit_keywords.replace(" ,",",").replace(", ",",").split(",")
    
    get_years = [myListbox.get(i) for i in myListbox.curselection()]
    
    get_exclusions = []
    exclusions = ex_entry.get()
    edit_exclusions = ' '.join(exclusions.split())
    get_exclusions = edit_exclusions.replace(" ,",",").replace(", ",",").split(",")
    
    try:
        ReadXML(get_path, [get_xml], get_name, get_years, get_keywords, get_exclusions)
    except(FileNotFoundError,OSError):
        messagebox.showerror("Error", "Error: Check inputs for correct path or that database exists")
    except(IndexError):
        messagebox.showerror("Error", "Error: Keyword not found. Try a different year or new keyword.")
    image = ImageTk.PhotoImage(file=get_path+"/output/"+get_name+"-frequencies.png")
    imagebox.config(image=image)
    imagebox.image = image

# multi-threading
def threadingWC():
    t1=Thread(target=showWordCloud)
    t1.start()
def threadingBG():
    t2=Thread(target=showBarGraph)
    t2.start()


# get path/directory
path_label = tk.Label(root, text="Enter database path:", font=('Helvetica',11))
path_label.grid(row=0, column=0, pady=5)
path_entry = tk.Entry(root, width=40, font=('Helvetica',11))
path_entry.grid(row=0, column=1)
path_entry.insert(0, "e.g. C:/Users/username/Documents")


# get xml file
xml_label = tk.Label(root, text="Enter the name of database file: \n (include .xml)", font=('Helvetica',11))
xml_label.grid(row=1, column=0, pady=5)
xml_entry = tk.Entry(root, width=40, font=('Helvetica',11))
xml_entry.grid(row=1, column=1)
xml_entry.insert(0, "demo.xml")


# save output
saveImg_label = tk.Label(root, text="Save output as: ", font=('Helvetica',11))
saveImg_label.grid(row=2, column=0, pady=5)
saveImg_entry = tk.Entry(root, width=40, font=('Helvetica',11))
saveImg_entry.grid(row=2, column=1)


# enter keywords
kw_label = tk.Label(root, text="Enter keyword(s):\n (separate by commas)", font=('Helvetica',11))
kw_label.place(x=850, y=3)
kw_entry = tk.Entry(root, width=40, font=('Helvetica',11))
kw_entry.place(x=1100, y=6)


# enter words to exclude
ex_label = tk.Label(root, text="Enter word(s) to exclude: \n (separate by commas)", font=("Helvetica",11))
ex_label.place(x=850, y=55)
ex_entry = tk.Entry(root, width=40, font=('Helvetica',11))
ex_entry.place(x=1100, y=60)


# choose from list (listbox)
myListbox=tk.Listbox(root, selectmode = "multiple", font=('Helvetica',11))
myListbox.place(x=1150, y=100)

# years = []
# for y in years:
    #myListbox.insert("end",y)

myListbox.insert("end", "2012")
myListbox.insert("end", "2013")
myListbox.insert("end", "2014")
myListbox.insert("end", "2015")
myListbox.insert("end", "2016")
myListbox.insert("end", "2017")
myListbox.insert("end", "2018")
myListbox.insert("end", "2019")
myListbox.insert("end", "2020")
myListbox.insert("end", "2021")
myListbox.insert("end", "2022")


# year selection
yr_label = tk.Label(root, text= "Click year(s) to select: ", font=('Helvetica',11))
yr_label.place(x=850, y=145)


# buttons
btn_label = tk.Label(root, text="Data analysis output:",  font=("Helvetica",11))
btn_label.place(x=45, y=165)
btn_wc = tk.Button(root, height=1, width=11, text="Word Cloud", command=threadingWC, font=('Helvetica',11))
btn_wc.place(x=315, y=160)
btn_bg = tk.Button(root, height=1, width=11, text="Bar Graph", command=threadingBG, font=('Helvetica',11))
btn_bg.place(x=495, y=160)


# display image
imagebox = tk.Label(root)
imagebox.place(x=100, y=245)


# show logos
# names typed in case photo does not appear
logo_label = tk.Label(root, text="Sponsors:", font=('Helvetica',11))
logo_label.place(x=940,y=425)
try:
    logo = tk.PhotoImage(data=img)
    label = tk.Label(root, image= logo)
    label.place(x=940, y=455)
except:
    names = tk.Label(root, text="Mickey Leland Energy Fellowship \n DOE Omni Technology Alliance \n National Energy Technology Lab \n Department of Energy",
                     font=("Helvetica",11))
    names.place(x=815,y=455)
    
root.mainloop()
