from tkinter import *
import database
# getAllData()，回傳一個list包含所有消費紀錄的(Year, Month, Date, Time, Name, Price)
# getAllTag(Tag)，以list回傳所有使用到此Tag名稱(string)的資料

data=getAllData()
allYear=[]

def getYear():
    for row in data:
        allYear.append(row[0])

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
        if(row[5]>=min and row[5]<=max):
            newData.append(row)
    data[:]=newData

def showResult():
    reslutWindow = Tk()
    reslutWindow.title("Result")

    headers = ["Year", "Month", "Date", "Time", "Name", "Price"]
    widths = [6, 5, 6, 5, 20, 7]  # Widths for each column

    for col, (header, width) in enumerate(zip(headers, widths)):
        header_label = Label(reslutWindow, text=header, font=("Courier New", 10, "bold"), width=width, anchor="center", bg="lightblue")
        header_label.grid(row=0, column=col, padx=0, pady=0, sticky="nsew")

    # Loop through the data and display it in the grid
    for row_idx, row in enumerate(data, start=2):  # Start from row 2, right after the separator
        # Alternate row colors: white for even, lightblue for odd rows
        row_color = "white" if row_idx % 2 == 0 else "lightblue"
        
        for col_idx, (value, width) in enumerate(zip(row, widths)):
            # Format price to 2 decimal places
            if isinstance(value, float):
                value = f"{value:.2f}"
            row_label = Label(reslutWindow, text=value, font=("Courier New", 10), width=width, anchor="center", bg=row_color)
            row_label.grid(row=row_idx, column=col_idx, padx=0, pady=0, sticky="nsew")  # No padding, sticky to fill the cell

    # Make the columns and rows expand to fill available space
    for col in range(6):
        reslutWindow.grid_columnconfigure(col, weight=1)
    for row in range(len(data) + 2):  # Add 2 for the header and separator
        reslutWindow.grid_rowconfigure(row, weight=1)

    reslutWindow.mainloop()

window=Tk()
window.title("Search")

Label(window, text="Date:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
Label(window, text="Tag:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
Label(window, text="Item:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
Label(window, text="Price:").grid(row=5, column=0, padx=10, pady=5, sticky="w")

window.mainloop()