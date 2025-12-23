import os
import csv

#유저데이터 불러오기
def load_user_data(filename="economy_data.csv"):
    usernames, idA, moneyA, levelA, timeA, timeB, timeC = [], [], [], [], [], [], [] #A:시급, B:출석, C:분급
    if not os.path.exists(filename):
        with open(filename, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["username", "id", "money", "level", "hourly_time", "attendance_time", "minutely_time"])
    with open(filename, "r", newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row:
                continue
            usernames.append(row[0])
            idA.append(row[1])
            moneyA.append(int(row[2]))
            levelA.append(int(row[3]))
            timeA.append(row[4])
            timeB.append(row[5])
            timeC.append(row[6])
    return usernames, idA, moneyA, levelA, timeA, timeB, timeC

#유저데이터 저장
def save_user_data(usernames, idA, moneyA, levelA, timeA, timeB, timeC, filename="economy_data.csv"):
    with open(filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["username", "id", "money", "level", "hourly_time", "attendance_time", "minutely_time"])
        for i in range(len(idA)):
            writer.writerow([usernames[i], idA[i], moneyA[i], levelA[i], timeA[i], timeB[i], timeC[i]])
