import requests
import bs4 as BeautifulSoup
import datetime
from typing import List


def collext_new_links(last_date) -> List[str]:
    has_next_page = True
    links = []
    last_date_in_datatime = datetime.datetime.strptime(last_date, '%d-%m-%Y:%H:%M')
    months = {
        'Январь': '01',
        'Февраль': '02',
        'Март': '03',
        'Апрель': '04',
        'Май': '05',
        'Июнь': '06',
        'Июль': '07',
        'Август': '08',
        'Сентябрь': '09',
        'Октябрь': '10',
        'Ноябрь': '11',
        'Декабрь': '12'
    }

    for i in range(1, 2):
        req = requests.get(f'https://sports.uz/news/index?page={i}')
        if has_next_page == False:
            has_next_page = True
            break
        if req.status_code == 200:
            soup = BeautifulSoup.BeautifulSoup(req.text, 'html.parser')
            articles = soup.find('main', class_='main-content').find('div', class_='news-list').find_all('div', class_='item')
            for article in articles:
                link = 'https://sports.uz/news' + article.find('a').get('href')
                try:
                    i = article.find('div', class_='news-body').find('ul').find('li').text
                    date = i.split(' ')
                    if len(date) == 4:
                        day = date[1]
                        month = months[date[2].replace(',', '').capitalize()]
                        year = datetime.datetime.now().strftime('%Y')
                        time = date[3]
                        date = day + '-' + month + '-' + year + ' ' + time
                        date = datetime.datetime.strptime(date, '%d-%m-%Y %H:%M')
                    else:
                        day = date[1]
                        month = months[date[1].replace(',', '').capitalize()]
                        year = date[3][:-1]
                        time = date[4]
                        date = day + '-' + month + '-' + year + ' ' + time
                        date = datetime.datetime.strptime(date, '%d-%m-%Y %H:%M')
                    if date > last_date_in_datatime:
                        links.append(link)
                    else:
                        has_next_page = False
                        break
                except:
                    pass

    return links


if __name__ == '__main__':
    print(collext_new_links('26-12-2022:22:49'))