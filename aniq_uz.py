import requests
import bs4 as BeautifulSoup
import datetime
from typing import List

def collext_new_links(last_date) -> List[str]:
    has_next_page = True
    links = []
    last_date_in_datatime = datetime.datetime.strptime(last_date, '%d-%m-%Y:%H:%M')
    for i in range(1, 11000):
        if has_next_page == False:
            has_next_page = True
            break
        req = requests.get(f'https://aniq.uz/uz/yangiliklar?page={i}')
        if req.status_code == 200:
            soup = BeautifulSoup.BeautifulSoup(req.text, 'html.parser')
            articles = soup.find_all('div', class_='news-list_item')
            for article in articles:
                date = article.find('div', class_='news-item_footer').text.split()
                link = article.find('a').get('href')
                if 'Bugun' in date:
                    time = date[2][:-1]
                    date = datetime.datetime.now().strftime('%d-%m-%Y')
                    date = date + ' ' + time
                    date_in_datatime = datetime.datetime.strptime(date, '%d-%m-%Y %H:%M')
                else:
                    day = date[2][:-1]
                    time = date[1]
                    date = day + ' ' + time
                    date_in_datatime = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M')
                if date_in_datatime > last_date_in_datatime:
                    links.append(link)
                else:
                    has_next_page = False
                    break
    return links

if __name__ == '__main__':
    print(collext_new_links('25-12-2022:23:05'))
