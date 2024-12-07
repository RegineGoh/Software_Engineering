# 檔案名稱: database.py

import csv
import os

class Database:
    def __init__(self):
        self.data_file = "data.csv"
        self.tag_file = "tags.csv"
        self.data_counter = self._get_next_data_no()

    def _get_next_data_no(self):
        """從資料檔案取得下一個資料編號"""
        if not os.path.exists(self.data_file):
            return 1
        with open(self.data_file, "r", newline="") as file:
            reader = csv.DictReader(file)
            data = list(reader)
            return int(data[-1]["Data_No"]) + 1 if data else 1

    def insertData(self, Year, Month, Date, Time, Name, Price):
        if not (isinstance(Year, int) and isinstance(Month, int) and isinstance(Date, int) and 
                isinstance(Time, int) and isinstance(Price, int)):
            return 0
        if not (1 <= Month <= 12 and 1 <= Date <= 31 and 0 <= Time <= 2359):
            return 0
        if not (isinstance(Name, str) and 1 <= len(Name) <= 20 and Name.isalnum()):
            return 0

        data_no = self.data_counter

        # 寫入資料檔案
        with open(self.data_file, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Data_No", "Year", "Month", "Date", "Time", "Name", "Price"])
            if os.path.getsize(self.data_file) == 0:
                writer.writeheader()
            writer.writerow({
                "Data_No": data_no, "Year": Year, "Month": Month, 
                "Date": Date, "Time": Time, "Name": Name, "Price": Price
            })

        self.data_counter += 1
        return data_no

    def insertTag(self, Data_No, Tag):
        if not (isinstance(Data_No, int) and isinstance(Tag, str) and 1 <= len(Tag) <= 20):
            return 0

        if not self._data_exists(Data_No):
            return 0

        if self.tagExists(Data_No, Tag):
            return 0  # 標籤已存在

        with open(self.tag_file, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Data_No", "Tag"])
            if os.path.getsize(self.tag_file) == 0:
                writer.writeheader()
            writer.writerow({"Data_No": Data_No, "Tag": Tag})
        return 1

    def getAllData(self):
        if not os.path.exists(self.data_file):
            return []
        with open(self.data_file, "r", newline="") as file:
            reader = csv.DictReader(file)
            return [
                (int(row["Year"]), int(row["Month"]), int(row["Date"]), 
                 int(row["Time"]), row["Name"], int(row["Price"]))
                for row in reader
            ]

    def getAllTag(self, Tag):
        if not os.path.exists(self.tag_file):
            return []
        with open(self.tag_file, "r", newline="") as file:
            reader = csv.DictReader(file)
            return [
                int(row["Data_No"]) for row in reader if row["Tag"] == Tag
            ]

    def getTagsByDataNo(self, Data_No):
        if not os.path.exists(self.tag_file) or not isinstance(Data_No, int):
            return []
        with open(self.tag_file, "r", newline="") as file:
            reader = csv.DictReader(file)
            return [
                row["Tag"] for row in reader if int(row["Data_No"]) == Data_No
            ]

    def tagExists(self, Data_No, Tag):
        if not os.path.exists(self.tag_file):
            return False
        with open(self.tag_file, "r", newline="") as file:
            reader = csv.DictReader(file)
            return any(int(row["Data_No"]) == Data_No and row["Tag"] == Tag for row in reader)

    def findSimilarTags(self, Tag):
        if not os.path.exists(self.tag_file):
            return []
        similar_tags = set()
        with open(self.tag_file, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_tag = row["Tag"]
                if self._isSimilar(Tag, existing_tag):
                    similar_tags.add(existing_tag)
        return list(similar_tags)

    def _isSimilar(self, tag1, tag2):
        """簡單相似判斷：忽略大小寫，判斷是否一方包含另一方"""
        tag1_lower = tag1.lower()
        tag2_lower = tag2.lower()
        return tag1_lower in tag2_lower or tag2_lower in tag1_lower

    def getTagName(self):
        if not os.path.exists(self.tag_file):
            return []
        with open(self.tag_file, "r", newline="") as file:
            reader = csv.DictReader(file)
            tags = {row["Tag"] for row in reader}
        return list(tags)

    def getTagData(self, Data_No):
        if not os.path.exists(self.data_file):
            return []
        with open(self.data_file, "r", newline="") as file:
            reader = csv.DictReader(file)
            return [
                (int(row["Year"]), int(row["Month"]), int(row["Date"]), 
                 int(row["Time"]), row["Name"], int(row["Price"]))
                for row in reader if int(row["Data_No"]) in Data_No
            ]

    def _data_exists(self, Data_No):
        """檢查 Data_No 是否存在於資料檔案中"""
        if not os.path.exists(self.data_file):
            return False
        with open(self.data_file, "r", newline="") as file:
            reader = csv.DictReader(file)
            return any(int(row["Data_No"]) == Data_No for row in reader)
