import re
from bs4 import BeautifulSoup
array = []
def work_with_1_string(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    data = {}
    # 1. Place
    place_td = soup.find('td', class_='table__cell_role_place')
    data['place'] = place_td.text.strip() if place_td else None
    # 2. Participant
    participant_td = soup.find('td', class_='table__cell_role_participant')
    participant_name = participant_td.find('div', class_='table__data_type_ptp')['title'] if participant_td else None
    data['participant_name'] = participant_name
    # 3. Results (bonuses and time)
    result_tds = soup.find_all('td', class_='table__cell_role_result')
    bonuses = []
    times = []
    for result_td in result_tds:
        bonus_div = result_td.find('div', class_='table__data_mood_pos')
        time_div = result_td.find('div', class_='table__data_type_time')
        bonus = bonus_div.text.strip() if bonus_div else None
        time_taken = time_div.text.strip() if time_div else None
        bonuses.append(bonus)
        times.append(time_taken)
    data['bonuses'] = bonuses
    data['times'] = times
    meta_tds = soup.find_all('td', class_='table__cell_role_meta')
    data['meta_1'] = meta_tds[0].text.strip() if len(meta_tds) > 0 else None
    data['meta_2'] = meta_tds[1].text.strip() if len(meta_tds) > 1 else None
    return data

def extract_standings(html_content):
    table = re.search(r'<table class="table table_role_standings.*?>(.*?)</table>', html_content, re.DOTALL)
    table_html = table.group(1)
    rows = re.findall(r'<tr class="table__row.*?>(.*?)</tr>', table_html, re.DOTALL)

    for i in range(len(rows)):
        one_person = work_with_1_string(rows[i])
        array.append(one_person)



for i in range(23):
    name = str(i+1) + " лист.txt"
    with open(name, 'r', encoding='utf-8') as f:
        html_content = f.read()
        participants_table = extract_standings(html_content)
for i in range(len(array)):
    print(array[i])