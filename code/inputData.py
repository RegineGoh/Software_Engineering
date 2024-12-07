# 檔案名稱: inputData.py
#從由使用者輸入改使用下拉式選單（年月日） -> 防呆

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import Database
from datetime import datetime

database = Database()

class InputDataWindow:
    def __init__(self):
        self.init_ui()

    def init_ui(self):
        # 主視窗
        self.window = Tk()
        self.window.title("Input Data")
        self.window.geometry("400x500")

        # 年份選單
        Label(self.window, text="Year:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        current_year = datetime.now().year
        self.yearBox = ttk.Combobox(self.window, values=[str(year) for year in range(current_year - 20, current_year + 1)], width=10)
        self.yearBox.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.yearBox.bind("<<ComboboxSelected>>", self.update_dates)

        # 月份選單
        Label(self.window, text="Month:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.monthBox = ttk.Combobox(self.window, values=[str(month) for month in range(1, 13)], width=10)
        self.monthBox.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.monthBox.bind("<<ComboboxSelected>>", self.update_dates)

        # 日期選單
        Label(self.window, text="Date:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.dateBox = ttk.Combobox(self.window, width=10)
        self.dateBox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # 時間輸入框
        Label(self.window, text="Time (HH:MM):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.timeBox = Entry(self.window, width=10)
        self.timeBox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # 物品名稱輸入框
        Label(self.window, text="Item Name:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.itemBox = Entry(self.window, width=20)
        self.itemBox.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # 價格輸入框
        Label(self.window, text="Price:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.priceBox = Entry(self.window, width=10)
        self.priceBox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # 標籤選單
        Label(self.window, text="Tag:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.tagBox = ttk.Combobox(self.window, values=database.getTagName(), width=18)
        self.tagBox.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # 提交按鈕
        Button(self.window, text="Submit", command=self.submit_data).grid(row=7, column=1, padx=10, pady=20, sticky="e")

        self.window.mainloop()

    def update_dates(self, event=None):
        """更新日期選單的內容"""
        try:
            year = int(self.yearBox.get())
            month = int(self.monthBox.get())
        except ValueError:
            # 若年份或月份未選擇，清空日期選單
            self.dateBox["values"] = []
            return

        # 計算該月的天數
        if month in [1, 3, 5, 7, 8, 10, 12]:
            days = 31
        elif month in [4, 6, 9, 11]:
            days = 30
        elif month == 2:
            # 閏年判斷
            days = 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
        else:
            days = 0

        # 更新日期選單
        self.dateBox["values"] = [str(day) for day in range(1, days + 1)]

    def submit_data(self):
        try:
            # 獲取輸入資料
            year = int(self.yearBox.get())
            month = int(self.monthBox.get())
            date = int(self.dateBox.get())

            # 檢查日期是否有效
            datetime(year, month, date)

            time_str = self.timeBox.get().strip()  # 取得時間字串，移除多餘空白
            if ":" not in time_str:
                raise ValueError("Time format must be HH:MM.")

            # 驗證時間格式
            try:
                hours, minutes = map(int, time_str.split(":"))
                if not (0 <= hours <= 23) or not (0 <= minutes <= 59):
                    raise ValueError
                time_int = hours * 100 + minutes  # 轉換為整數格式
            except ValueError:
                raise ValueError("Invalid time! Time must be in HH:MM format.")

            name = self.itemBox.get().strip()
            if not (1 <= len(name) <= 20):
                raise ValueError("Item name must be between 1 and 20 characters.")

            price = int(self.priceBox.get())
            if price <= 0:
                raise ValueError("Price must be a positive number.")

            # 新增資料到資料庫
            data_id = database.insertData(year, month, date, time_int, name, price)
            if data_id == 0:
                raise Exception("Failed to add data.")

            # 新增標籤
            tag = self.tagBox.get()
            if tag:
                database.insertTag(data_id, tag)

            messagebox.showinfo("Success", f"Data added successfully with ID: {data_id}")

            # 清空欄位
            self.yearBox.set("")
            self.monthBox.set("")
            self.dateBox.set("")
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
