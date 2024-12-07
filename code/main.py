import subprocess
from tkinter import *
from tkinter import messagebox


class Homepage:
    def __init__(self):
        self.init_ui()

    def init_ui(self):
        # 主視窗
        self.window = Tk()
        self.window.title("Homepage")
        self.window.geometry("400x300")

        # 標題
        Label(self.window, text="Welcome to the Homepage", font=("Arial", 16)).pack(pady=20)

        # 按鈕區域
        button_frame = Frame(self.window)
        button_frame.pack(pady=20)

        # 按鈕
        Button(button_frame, text="Input Data", command=self.open_input_data).grid(row=0, column=0, padx=10, pady=10)
        Button(button_frame, text="Search", command=self.open_search).grid(row=0, column=1, padx=10, pady=10)
        Button(button_frame, text="Statistic", command=self.open_statistics).grid(row=0, column=2, padx=10, pady=10)

        # 主循環
        self.window.mainloop()

    # 點擊按鈕後執行其他 Python 檔案
    def open_input_data(self):
        subprocess.Popen(["python", "inputData.py"])  # 請確保檔案名稱正確且與此檔案同目錄

    def open_search(self):
        subprocess.Popen(["python", "search.py"])

    def open_statistics(self):
        subprocess.Popen(["python", "statistic.py"])


# 啟動應用程式
if __name__ == "__main__":
    app = Homepage()
