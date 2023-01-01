import requests
import bs4 as BeautifulSoup
import datetime
from typing import List

def collext_new_links(last_date) -> List[str]:
    has_next_page = True
    links = []
    last_date_in_datatime = datetime.datetime.strptime(last_date, '%d-%m-%Y:%H:%M')
    for i in range(1, 3500):
        if has_next_page == False:
            has_next_page = True
            break
        req = requests.get(f'https://goal24.uz/lastnews/page/{i}/')
        if req.status_code == 200:
            soup = BeautifulSoup.BeautifulSoup(req.text, 'html.parser')
            articles = soup.find_all('div', class_='shortstory2')
            for article in articles:
                date = article.find('div', class_='sdate').text.split('|')[0].strip()
                link = article.find('a').get('href')
                if 'Bugun' in date or 'Kecha' in date:
                    time = date.split(',')[1]
                    if 'Bugun' in date:
                        date = datetime.datetime.now().strftime('%d-%m-%Y')
                    else:
                        date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%d-%m-%Y')
                    date = date + ' ' + time
                else:
                    day = date.split(',')[0]
                    time = date.split(',')[1]
                    date = day + ' ' + time
                date_in_datatime = datetime.datetime.strptime(date, '%d-%m-%Y %H:%M')
                if date_in_datatime > last_date_in_datatime:
                    links.append(link)
                else:
                    has_next_page = False
                    break
    return links

if __name__ == '__main__':
    print(collext_new_links('26-12-2022:13:15'))
