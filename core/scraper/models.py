from django.db import models
import requests
import json
from urllib.parse import quote
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from lxml import html
import re
from tqdm import tqdm
import os
from django.conf import settings
import threading
import time
from apscheduler.schedulers.background import BackgroundScheduler
from decouple import config
from solo.models import SingletonModel
file_path = os.path.join(settings.BASE_DIR, 'scraper/scrape_config.json')

with open(file_path,"r") as f:
    scrape_config = json.loads(f.read())

# Create your models here.

class OjccCase(models.Model):
    case_id = models.TextField(null=True,blank=True,verbose_name="CaseID")
    case_yr = models.TextField(null=True,blank=True,verbose_name="caseYr")
    case_num = models.TextField(null=True,blank=True,verbose_name="caseNum")
    ojcc_case_number = models.TextField(null=True,blank=True,verbose_name="OJCC Case Number")
    judge = models.TextField(null=True,blank=True,verbose_name="Judge")
    mediator = models.TextField(null=True,blank=True,verbose_name="Mediator")
    carrier = models.TextField(null=True,blank=True,verbose_name="Carrier")
    accident_date = models.TextField(null=True,blank=True,verbose_name="Accident Date")
    date_assigned = models.TextField(null=True,blank=True,verbose_name="Date Assigned")
    district = models.TextField(null=True,blank=True,verbose_name="District")
    county = models.TextField(null=True,blank=True,verbose_name="County")
    counsel_for_claimant = models.TextField(null=True,blank=True,verbose_name="Counsel For Claimant")
    counsel_for_employer = models.TextField(null=True,blank=True,verbose_name="Counsel For Employer/Carrier")
    case_status = models.TextField(null=True,blank=True,verbose_name="case status")
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "OJCC Case"
        verbose_name_plural = "OJCC Cases"

    def __str__(self) :
        return "OJCC Case Number " + self.ojcc_case_number


class Schedule(models.Model):
    ojcc_case = models.ForeignKey(OjccCase,on_delete=models.CASCADE)
    hearing_type = models.TextField(null=True,blank=True,verbose_name="Hearing Type")
    event_date = models.TextField(null=True,blank=True,verbose_name="Event Date")
    start_time = models.TextField(null=True,blank=True,verbose_name="Start Time*")
    current_status = models.TextField(null=True,blank=True,verbose_name="Current Status")
    _with = models.TextField(null=True,blank=True,verbose_name="With")
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedule"
    def __str__(self):
        return ""


class Docket(models.Model):
    ojcc_case = models.ForeignKey(OjccCase,on_delete=models.CASCADE)
    date = models.TextField(null=True,blank=True,verbose_name="Date")
    proceeding = models.TextField(null=True,blank=True,verbose_name="Proceedings")
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Docket"
        verbose_name_plural = "Docket"
    def __str__(self):
        return ""



class StartScraper(SingletonModel):

    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    current_page = models.IntegerField(default=1,null=True , blank = True)
    status = models.CharField(max_length=255,default="Press Save Button To Start Scraping")
    Progress_bar = models.TextField(null=True,blank=True)
    start_job = models.BooleanField(default=True)
    def save(self, *args,**kwargs):
        if not self.pk:
            super(StartScraper, self).save(*args,**kwargs)
        elif self.start_job:
            threading.Thread(target=scrape_ojcc).start()
            self.status = "Scraper Is Now Running!"
            self.current_page = 1
            self.start_job = False
            super(StartScraper, self).save(*args,**kwargs)


try:scrape_starter,created = StartScraper.objects.get_or_create()
except:pass


def scrape_ojcc():
    print("------------SCRAPER HAS STARTED-----------")
    global scrape_config
    global scrape_starter
    
    # First
    url = "https://www.jcc.state.fl.us/JCC/searchJCC/searchCases.asp"

    headers = {
    'authority': 'www.jcc.state.fl.us',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    response = requests.request("GET", url, headers=headers)
    # Second
    headers = {
    'authority': 'www.jcc.state.fl.us',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.jcc.state.fl.us',
    'referer': 'https://www.jcc.state.fl.us/JCC/searchJCC/searchCases.asp',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    
    headers["cookie"] = response.headers['Set-Cookie']

    url = "https://www.jcc.state.fl.us/JCC/searchJCC/searchAction.asp?sT=byOther"

    if scrape_config["CaseStatus"] == "All":
        CaseStatus = 0
    elif scrape_config["CaseStatus"] == "Active":
        CaseStatus = 1
    elif scrape_config["CaseStatus"] == "Inactive":
        CaseStatus = 2
        
    payload = f'CaseStatus={CaseStatus}&DateOpenStart={quote(scrape_config["DateOpenStart"],safe="")}&DateOpenEnd={quote(scrape_config["DateOpenEnd"],safe="")}&AccidentDate={scrape_config["AccidentDate"]}&fname={scrape_config["fname"]}&lname={scrape_config["lname"]}&County={scrape_config["County"]}&SSN={scrape_config["SSN"]}&employer={scrape_config["employer"]}&carrier={scrape_config["carrier"]}&JCC={scrape_config["JCC"]}&submit=%20Search%20'

    response = requests.request("GET", url, headers=headers, data=payload , allow_redirects=False)
    # Third
    headers["cookie"] = response.headers['Set-Cookie']

    target_url = urljoin(response.url, response.headers['location'])

    response = requests.request("GET", target_url, headers=headers)
    soup = BeautifulSoup(response.text,"html.parser")
    root = html.fromstring(str(soup))
    last_href = root.xpath("//div[@align='center']/a[contains(text(),'Last')]/@href")[0]
    number_of_pages = int(re.findall(r"\d+",last_href)[0])
    print("number of pages: "+str(number_of_pages))
    Progress_bar = tqdm(total = number_of_pages)

    for page in tqdm(range(1,number_of_pages)) :
        scrape_starter.current_page = page
        scrape_starter.start_job = False
        Progress_bar.n = page
        scrape_starter.Progress_bar = Progress_bar.__str__()
        scrape_starter.save()
        scrape_page(target_url,page,headers)


def scrape_page(target_url,page,headers):
    print("current page: "+str(page))
    url = f"{target_url}?pc{page}"
    page_response = requests.request("GET", url, headers=headers)
    page_soup = BeautifulSoup(page_response.text,"html.parser")
    page_soup.select("div.grid_5.alignleft a[href]")
    case_elements = page_soup.select("div.grid_5.alignleft a[href]")
    for case_element in case_elements:
        element_url = urljoin(page_response.url, case_element.get("href"))
        case_response = requests.request("GET", element_url, headers=headers)
        case_soup = BeautifulSoup(case_response.text,"html.parser")
        case_dockets = case_soup.select("#docket tr.odd,tr.even")
        continue_case = True
        
        # Check settlements:
        for case_docket in case_dockets:
            if "Settlement Order" in case_docket.text:
                continue_case = False
        if continue_case:
            continue
        scrape_case(element_url,case_soup,case_element)


def scrape_case(element_url,case_soup,case_element):
    case_dockets = case_soup.select("#docket tr.odd,tr.even")
    ojcc_data = {}
    ojcc_data["case_id"] = re.findall(r"CaseID=(\d+)",element_url)[0]
    ojcc_object,o = OjccCase.objects.get_or_create(**ojcc_data)
    # create OjccCase objects
    for case_docket in case_dockets:
        # create Docket objects
        docket_data = {}
        try:docket_data["date"] = case_docket.select_one("td[width='15%']").text
        except:pass
        try:docket_data["proceeding"] = case_docket.select_one("td[width='75%']").text
        except:pass
        try:docket_data["ojcc_case"] = ojcc_object
        except:pass
        try:Docket.objects.get_or_create(**docket_data)
        except:pass

    case_schedules = case_soup.select("#schedule tr:has(td[align=center])")
    for case_schedule in case_schedules:
        # create Schedule objects
        schedule_attrs = case_schedule.select("td[align=center]")
        schedule_data = {}
        try:schedule_data["hearing_type"] = schedule_attrs[0].text                        
        except:pass
        try:schedule_data["event_date"] = schedule_attrs[1].text            
        except:pass
        try:schedule_data["start_time"] = schedule_attrs[2].text            
        except:pass
        try:schedule_data["current_status"] = schedule_attrs[3].text            
        except:pass
        try:schedule_data["_with"] = schedule_attrs[4].text
        except:pass
        try:schedule_data["ojcc_case"] = ojcc_object
        except:pass
        if schedule_data : Schedule.objects.get_or_create(**schedule_data)

    # OjccCase attributes
    try:ojcc_object.case_yr = re.findall(r"caseYr=(\d+)",element_url)[0]
    except:pass
    try:ojcc_object.case_num = re.findall(r"caseNum=(\d+)",element_url)[0]
    except:pass
    try:ojcc_object.ojcc_case_number = case_element.text.strip()
    except:pass
    try:ojcc_object.judge = case_soup.select_one("div.grid_2:contains('udge') + div.grid_6.nomargin").text.strip()
    except:pass
    try:ojcc_object.mediator = case_soup.select_one("div.grid_2:contains('ediator') + div.grid_6.nomargin").text.strip()
    except:pass
    try:ojcc_object.carrier = case_soup.select_one("div.grid_2:contains('arrier') + div.grid_6.nomargin").text.strip()
    except:pass
    try:ojcc_object.accident_date = case_soup.select_one("div.grid_2:contains('ccident') + div.grid_6.nomargin").text.strip()
    except:pass
    try:ojcc_object.date_assigned = case_soup.select_one("div.grid_2:contains('ssigned') + div.grid_6.nomargin").text.strip()
    except:pass
    try:ojcc_object.district = case_soup.select_one("div.grid_2:contains('istrict') + div.grid_6.nomargin").text.strip()
    except:pass
    try:ojcc_object.county = case_soup.select_one("div.grid_2:contains('ounty') + div.grid_6.nomargin").text.strip()
    except:pass
    ojcc_object.counsel_for_claimant = ''


    try:counsel_for_claimants = case_soup.select_one("#counsel table[align='center']:has(h4:contains('lainment'))").select('td')
    except:counsel_for_claimants =[]
    for claimant in counsel_for_claimants:
        ojcc_object.counsel_for_claimant += claimant.text.strip()

    ojcc_object.counsel_for_employer = ""

    try:counsel_for_employers = case_soup.select_one("#counsel table[align='center']:has(h4:contains('mployer'))").select('td:not(:has(h4))')
    except:counsel_for_employers=[]
    for employer in counsel_for_employers:
        ojcc_object.counsel_for_employer += employer.text.strip()
    ojcc_object.case_status = scrape_config["CaseStatus"]
    ojcc_object.save()

