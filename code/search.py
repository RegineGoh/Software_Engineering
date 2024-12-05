from tkinter import *
from tkinter import ttk
from database import Database

database=Database()

class SearchWindow:
    def __init__(self):
        self.year = -1
        self.month = 0
        self.date = 0
        self.tag = database.getTagName()
        self.name = ""
        self.valueOrMin = -1
        self.max = -1
        self.data = database.getAllData()
        self.init_ui()

        database.insertData(2024, 8, 30, 1222, "lunch", 130)


    def get_years(self):
        years = set(row["Year"] for row in self.data)
        return list(years)

    def search_date(self, year, month, date):
        self.data = [row for row in self.data if row["Year"] == year and row["Month"] == month and row["Date"] == date]

    def search_month(self, year, month):
        self.data = [row for row in self.data if row["Year"] == year and row["Month"] == month]

    def search_tag(self, tag):
        self.data = [row for row in self.data if row["Data_No"] == database.getAllTag(tag)]

    def search_item(self, name):
        self.data = [row for row in self.data if row["Name"] == name]

    def search_amount(self, value):
        self.data = [row for row in self.data if row["Price"] == value]

    def search_range(self, min_val, max_val):
        self.data = [row for row in self.data if min_val <= row["Price"] <= max_val]

    def show_result(self):
        result_window = Tk()
        result_window.title("Result")

        headers = ["Year", "Month", "Date", "Time", "Name", "Price"]
        widths = [6, 5, 6, 5, 20, 7]

        for col, (header, width) in enumerate(zip(headers, widths)):
            Label(result_window, text=header, font=("Courier New", 10, "bold"), width=width, bg="lightblue").grid(row=0, column=col, sticky="nsew")

        for row_idx, row in enumerate(self.data, start=2):
            row_color = "white" if row_idx % 2 == 0 else "lightblue"
            for col_idx, (value, width) in enumerate(zip(row, widths)):
                if isinstance(value, float):
                    value = f"{value:.2f}"
                Label(result_window, text=value, font=("Courier New", 10), width=width, bg=row_color).grid(row=row_idx, column=col_idx, sticky="nsew")

        for col in range(len(headers)):
            result_window.grid_columnconfigure(col, weight=1)

        result_window.mainloop()

    def search(self):
        self.data = database.getAllData()
        if self.yearBox.current() >= 0:
            year = int(self.yearBox.get())
            month = int(self.monthBox.get().strip())
            if not (1 <= month <= 12):
                self.error_window()
                return
            date = int(self.dateBox.get().strip()) if self.dateBox.get().strip() != "" else None
            if (date==""):
                self.search_date(year, month, date)
            else:
                self.search_month(year, month)

        if self.tagBox.current() >= 0:
            tag = self.tagBox.get()
            self.search_tag(tag)

        name = self.itemBox.get(1.0, 'end-1c').strip()
        if name:
            self.search_item(name)

        min_val = float(self.minBox.get().strip()) if self.minBox.get().strip() != "" else None
        max_val = float(self.maxBox.get().strip()) if self.maxBox.get().strip() != "" else None
        if min_val is not None:
            if max_val is not None:
                self.search_range(min_val, max_val)  # Search with both min and max
            else:
                self.search_amount(min_val)  # Search with min only

        self.show_result()
        
    def error_window(self):
        error_window = Tk()
        error_window.title("Error")
        Label(error_window, text="Input invalid! Please check your input!").pack(padx=10, pady=5)
        error_window.mainloop()

    def init_ui(self):
        window = Tk()
        window.title("Search")

        Label(window, text="Date:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        Label(window, text="Tag:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        Label(window, text="Item:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        Label(window, text="Price:").grid(row=5, column=0, padx=10, pady=5, sticky="w")

        Label(window, text="Year:").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        Label(window, text="Month:").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        Label(window, text="Date:").grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.yearBox = ttk.Combobox(window, values=self.get_years(), width=5)
        self.yearBox.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.monthBox = Entry(window, width=3)
        self.monthBox.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        self.dateBox = Entry(window, width=3)
        self.dateBox.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        self.tagBox = ttk.Combobox(window, values=self.tag, width=8)
        self.tagBox.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        self.itemBox = Text(window, height=1, width=21)
        self.itemBox.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky="w")

        self.minBox = Entry(window, width=8)
        self.minBox.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        Label(window, text="~").grid(row=5, column=2, padx=1, pady=2, sticky="w")
        self.maxBox = Entry(window, width=8)
        self.maxBox.grid(row=5, column=2, padx=10, pady=5, sticky="e")

        btn = Button(window, text='Search', command=self.search)
        btn.grid(row=6, column=2, padx=10, pady=5, sticky="e")

        window.mainloop()

app = SearchWindow()
