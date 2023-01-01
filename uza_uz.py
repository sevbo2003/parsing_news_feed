import requests
import datetime
from typing import List


def collext_new_links(last_date) -> List[str]:
    has_next_page = True
    count = 0
    links = []
    last_date_in_datatime = datetime.datetime.strptime(last_date, '%d-%m-%Y:%H:%M')
    for i in range(1, 7777):
        if has_next_page == False:
            has_next_page = True
            break
        api = f'https://api.uza.uz/api/v1/posts?page={i}'
        req = requests.get(api)
        if req.status_code == 200:
            data = req.json()['data']
            for item in data:
                date = item['publish_time']
                link ='https://uza.uz/uz/posts/' + item['slug']
                date_in_datatime = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                if date_in_datatime > last_date_in_datatime:
                    links.append(link)
                    count += 1
                else:
                    has_next_page = False
                    break
    print(datetime.datetime.now())    
    return links


if __name__ == '__main__':
    print(collext_new_links('26-12-2022:11:50'))