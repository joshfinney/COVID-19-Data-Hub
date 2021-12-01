
# COVID-19 Data Hub

Web server powered by Flask, made for ECM1400 Programming coursework at Exeter University


## 👨🏽‍💻 Repository

- [Github Repo](https://github.com/joshfinney/COVID-19-Data-Hub)
## 👨🏽‍🎓 Author

- [@joshfinney](https://github.com/joshfinney)


## 📰 Configuration

1. Get required API key from:
- [NewsAPI](https://newsapi.org/)

2. Replace fields in ``` ./config.json ```
 
 

```html
{
  "API-keys": {
    "news": "Insert API key from https://newsapi.org/"
  },
	"information":{
		"city":"Insert name of English city you would like to personalise web page with"
		}
}
```


## 🚀 Installation

1. Install the following packages:
- [flask](https://flask.palletsprojects.com/en/2.0.x/)
- [uk_covid19](https://github.com/publichealthengland/coronavirus-dashboard-api-python-sdk)

2. Run `covid_data_handler.py`, `test_covid_data_handler.py` and `test_news_data_handling.py`

3. Server should be running locally at port 5000 (/index)
    
## ⛔️ Project structure
```
covid-data-hub-main/
├─ static/
│  ├─ images/
│  │  ├─ favicon.ico
│  │  ├─ favicon.png (server logo)
├─ nation_2021-10-28.csv
├─ LICENSE (contains licensing terms)
├─ config.json (stores server configuration)
├─ gb-news.json
├─ logging.log (contains record of server interactions)
├─ README.md
├─ covid_data_handler.py (controls web-server variables)
├─ covid_news_handling.py (controls the back-end for COVID news)
├─ test_covid_data_handler.py (runs regular tests on covid_data_handler.py)
├─ test_news_data_handling.py (runs regular tests on covid_news_handling.py)
```


## 📝 License
Copyright © 2021 [Joshua](https://github.com/joshfinney).

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.
