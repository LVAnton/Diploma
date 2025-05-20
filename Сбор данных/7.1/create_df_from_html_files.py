import re
import pandas as pd
from bs4 import BeautifulSoup
array = [] #Массив, в который планируется записать всю информацию об участниках

def translate_time(time):
    if ':' in time:
        hours = int(time[:2])
        minutes = int(time[3:])
        res = hours * 60 + minutes
        return res
    else:
        res = 0
        if 'д' in time:
            for i in range(len(time) - 1):
                if time[i + 1] == 'д':
                    days = int(time[i])
            res += days * 24 * 60
        if 'ч' in time:
            for i in range(len(time) - 1):
                if time[i + 1] == 'ч':
                    to_test = time[i - 1] + time[i]
                    try:
                        to_test = int(to_test)
                    except:
                        to_test = time[i]
                        to_test = int(to_test)
            hours = to_test
            res += hours * 60
        return res

def work_with_1_string(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    data = {}
    place_td = soup.find('td', class_='table__cell_role_place')
    data['rate'] = place_td.text.strip() if place_td else None
    participant_td = soup.find('td', class_='table__cell_role_participant')
    participant_name = participant_td.find('div', class_='table__data_type_ptp')['title'] if participant_td else None
    data['id'] = participant_name
    result_tds = soup.find_all('td', class_='table__cell_role_result')
    bonuses = []
    times = []
    k = 0
    for result_td in result_tds:
        bonus_div = result_td.find('div', class_='table__data_mood_pos')
        if bonus_div == None:
            bonus_div = result_td.find('div', class_='table__data_mood_neg')
        time_div = result_td.find('div', class_='table__data_type_time')
        bonus = bonus_div.text.strip() if bonus_div else None
        time_taken = time_div.text.strip() if time_div else None
        task = chr(ord('A') + k)

        if bonus != None:
            data[task] = bonus[0]
            if len(bonus) == 1:
                data[task + '_errors'] = 0
            else:
                data[task + '_errors'] = int(bonus[1:])
            data[task + '_time'] = translate_time(time_taken)
        else:
            data[task] = None
            data[task + '_errors'] = None
            data[task + '_time'] = None
        k += 1
    meta_tds = soup.find_all('td', class_='table__cell_role_meta')
    data['ready_num'] = meta_tds[0].text.strip() if len(meta_tds) > 0 else None
    data['penalty'] = meta_tds[1].text.strip() if len(meta_tds) > 1 else None
    if data['rate'] != None and data['id'] != 'AntonLapin24':
        return data

def add_people(html_content):
    #поиск нужного тега, с таблицей
    table = re.search(r'<table class="table table_role_standings.*?>(.*?)</table>', html_content, re.DOTALL)
    table_html = table.group(1)
    rows = re.findall(r'<tr class="table__row.*?>(.*?)</tr>', table_html, re.DOTALL)

    for i in range(len(rows)):
        one_person = work_with_1_string(rows[i])
        if one_person != None:
            array.append(one_person)

for i in range(43): # было 43
    name = str(i+1) + " лист.txt"
    # Открываем нужный файл
    with open(name, 'r', encoding='utf-8') as f:
        #Считываем его содержание
        html_content = f.read()
        #Дополняем таблицу участников из файла
        add_people(html_content)

df = pd.DataFrame(array)
print(df)

#Как правильно записать время?
df.to_csv('1.csv', index=False)