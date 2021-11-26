from covid_news_handling import check_for_deleted_news, delete_news, get_accepted_articles, news_api_request
import sched, time, logging

def test_all():
    test_get_accepted_articles()
    test_delete_news()
    test_check_for_deleted_news()
    test_news_API_request()
    logging.info("News data handling test completed")

def test_get_accepted_articles():
    assert isinstance(get_accepted_articles(),list)

def test_delete_news():
    delete_news("Test article article")

def test_check_for_deleted_news():
    check_for_deleted_news()

def test_news_API_request():
    assert news_api_request()
    assert news_api_request('Covid COVID-19 coronavirus') == news_api_request()

logging.basicConfig(
       filename='logging.log',
       level=logging.INFO,
       format='%(asctime)s:%(levelname)s:%(message)s'
       )

test_all()

test_scheduler = sched.scheduler(time.time,time.sleep)
test_scheduler.enter(60*60,1,test_all)
test_scheduler.run