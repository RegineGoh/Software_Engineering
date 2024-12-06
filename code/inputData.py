# 有GUI介面
# 可以輸入

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import Database

# 模擬資料庫類別（如果未提供資料庫實現，可用以下類別測試）
class Database:
    def __init__(self):
        self.data = []
        self.tags = {}

    def insertData(self, year, month, day, time, name, price):
        new_data = (year, month, day, time, name, price)
        self.data.append(new_data)
        return len(self.data)  # 回傳資料 ID

    def insertTag(self, data_id, tag):
        self.tags.setdefault(data_id, []).append(tag)
        return 1

    def getTagName(self):
        return ["Food", "Entertainment", "Transportation"]

    def getAllData(self):
        return self.data

database = Database()

class InputDataWindow:
    def __init__(self):
        self.init_ui()

    def init_ui(self):
        # 主視窗
        self.window = Tk()
        self.window.title("Input Data")
        self.window.geometry("400x500")

        # 標籤與輸入欄位
        Label(self.window, text="Year:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.yearBox = Entry(self.window, width=10)
        self.yearBox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        Label(self.window, text="Month:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.monthBox = Entry(self.window, width=10)
        self.monthBox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        Label(self.window, text="Date:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.dateBox = Entry(self.window, width=10)
        self.dateBox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        Label(self.window, text="Time (0000~2359):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.timeBox = Entry(self.window, width=10)
        self.timeBox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        Label(self.window, text="Item Name:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.itemBox = Entry(self.window, width=20)
        self.itemBox.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        Label(self.window, text="Price:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.priceBox = Entry(self.window, width=10)
        self.priceBox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        Label(self.window, text="Tag:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.tagBox = ttk.Combobox(self.window, values=database.getTagName(), width=18)
        self.tagBox.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # 按鈕
        Button(self.window, text="Submit", command=self.submit_data).grid(row=7, column=1, padx=10, pady=20, sticky="e")

        self.window.mainloop()

    def submit_data(self):
        try:
            # 獲取輸入資料
            year = int(self.yearBox.get())
            if not (1000 <= year <= 9999):
                raise ValueError("Year must be a valid 4-digit number.")

            month = int(self.monthBox.get())
            if not (1 <= month <= 12):
                raise ValueError("Month must be between 1 and 12.")

            date = int(self.dateBox.get())
            from datetime import datetime
            datetime(year, month, date)  # 檢查日期是否有效

            time = int(self.timeBox.get())
            if not (0 <= time <= 2359):
                raise ValueError("Time must be between 0000 and 2359.")

            name = self.itemBox.get().strip()
            if not (1 <= len(name) <= 20):
                raise ValueError("Item name must be between 1 and 20 characters.")

            price = int(self.priceBox.get())
            if price <= 0:
                raise ValueError("Price must be a positive number.")

            # 新增資料到資料庫
            data_id = database.insertData(year, month, date, time, name, price)
            if data_id == 0:
                raise Exception("Failed to add data.")

            # 新增標籤
            tag = self.tagBox.get()
            if tag:
                database.insertTag(data_id, tag)

            messagebox.showinfo("Success", f"Data added successfully with ID: {data_id}")

            # 清空輸入欄位
            self.yearBox.delete(0, END)
            self.monthBox.delete(0, END)
            self.dateBox.delete(0, END)
            self.timeBox.delete(0, END)
            self.itemBox.delete(0, END)
            self.priceBox.delete(0, END)
            self.tagBox.set("")

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# 啟動應用程式
app = InputDataWindow()
