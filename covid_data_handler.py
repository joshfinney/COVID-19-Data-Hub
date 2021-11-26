""" This module controls the functionality of the COVID hub web page """

from uk_covid19 import Cov19API
from flask import Flask, render_template, request
import csv
import json
import logging
import sched, time
from covid_news_handling import get_accepted_articles, news_api_request, delete_news
 
updated:bool = False
covid_news_data:list = []
 
list_of_updates:list = []
 
news_scheduler = sched.scheduler(time.time,time.sleep)
covid_data_scheduler = sched.scheduler(time.time, time.sleep)
 
form_data = {
   'Scheduled_data_updates' : str,
   'Update_label' : str,
   'Repeat_update' : bool,
   'Update_covid_data' : bool,
   'Update_news_article' : bool,
}
 
exeter_covid_data:dict = {}
nation_covid_data:dict = {}
 
""" Opens config.json file to import city name """
with open('config.json', 'r') as f:
   config = json.load(f)
  
   user_info = config["information"]
   city_name = user_info["city"]
 
""" Checks if form has been filled """
def get_updated():
   return updated
 
""" Converts given CSV file to a list """
def parse_csv_data(csv_filename):
   with open(csv_filename) as csv_file:
       csv_reader = csv.reader(csv_file, delimiter=',')
       list_of_rows = []
       for row in csv_reader:
           list_of_rows.append(row)
       return list_of_rows
 
""" Processes COVID data as a list into 3 values (number of cases in the past 7 days, hospital cases and total deaths) """
def process_covid_csv_data(covid_csv_data):
   last7days_cases:int = 0
   current_hospital_cases:int
   total_deaths:int
 
   for i in range(3,10):
       last7days_cases += int(covid_csv_data[i][6])
  
   current_hospital_cases = covid_csv_data[1][5]
   total_deaths = covid_csv_data[14][4]
 
   return int(last7days_cases), int(current_hospital_cases), int(total_deaths)
 
""" Returns updated COVID data when given a location and location type """
def covid_API_request(location = city_name,location_type = 'ltla'):
   filter_only = [
       'areaType=' + location_type,
       'areaName=' + location
       ]
   cases_and_deaths = {
       "areaName": "areaName",
       "date": "date",
       "cumDeaths28DaysByPublishDate": "cumDeaths28DaysByPublishDate",
       "hospitalCases": "hospitalCases",
       "newCasesBySpecimenDate": "newCasesBySpecimenDate",
       }
  
   api = Cov19API(filters=filter_only, structure=cases_and_deaths)
 
   return api.get_json()
 
""" Converts json data to values wanted by user """
def parse_json_data(data, starting_value):
   global exeter_covid_data
   global nation_covid_data
  
   covid_data_values = {
       '7DayCases' : 0,
       'HospitalCases' : 0,
       'DeathsTotal' : 0,
   }
   actual_data = data['data']
   for key in range(starting_value,starting_value+7):
       if actual_data[key]['newCasesBySpecimenDate']:
           covid_data_values['7DayCases'] += actual_data[key]['newCasesBySpecimenDate']
 
   covid_data_values['DeathsTotal'] = actual_data[0]['cumDeaths28DaysByPublishDate']
 
   covid_data_values['HospitalCases'] = actual_data[0]['hospitalCases']
 
   if actual_data[1]['areaName'] == city_name:
       exeter_covid_data = covid_data_values
   else:
       nation_covid_data = covid_data_values
 
   return covid_data_values
 
""" Converts hh:mm time format to seconds """
def hhmm_to_seconds( hhmm: str ) -> int:
   return int(str(hhmm).split(':')[0])*60*60+int(str(hhmm).split(':')[1])*60
 
""" Schedules COVID data updates at given delay and adds the update details to list_of_updates list """
def schedule_covid_updates(update_interval:int, update_name, location:str, location_type:str):
   starting_val = 1
   if location == city_name:
       starting_val = 0
   title = location + " COVID-19 data update"
   update_name = covid_data_scheduler.enter(update_interval,1,parse_json_data,(covid_API_request(location,location_type),starting_val,))
   content = "COVID data will update every " + str(update_interval) + " seconds"
   list_of_updates.append({
       "title":title,
       "content":content
   })
 
""" Schedules COVID news updates every 1000 seconds and adds the update details to list_of_updates list """
def update_news(delay = 1000):
   e1 = news_scheduler.enter(delay,1,news_api_request)
   content = "COVID news will update every " + str(delay) + " seconds"
   list_of_updates.append({
       "title":"News Update",
       "content":content
   })
 
""" Delete update from list of updates """
def delete_update(update_title_to_delete):
   for update in list_of_updates:
       if update["title"] == update_title_to_delete:
           list_of_updates.remove(update)
 
""" Initiliases the variables before web page is started (Exeter data, nation data and COVID news) """
parse_json_data(covid_API_request(city_name,'ltla'),0)
parse_json_data(covid_API_request('England','nation'),1)
news_api_request()

""" Intiliases the logging file and format """
logging.basicConfig(
       filename='logging.log',
       level=logging.INFO,
       format='%(asctime)s:%(levelname)s:%(message)s'
       )

app = Flask(__name__, template_folder='templates')
 
@app.route('/index')
def main_page():
  
   """ Web server variables """
   title = str(city_name).upper() + " COVID HUB"
   location = city_name
   nation_location = "England"
  
   """ Checks if form has been filled, if not initiliases the web sever variables """
   if get_updated() == False:
       local_7day_infections = ()
       national_7day_infections = ()
       Hospital_cases = ()
       Deaths_total = ()
  
   """ Checks if form has been filled, if so transfers form data into form_data dictionary """
   try:
        if request.method == "GET" and form_data['Update_label'] != ():
            form_data['Scheduled_data_updates'] = request.args.get('update')
            form_data['Update_label'] = request.args.get('two')
            form_data['Repeat_update'] = request.args.get('repeat')
            form_data['Update_covid_data'] = request.args.get('covid-data')
            form_data['Update_news_article'] = request.args.get('news')
   except ValueError:
        logging.error("Invalid form input")
  
   """ Delete news when the cross is clicked """
   if request.args.get("notif"):
       article_title_to_delete = request.args.get("notif")
       delete_news(article_title_to_delete)
       logging.info("Article deleted")
 
   """ Delete updates when the cross is clicked """
   if request.args.get("update_item"):
       update_title_to_delete = request.args.get("update_item")
       delete_update(update_title_to_delete)
       logging.info("Updated cancelled")
 
   """ Checks if form has been filled, if so make run updates if necessary """
   if form_data['Update_label'] != None:
       logging.info("Form submitted - " + str(form_data))

       updated = True
 
       """ Calculates delay to update COVID data """
       current_time_in_seconds = time.gmtime().tm_hour*60*60 + time.gmtime().tm_min*60
       delay = hhmm_to_seconds(str(form_data['Scheduled_data_updates'])) - current_time_in_seconds
      
       """ Run schedulers """
       if form_data['Repeat_update']:
           """ Looks for new COVID news every 1000 seconds """
           if form_data['Update_news_article']:
               update_news()
               news_scheduler.run(blocking=False)
               logging.info("News update scheduled every 1000 seconds")
 
           """ Looks for new COVID data at a given delay """
           if form_data['Update_covid_data']:
               schedule_covid_updates(delay,form_data['Update_label'],city_name,'ltla',)
               schedule_covid_updates(delay,form_data['Update_label'],'England','nation',)
               covid_data_scheduler.run(blocking=False)
               logging.info("COVID data update scheduled every " + str(delay) + " seconds")
       else:
           """ Looks if user wanted to update COVID data manually """
           if form_data['Update_covid_data']:
               parse_json_data(covid_API_request(city_name,'ltla'),0)
               parse_json_data(covid_API_request('England','nation'),1)
               logging.info("Manual COVID data update")

           """ Looks if user wanted to update COVID news manually """
           if form_data['Update_news_article']:
               news_api_request()
               logging.info("Manual news update")
 
   return render_template(
       'index.html',
       favicon = "favicon.ico",
       image = "favicon.png",
       updates = list_of_updates,
       news_articles = get_accepted_articles(),
       title = title,
       location = location,
       local_7day_infections = exeter_covid_data['7DayCases'],
       nation_location = nation_location,
       national_7day_infections = nation_covid_data['7DayCases'],
       hospital_cases = nation_covid_data['HospitalCases'],
       deaths_total = nation_covid_data['DeathsTotal']
       )
 
if __name__ == '__main__':
   app.run()
