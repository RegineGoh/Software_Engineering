from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import matplotlib
import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime
from database import Database

database = Database()

class StatisticWindow:
    def __init__(self):
        self.database = database
        self.data = database.getAllData()
        self.init_ui()

    def get_data_within_date_range(self, start_date, end_date):
        return [row for row in self.data if start_date <= datetime(row[0], row[1], row[2]) <= end_date]

    def show_detail(self, filtered_data):
        detail_window = Toplevel()
        detail_window.title("Statistic Detail")

        headers = ["Year", "Month", "Date", "Time", "Item", "Price"]
        widths = [6, 5, 6, 5, 20, 7]

        # 設置標題欄
        for col, (header, width) in enumerate(zip(headers, widths)):
            Label(detail_window, text=header, font=("Courier New", 10, "bold"), width=width, bg="lightblue").grid(row=0, column=col, sticky="nsew")

        # 顯示資料
        for row_idx, row in enumerate(filtered_data, start=1):
            row_color = "white" if row_idx % 2 == 0 else "lightblue"
            for col_idx, (value, width) in enumerate(zip(row, widths)):
                if isinstance(value, float):
                    value = f"{value:.2f}"
                Label(detail_window, text=value, font=("Courier New", 10), width=width, bg=row_color).grid(row=row_idx, column=col_idx, sticky="nsew")

        for col in range(len(headers)):
            detail_window.grid_columnconfigure(col, weight=1)

    def show_chart(self, filtered_data):
        # 初始化標籤的總價格
        tag_totals = {tag: 0 for tag in self.database.getTagName()}

        # 如果沒有標籤資料，顯示提示信息
        if not tag_totals:
            messagebox.showinfo("No Tags", "No tags found for the selected data.")
            return

        # 遍歷篩選出的資料
        for record in filtered_data:
            # 每筆資料的 `Data_No`（從索引 0 開始推算）
            data_no = filtered_data.index(record) + 1

            # 取得該資料的所有標籤
            tags = self.database.getTagsByDataNo(data_no)

            # 取得該資料的價格
            price = record[-1]  # 假設價格在最後一個欄位

            # 累加價格到每個標籤
            for tag in tags:
                if tag in tag_totals:
                    tag_totals[tag] += price

        # 如果所有標籤的價格總和為 0，則顯示提示
        if all(value == 0 for value in tag_totals.values()):
            messagebox.showinfo("No Data", "No data available for the selected tags.")
            return
                
        labels = [tag for tag, total in tag_totals.items() if total > 0]
        sizes = [total for total in tag_totals.values() if total > 0]
        colors = plt.cm.Paired(range(len(labels)))

        # 顯示圓餅圖
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        plt.title("Tags Distribution")
        plt.axis('equal')  # 圓形比例
        plt.show()

    # def search(self):
        # 取得開始日期
        try:
            start_year = int(self.start_yearBox.get())
            start_month = int(self.start_monthBox.get())
            start_day = int(self.start_dateBox.get())
            start_date = datetime(start_year, start_month, start_day)
        except ValueError:
            # 當日期格式錯誤時，設置為最早的日期
            messagebox.showerror("Input Error", "Invalid start date. Setting to the earliest available date.")
            start_date = min(datetime(row[0], row[1], row[2]) for row in self.data)  # 設定最早的日期

        # 取得結束日期
        try:
            end_year = int(self.end_yearBox.get())
            end_month = int(self.end_monthBox.get())
            end_day = int(self.end_dateBox.get())
            end_date = datetime(end_year, end_month, end_day)
        except ValueError:
            # 當日期格式錯誤時，設置為最晚的日期
            messagebox.showerror("Input Error", "Invalid end date. Setting to the latest available date.")
            end_date = max(datetime(row[0], row[1], row[2]) for row in self.data)  # 設定最晚的日期

        # 篩選資料
        filtered_data = self.get_data_within_date_range(start_date, end_date)

        if len(filtered_data) == 0:
            messagebox.showinfo("No Data", "No data found for the given date range.")
            return

        if self.detail_var.get():
            self.show_detail(filtered_data)

        if self.chart_var.get():
            self.show_chart(filtered_data)

    def search(self):
        start_date = self.get_date_from_input(self.start_yearBox, self.start_monthBox, self.start_dateBox, "start")
        end_date = self.get_date_from_input(self.end_yearBox, self.end_monthBox, self.end_dateBox, "end")

        filtered_data = self.get_data_within_date_range(start_date, end_date)

        if len(filtered_data) == 0:
            messagebox.showinfo("No Data", "No data found for the given date range.")
            return

        if self.detail_var.get():
            self.show_detail(filtered_data)

        if self.chart_var.get():
            self.show_chart(filtered_data)

    def get_date_from_input(self, year_box, month_box, date_box, date_type):
        try:
            year = int(year_box.get())
            month = int(month_box.get())
            day = int(date_box.get())
            return datetime(year, month, day)
        except ValueError:
            messagebox.showerror(f"{date_type.capitalize()} Date Error", f"Invalid {date_type} date. Setting to the earliest/latest available date.")
            default_date = min(datetime(row[0], row[1], row[2]) for row in self.data) if date_type == "start" else max(datetime(row[0], row[1], row[2]) for row in self.data)
            return default_date

    def update_dates(self, year_box, month_box, date_box, is_start=True):
        try:
            year = int(year_box.get())
            month = int(month_box.get())
        except ValueError:
            date_box["values"] = []
            return

        days = self.get_days_in_month(year, month)
        date_box["values"] = [str(day) for day in range(1, days + 1)]

    def get_days_in_month(self, year, month):
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        elif month == 2:
            return 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
        return 0

    def create_date_input(self, window, prefix, start_row, start_col):
        current_year = datetime.now().year
        Label(window, text=f"{prefix} Date:").grid(row=start_row, column=0, padx=5, pady=5, sticky="w")

        Label(window, text="Year:").grid(row=start_row, column=start_col, padx=5, pady=5, sticky="w")
        year_box = ttk.Combobox(window, values=[str(year) for year in range(current_year - 20, current_year + 1)], width=10)
        year_box.grid(row=start_row, column=start_col + 1, padx=5, pady=5, sticky="w")

        Label(window, text="Month:").grid(row=start_row + 1, column=start_col, padx=5, pady=5, sticky="w")
        month_box = ttk.Combobox(window, values=[str(month) for month in range(1, 13)], width=5)
        month_box.grid(row=start_row + 1, column=start_col + 1, padx=5, pady=5, sticky="w")

        Label(window, text="Date:").grid(row=start_row + 2, column=start_col, padx=5, pady=5, sticky="w")
        date_box = ttk.Combobox(window, width=5)
        date_box.grid(row=start_row + 2, column=start_col + 1, padx=5, pady=5, sticky="w")

        year_box.bind("<<ComboboxSelected>>", lambda e: self.update_dates(year_box, month_box, date_box, True))
        month_box.bind("<<ComboboxSelected>>", lambda e: self.update_dates(year_box, month_box, date_box, True))

        return year_box, month_box, date_box

    def init_ui(self):
        window = Tk()
        window.title("Statistic Search")

        self.start_yearBox, self.start_monthBox, self.start_dateBox = self.create_date_input(window, "Start", 0, 1)
        self.end_yearBox, self.end_monthBox, self.end_dateBox = self.create_date_input(window, "End", 3, 1)

        self.detail_var = BooleanVar()
        self.chart_var = BooleanVar()

        Checkbutton(window, text="Show Detail", variable=self.detail_var).grid(row=6, column=0, padx=10, pady=5, sticky="w")
        Checkbutton(window, text="Show Chart", variable=self.chart_var).grid(row=7, column=0, padx=10, pady=5, sticky="w")

        search_btn = Button(window, text="Get statistic", command=self.search)
        search_btn.grid(row=8, column=0, columnspan=2, pady=10)

        window.mainloop()

    # def init_ui(self):
        window = Tk()
        window.title("Statistic Search")
        # window.geometry("600x400")  # 設定視窗大小為 600x400

        Label(window, text="Start Date:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        # 開始年份選單
        current_year = datetime.now().year
        Label(window, text="Year:").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.start_yearBox = ttk.Combobox(window, values=[str(year) for year in range(current_year - 20, current_year + 1)], width=10)
        self.start_yearBox.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.start_yearBox.bind("<<ComboboxSelected>>", self.start_year_selected)

        # 開始月份選單
        Label(window, text="Month:").grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.start_monthBox = ttk.Combobox(window, values=[str(month) for month in range(1, 13)], width=5)
        self.start_monthBox.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.start_monthBox.bind("<<ComboboxSelected>>", self.start_month_selected)

        # 開始日期選單
        Label(window, text="Date:").grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.start_dateBox = ttk.Combobox(window, width=5)
        self.start_dateBox.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # 設定結束日期輸入
        Label(window, text="End Date:").grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # 結束年份選單
        current_year = datetime.now().year
        Label(window, text="Year:").grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.end_yearBox = ttk.Combobox(window, values=[str(year) for year in range(current_year - 20, current_year + 1)], width=10)
        self.end_yearBox.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.end_yearBox.bind("<<ComboboxSelected>>", self.end_year_selected)

        # 結束月份選單
        Label(window, text="Month:").grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.end_monthBox = ttk.Combobox(window, values=[str(month) for month in range(1, 13)], width=5)
        self.end_monthBox.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.end_monthBox.bind("<<ComboboxSelected>>", self.end_month_selected)

        # 結束日期選單
        Label(window, text="Date:").grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.end_dateBox = ttk.Combobox(window, width=5)
        self.end_dateBox.grid(row=5, column=2, padx=5, pady=5, sticky="w")


        # 勾選框：顯示細節與圖表
        self.detail_var = BooleanVar()
        self.chart_var = BooleanVar()

        Checkbutton(window, text="Show Detail", variable=self.detail_var).grid(row=6, column=0, padx=10, pady=5, sticky="w")
        Checkbutton(window, text="Show Chart", variable=self.chart_var).grid(row=7, column=0, padx=10, pady=5, sticky="w")

        # 按鈕：搜尋並顯示結果
        search_btn = Button(window, text="Get statistic", command=self.search)
        search_btn.grid(row=8, column=0, columnspan=2, pady=10)

        window.mainloop()

    # def start_year_selected(self, event=None):
    #     """當年份選擇時清空月份和日期"""
    #     self.start_monthBox.set("")
    #     self.start_dateBox.set("")
    #     self.start_dateBox["values"] = []

    # def start_month_selected(self, event=None):
    #     """當月份選擇時更新日期選單"""
    #     self.start_dateBox.set("")
    #     self.update_start_dates()

    # def update_start_dates(self, event=None):
    #     try:
    #         year = int(self.start_yearBox.get())
    #         month = int(self.start_monthBox.get())
    #     except ValueError:
    #         # 若年份或月份未選擇，清空日期選單
    #         self.start_dateBox["values"] = []
    #         return

    #     # 計算該月的天數
    #     if month in [1, 3, 5, 7, 8, 10, 12]:
    #         days = 31
    #     elif month in [4, 6, 9, 11]:
    #         days = 30
    #     elif month == 2:
    #         # 閏年判斷
    #         days = 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
    #     else:
    #         days = 0

    #     # 更新日期選單
    #     self.start_dateBox["values"] = [str(day) for day in range(1, days + 1)]

    # def end_year_selected(self, event=None):
    #     """當年份選擇時清空月份和日期"""
    #     self.end_monthBox.set("")
    #     self.end_dateBox.set("")
    #     self.end_dateBox["values"] = []

    # def end_month_selected(self, event=None):
    #     """當月份選擇時更新日期選單"""
    #     self.end_dateBox.set("")
    #     self.update_end_dates()

    # def update_end_dates(self, event=None):
        try:
            year = int(self.end_yearBox.get())
            month = int(self.end_monthBox.get())
        except ValueError:
            # 若年份或月份未選擇，清空日期選單
            self.end_dateBox["values"] = []
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
        self.end_dateBox["values"] = [str(day) for day in range(1, days + 1)]

    # def start_year_selected(self, event=None):
    #     """當年份選擇時清空月份和日期"""
    #     self.start_monthBox.set("")
    #     self.start_dateBox.set("")
    #     self.start_dateBox["values"] = []

    # def start_month_selected(self, dateBox, event=None):
    #     """當月份選擇時更新日期選單"""
    #     self.start_dateBox.set("")
    #     self.update_start_dates()

    #     def update_start_dates(self, event=None):
    #     try:
    #         year = int(self.start_yearBox.get())
    #         month = int(self.start_monthBox.get())
    #     except ValueError:
    #         # 若年份或月份未選擇，清空日期選單
    #         self.start_dateBox["values"] = []
    #         return

    #     # 計算該月的天數
    #     if month in [1, 3, 5, 7, 8, 10, 12]:
    #         days = 31
    #     elif month in [4, 6, 9, 11]:
    #         days = 30
    #     elif month == 2:
    #         # 閏年判斷
    #         days = 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
    #     else:
    #         days = 0

    #     # 更新日期選單
    #     self.start_dateBox["values"] = [str(day) for day in range(1, days + 1)]


app = StatisticWindow()

# # 測試：
# from database import Database
# database = Database()
# database.insertData(2024, 8, 30, 1222, "Lunch", 130)
# database.insertTag(1, "Food")
# database.insertData(2024, 8, 31, 1422, "Dinner", 150)
# database.insertTag(2, "Food")
# database.insertData(2024, 9, 1, 1022, "Taxi", 200)
# database.insertTag(3, "Transport")
# app = StatisticWindow(database)