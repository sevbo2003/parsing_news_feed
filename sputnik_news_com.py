import requests
import bs4 as BeautifulSoup
import datetime
from typing import List


def collext_new_links(last_date) -> List[str]:
    has_next_page = True
    links = []
    last_date_in_datatime = datetime.datetime.strptime(last_date, '%d-%m-%Y:%H:%M')
    months = {
        'Январ': '01',
        'Феврал': '02',
        'Март': '03',
        'Апрел': '04',
        'Май': '05',
        'Июн': '06',
        'Июь': '07',
        'Август': '08',
        'Сентябр': '09',
        'Октябр': '10',
        'Ноябр': '11',
        'Декабр': '12'
    }

    for i in range(1, 2700):
        req = requests.get(f'https://sputniknews-uz.com/archive/?page={i}')
        if has_next_page == False:
            has_next_page = True
            break
        if req.status_code == 200:
            soup = BeautifulSoup.BeautifulSoup(req.text, 'html.parser')
            articles = soup.find_all('div', class_='list__item')
            for article in articles:
                link = article.find('a').get('href')
                try:
                    date = article.find('span', class_='date').text
                    date = date.split(' ')
                    if len(date) == 1:
                        time = date[0]
                        today = datetime.datetime.now()
                        date = today.strftime('%d-%m-%Y') + ' ' + time
                    elif len(date) == 2:
                        time = date[1]
                        today = datetime.datetime.now() - datetime.timedelta(days=1)
                        date = today.strftime('%d-%m-%Y') + ' ' + time
                    elif len(date) == 3:
                        day = date[0]
                        month = months[date[1].replace(',', '')]
                        year = datetime.datetime.now().strftime('%Y')
                        time = date[2]
                        date = day + '-' + month + '-' + year + ' ' + time
                        date = datetime.datetime.strftime(date, '%d-%m-%Y %H:%M')
                    else:
                        day = date[0]
                        month = months[date[1].replace(',', '')]
                        year = date[2][:-1]
                        time = date[3]
                        date = day + '-' + month + '-' + year + ' ' + time
                        date = datetime.datetime.strftime(date, '%d-%m-%Y %H:%M')     
                    date_in_datatime = datetime.datetime.strptime(date, '%d-%m-%Y %H:%M')
                    if date_in_datatime > last_date_in_datatime:
                        links.append(link)
                    else:
                        has_next_page = False
                        break
                except:
                    pass     
                
    print(len(links))
    return links


if __name__ == '__main__':
    print(collext_new_links('26-12-2022:14:49'))