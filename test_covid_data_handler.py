from covid_data_handler import delete_update, hhmm_to_seconds, parse_csv_data, update_news, process_covid_csv_data, covid_API_request, schedule_covid_updates, get_updated, parse_json_data
from random import randint
import sched, time, logging

def test_all():
    test_get_updated()
    test_parse_csv_data()
    test_process_covid_csv_data()
    test_covid_API_request()
    test_parse_json_data()
    test_hhmm_to_seconds()
    test_schedule_covid_updates()
    test_update_news()
    test_delete_update()
    logging.info("COVID data handling test completed")

def test_get_updated():
    assert isinstance(get_updated(),bool)

def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = process_covid_csv_data (parse_csv_data('nation_2021-10-28.csv'))
    assert str(last7days_cases) == "240299"
    assert str(current_hospital_cases) == "7019"
    assert str(total_deaths) == "141544"

def test_covid_API_request():
    data = covid_API_request(location='Exeter',location_type='ltla')
    assert isinstance(data, dict)

def test_parse_json_data():
    assert isinstance(parse_json_data(covid_API_request(location='Exeter',location_type='ltla'),0),dict)

def test_hhmm_to_seconds():
    test_time_input_1 = randint(0,23)
    test_time_input_2 = randint(0,59)
    test_time:str
    
    if test_time_input_1 < 10:
        test_time = "0" + str(test_time_input_1) + ":"
    else:
        test_time = str(test_time_input_1) + ":"
    
    if test_time_input_2 < 10:
        test_time = test_time + "0" + str(test_time_input_1)
    else:
        test_time = test_time + str(test_time_input_1)

    assert isinstance(hhmm_to_seconds(test_time), int)

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test',location='Exeter',location_type='ltla')

def test_update_news():
    update_news()

def test_delete_update():
    delete_update("Exeter COVID-19 data update")

logging.basicConfig(
       filename='logging.log',
       level=logging.INFO,
       format='%(asctime)s:%(levelname)s:%(message)s'
       )

test_scheduler = sched.scheduler(time.time,time.sleep)
test_scheduler.enter(60*60,1,test_all)
test_scheduler.run