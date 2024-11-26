from tkinter import *
from tkinter import ttk
import database
# getAllData()，回傳一個list包含所有消費紀錄的(Year, Month, Date, Time, Name, Price)
# getAllTag(Tag)，以list回傳所有使用到此Tag名稱(string)的資料

year=-1
month=0
date=0
tag=-1
name=""
valueOrMin=-1
max=-1

data=getAllData()

def getYear():
    allYear=()
    for row in data:
        allYear.add(row[0])
    return allYear

def searchDate(year, month, date):
    newData=[]
    for row in data:
        if(row[0]==year and row[1]==month and row[2]==data):
            newData.append(row)
    data[:]=newData
def searchMonth(year, month):
    newData=[]
    for row in data:
        if(row[0]==year and row[1]==month):
            newData.append(row)
    data[:]=newData
def searchTag(name):

def searchItem(name):
    newData=[]
    for row in data:
        if(row[4]==name):
            newData.append(row)
    data[:]=newData
def searchAmount(value):
    newData=[]
    for row in data:
        if(row[5]==value):
            newData.append(row)
    data[:]=newData
def searchRange(min, max):
    newData=[]
    for row in data:
        if(min<=row[5]<=max):
            newData.append(row)
    data[:]=newData

def showResult():
    reslutWindow = Tk()
    reslutWindow.title("Result")

    headers = ["Year", "Month", "Date", "Time", "Name", "Price"]
    widths = [6, 5, 6, 5, 20, 7]

    for col, (header, width) in enumerate(zip(headers, widths)):
        header_label = Label(reslutWindow, text=header, font=("Courier New", 10, "bold"), width=width, anchor="center", bg="lightblue")
        header_label.grid(row=0, column=col, padx=0, pady=0, sticky="nsew")

    #data output, background color: odd-lightblue, even-white
    for row_idx, row in enumerate(data, start=2):
        row_color = "white" if row_idx % 2 == 0 else "lightblue"
        
        for col_idx, (value, width) in enumerate(zip(row, widths)):
            #if the value is float, choose to the second charactor after point
            if isinstance(value, float):
                value = f"{value:.2f}"
            row_label = Label(reslutWindow, text=value, font=("Courier New", 10), width=width, anchor="center", bg=row_color)
            row_label.grid(row=row_idx, column=col_idx, padx=0, pady=0, sticky="nsew") #sticky:full, no space to eachother

    #let the table size change with the window
    for col in range(6):
        reslutWindow.grid_columnconfigure(col, weight=1)
    for row in range(len(data) + 2):
        reslutWindow.grid_rowconfigure(row, weight=1)

    reslutWindow.mainloop()

def search():
    if(yearBox.current()>=0):
        year=yearBox.get()
        month=monthBox.get(1.0, 'end-1c')
        if(1<=month<=12):
            errorWindow()
            data[:]=getAllData()
            return
        date=dateBox.get(1.0, 'end-1c')
        endDate=0;
        if(month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12):
            endDate=31
        elif(month==2):
            if(year%4==0):
                endDate=29
            else:
                endDate=28
        elif(month==4 or month==6 or month==9 or month==11):
            endDate=30
        if(1<=date<=endDate):
            searchDate(year,month,date)
        else:
            searchMonth(year,month)
    if(tagBox.current()>=0):
        tag=tagBox.get()
        searchTag()
    name=itemBox.get(1.0, 'end-1c')
    if(name!=0):
        searchItem(name)
    valueOrMin=minBox.get(1.0, 'end-1c')
    max=maxBox.get(1.0, 'end-1c')
    if(valueOrMin!=-1):
        if(max==-1):
            searchAmount(valueOrMin)
        else:
            searchRange(valueOrMin, max)
    showResult()
    data[:]=getAllData()

def errorWindow():
    errorWindow=Tk()
    window.title("Error")
    Label(errorWindow, text="Input unvalid!\nPlease check your input!").grid(padx=10,pady=5)
    errorWindow.mainloop()
    
window=Tk()
window.title("Search")

Label(window, text="Date:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
Label(window, text="Tag:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
Label(window, text="Item:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
Label(window, text="Price:").grid(row=5, column=0, padx=10, pady=5, sticky="w")

Label(window, text="Year:").grid(row=0, column=1, padx=10, pady=5, sticky="w")
Label(window, text="Month:").grid(row=1, column=1, padx=10, pady=5, sticky="w")
Label(window, text="Date:").grid(row=2, column=1, padx=10, pady=5, sticky="w")

yearBox = ttk.Combobox(window, values=getYear(), width=5)
yearBox.grid(row=0, column=2, padx=10, pady=5, sticky="w")

monthBox = Text(window, height=1, width=3)
monthBox.grid(row=1, column=2, padx=10, pady=5, sticky="w")

dateBox = Text(window, height=1, width=3)
dateBox.grid(row=2, column=2, padx=10, pady=5, sticky="w")

tagBox = ttk.Combobox(window, values=getAllTag())
tagBox.grid(row=3, column=2, padx=10, pady=5, sticky="w")

itemBox = Text(window, height=1, width=21)
itemBox.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky="w")

minBox = Text(window, height=1, width=8)
minBox.grid(row=5, column=1, padx=10, pady=5, sticky="w")
Label(window, text="~").grid(row=5, column=2, padx=1, pady=2, sticky="w")
maxBox = Text(window, height=1, width=8)
maxBox.grid(row=5, column=2, padx=10, pady=5, sticky="e")

btn = Button(window, text='Search', command=search)
btn.grid(row=6, column=2, padx=10, pady=5, sticky="e")

window.mainloop()