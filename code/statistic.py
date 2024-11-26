from datetime import date
from collections import Counter
import matplotlib.pyplot as plt

def getStatistic(db, YearA, MonthA, DateA, YearB, MonthB, DateB, detail=False, chart=False):
    # 獲取所有資料
    all_data = [
        {"Year": data[0], "Month": data[1], "Date": data[2], "Time": data[3], "Name": data[4], "Price": data[5], "Data_No": index + 1}
        for index, data in enumerate(db.getAllData())
    ]

    # 驗證是否有資料
    if not all_data:
        print("無消費資料。")
        return

    # 預設日期範圍
    default_start = min(all_data, key=lambda x: (x["Year"], x["Month"], x["Date"]))
    default_end = max(all_data, key=lambda x: (x["Year"], x["Month"], x["Date"]))

    # 驗證日期 A 和 B
    try:
        start_date = date(YearA, MonthA, DateA)
    except ValueError:
        print(f"日期 A ({YearA}-{MonthA}-{DateA}) 無效，使用最早日期 {default_start}.")
        start_date = date(default_start["Year"], default_start["Month"], default_start["Date"])

    try:
        end_date = date(YearB, MonthB, DateB)
    except ValueError:
        print(f"日期 B ({YearB}-{MonthB}-{DateB}) 無效，使用最晚日期 {default_end}.")
        end_date = date(default_end["Year"], default_end["Month"], default_end["Date"])

    # 確保日期範圍有效
    if start_date > end_date:
        print("日期範圍錯誤，交換 A 與 B 的值。")
        start_date, end_date = end_date, start_date

    # 篩選符合範圍的資料
    filtered_data = [
        data for data in all_data
        if start_date <= date(data["Year"], data["Month"], data["Date"]) <= end_date
    ]

    if not filtered_data:
        print("篩選後無消費資料。")
        return

    # 計算總消費
    total_expense = sum(data["Price"] for data in filtered_data)

    # 計算標籤佔比
    tag_counts = Counter(
        tag
        for data in filtered_data
        for tag in db.getTagsByDataNo(data["Data_No"])
    )

    # 輸出統計資訊
    print(f"日期範圍：{start_date} ~ {end_date}")
    print(f"總消費：{total_expense} 元")
    print("標籤佔比：")
    for tag, count in tag_counts.items():
        print(f"  {tag}: {count} 筆 ({(count / len(filtered_data) * 100):.2f}%)")

    # 輸出消費細項
    if detail:
        print("\n消費細項：")
        for data in filtered_data:
            print(f"  日期: {data['Year']}-{data['Month']:02d}-{data['Date']:02d}, "
                  f"時間: {data['Time']:04d}, 名稱: {data['Name']}, 價格: {data['Price']} 元")

    # 輸出圓餅圖
    if chart:
        labels = list(tag_counts.keys())
        sizes = list(tag_counts.values())
        colors = plt.cm.Paired(range(len(labels)))

        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        plt.title("Statistic")
        plt.axis('equal')  # 圓形比例
        plt.show()




""""
測試 statistic: 

from database import Database
from statistic import getStatistic

if __name__ == "__main__":
    from database import Database
    db = Database()
    db.insertData(2022, 11, 1, 1200, "Lunch", 100)
    db.insertTag(1, "Food")
    db.insertData(2023, 11, 2, 1400, "Taxi", 200)
    db.insertTag(2, "Transport")
    db.insertData(2023, 11, 3, 1800, "Dinner", 300)
    db.insertTag(3, "Food")

    print(db.getAllTag("Food"))
    getStatistic(db, 2023, 11, 1, 2023, 11, 4, detail=True, chart=True)
"""