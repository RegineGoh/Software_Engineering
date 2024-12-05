# 檔案名稱: database.py

class Database:
    def __init__(self):
        # 儲存資料的 list
        self.data_list = []  # 儲存所有 insertData 的資料
        self.tag_list = []   # 儲存所有 insertTag 的資料
        self.data_counter = 1  # 用來生成唯一的 Data_No

    def insertData(self, Year, Month, Date, Time, Name, Price):
        if not (isinstance(Year, int) and isinstance(Month, int) and isinstance(Date, int) and isinstance(Time, int) and isinstance(Price, int)):
            return 0
        if not (1 <= Month <= 12 and 1 <= Date <= 31 and 0 <= Time <= 2359):
            return 0
        if not (isinstance(Name, str) and 1 <= len(Name) <= 20 and Name.isalnum()):
            return 0

        data_no = self.data_counter
        self.data_list.append({
            "Data_No": data_no,
            "Year": Year,
            "Month": Month,
            "Date": Date,
            "Time": Time,
            "Name": Name,
            "Price": Price
        })
        self.data_counter += 1
        return data_no

    def insertTag(self, Data_No, Tag):
        if not (isinstance(Data_No, int) and isinstance(Tag, str) and 1 <= len(Tag) <= 20):
            return 0
        if not any(data["Data_No"] == Data_No for data in self.data_list):
            return 0
        # 新增前檢查是否已有該標籤
        if any(tag["Data_No"] == Data_No and tag["Tag"] == Tag for tag in self.tag_list):
            return 0  # 標籤已存在於該資料中
        self.tag_list.append({"Data_No": Data_No, "Tag": Tag})
        return 1

    def getAllData(self):
        return [
            (data["Year"], data["Month"], data["Date"], data["Time"], data["Name"], data["Price"])
            for data in self.data_list
        ]

    def getAllTag(self, Tag):
        return [
            tag["Data_No"] for tag in self.tag_list if tag["Tag"] == Tag
        ]

    def getTagsByDataNo(self, Data_No):
        if not isinstance(Data_No, int):
            return []
        return [
            tag["Tag"] for tag in self.tag_list if tag["Data_No"] == Data_No
        ]

    def tagExists(self, Data_No, Tag):
        """檢查特定資料編號下是否已有該標籤"""
        return any(tag["Data_No"] == Data_No and tag["Tag"] == Tag for tag in self.tag_list)

    def findSimilarTags(self, Tag):
        """檢查是否有現有的標籤與輸入的標籤相似（使用簡單的相似判斷）"""
        similar_tags = []
        for existing_tag in {tag["Tag"] for tag in self.tag_list}:
            if self._isSimilar(Tag, existing_tag):
                similar_tags.append(existing_tag)
        return similar_tags

    def _isSimilar(self, tag1, tag2):
        """簡單相似判斷：忽略大小寫，判斷是否一方包含另一方"""
        tag1_lower = tag1.lower()
        tag2_lower = tag2.lower()
        return tag1_lower in tag2_lower or tag2_lower in tag1_lower
    
    def getTagName(self):
        tag=set(tag["Tag"] for tag in self.tag_list)
        return list(tag)

