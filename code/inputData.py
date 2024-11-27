#目前可輸入品項 
#防呆模式還未完善
#無GUI，純文字介面

# 功能提示文字
print("請輸入消費品項的年分、月份、日期、時間、品項名稱及消費金額")
print("按 Enter 確認每項輸入，若要取消動作可直接結束程式")

# 功能函數
def checkYear(year):
    return isinstance(year, int) and 1000 <= year <= 9999

def checkMonth(month):
    return isinstance(month, int) and 1 <= month <= 12

def checkDate(year, month, day):
    try:
        from datetime import datetime
        datetime(year, month, day)
        return True
    except ValueError:
        return False

def checkTime(time):
    return isinstance(time, int) and 0 <= time <= 2359

def checkName(name):
    return isinstance(name, str) and 1 <= len(name) <= 20 and name.isalnum()

def checkPrice(price):
    return isinstance(price, int) and price > 0

# 開始輸入資料
try:
    year = int(input("年分: "))
    if not checkYear(year):
        raise ValueError("年份輸入有誤，請輸入有效的四位數年份。")

    month = int(input("月份: "))
    if not checkMonth(month):
        raise ValueError("月份輸入有誤，請輸入 1 到 12 的值。")

    date = int(input("日期: "))
    if not checkDate(year, month, date):
        raise ValueError("日期輸入有誤，請確認日期是否合法。")

    time = int(input("時間 (格式: 0000 - 2359): "))
    if not checkTime(time):
        raise ValueError("時間輸入有誤，請確認格式為 0000 到 2359。")

    while True:
        # 輸入單一品項
        name = input("品項名稱: ")
        if not checkName(name):
            raise ValueError("名稱輸入有誤，請輸入長度為 1~20 的字母或數字。")

        price = int(input("消費金額: "))
        if not checkPrice(price):
            raise ValueError("金額輸入有誤，請輸入大於 0 的正整數。")

        # 新增資料到資料庫
        # data_no = db.insertData(year, month, date, time, name, price)
        data_no = 1  # 假設資料成功新增並回傳資料編號 1
        if data_no == 0:
            print("資料新增失敗，請重新輸入資料。")
        else:
            print(f"資料新增成功，資料編號為 {data_no}。")
            print("請選擇標籤：")
            # tags = db.getTagsByDataNo(data_no)  # 列出現有標籤
            tags = ["食物", "娛樂", "交通"]  # 假設標籤範例
            if tags:
                print("可用標籤:", tags)
            tag = input("標籤名稱: ")
            # if db.insertTag(data_no, tag) == 1:
            if tag:  # 假設標籤成功新增
                print("標籤新增成功。")
            else:
                print("標籤新增失敗，請重新選擇。")

        # 確認是否繼續輸入
        cont = input("是否繼續輸入下一個品項？(y/n): ").lower()
        if cont != 'y':
            print("輸入完成，感謝使用！")
            break

except ValueError as e:
    print(f"輸入錯誤: {e}")
except Exception as e:
    print(f"發生未知錯誤: {e}")
