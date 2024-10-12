##office.kis
import requests, os
from dotenv import load_dotenv

load_dotenv()
session = requests.Session()

LOGIN_HEADERS = {
    'size' : '1920',
    'u' : os.environ.get('OFFICEKIS_USER'),
    'p' : os.environ.get('OFFICEKIS_PASSWD'),
    'login' : '> Login',
    'Newsletter' : '' 
}

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,hu-HU;q=0.8,hu;q=0.7,ja-JP;q=0.6,ja;q=0.5,de-DE;q=0.4,de;q=0.3',
        'Connection': 'keep-alive',
        'Referer': 'https://office.kis.uni-kl.de/views/pia/pia.asp',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }


def login():
    global LOGIN_HEADERS
    global headers
    payload = {
        'size': '1920',
        'u': os.environ.get('OFFICEKIS_USER'),
        'p': os.environ.get('OFFICEKIS_PASSWD'),
        'login': '> Login',
        'Newsletter': ''
    }
    response = session.post('https://office.kis.uni-kl.de/default.asp', data=payload, headers=headers, allow_redirects=True)

    print(response.text)  # Zeigt die HTML-Antwort des Servers an
    return response

def get_timetable(cookies):
    global headers

    # Cookies müssen korrekt übernommen werden
    session.cookies.update(cookies)

    return session.get('https://office.kis.uni-kl.de/views/calendar/timeTable.asp', headers=headers, cookies=cookies)


def main():
    login_response = login()
    cookies = login_response.cookies
    print(login_response.url)

    #print(login_response.status_code, type(login_response.status_code))
    if login_response.status_code == 200:
        timetable_asp = get_timetable(cookies=cookies)
        #print(timetable_asp.text)
        f = open('test.html', 'w')
        f.write(timetable_asp.text)
        f.close()

main()