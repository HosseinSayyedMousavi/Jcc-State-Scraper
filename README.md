# Jcc-State-Scraper
scrape jcc state 

## 1. quick start

#### A. Run this command at BASE_DR 
```
docker compose up --build -d
```
it create 2 containers named "scraper" and "scraper_db" (a postgres database)

in scraper you have a django server that views and start desired scraper

#### B. Open this address:
```
http://localhost:9000/admin
```
login with following username and password:
```
username=admin
password=admin
```

#### C. Start scraper on Start scraper singletone model:

if you click on save button scraper will be start.

you can stream all scraped OjccCases with its Docket and Scheduler objects that connect to this with ForeignKey.

## 2. Scraper characteristics :


#### A. This scraper just use BeautifulSoup as a protocol method

#### B. You can start scraping from admin panel and in future it can develop to start and stop proccessing

#### C. All of cases can update on modelling of django and you can develop it to have an api service and ...

#### D. You can customize it by change scraper/scrape_config and .env file for another considerations

## 3. steps of scrape data

for scrape data without browser we must to operate like this in protocol methods. 
#### A. First request
At first request we use normal headers of a common browser like this:
'''
{
    # ...
    'authority': 'www.jcc.state.fl.us',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    # ...
    }
'''
this request gives you a cookie at first like this:
'''
'set-cooke':''
'''
#### B. Second request
when you click on search button a requests send with previous cookie and you must send it with your desired parameters.

after a moment your response is a 302 redirect with a new "set-cookie" parameter.

thats means your parameters is in mind of server by your new cookie

#### C. Third request
Now you can request to redirected url with that cookie gotten from previous step in circle and get all cases. 


That was a brief explanation from project  you can read codes for deeper information.

Thanks for your attention.
