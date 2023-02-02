### SQLAlchemy     
---    

[Крадущийся тигр, затаившийся SQLAlchemy. Основы](https://habr.com/ru/post/470285/)     
[SQLAlchemy. Основы](https://github.com/sandix90/sqlalchemy_basics) - как кажется хороший пример кода     
[SQLAlchemy](https://ru.wikibooks.org/wiki/SQLAlchemy) - хороший пример кода

[Alembic’s documentation](https://alembic.sqlalchemy.org/en/latest/)     
[Пишем и тестируем миграции БД с Alembic. Доклад Яндекса](https://habr.com/ru/company/yandex/blog/511892/)    
[Создаем начальную миграцию с alembic для существующей базы](https://habr.com/ru/post/585228/)    

---     

[Psycopg documentation](https://www.psycopg.org/docs/install.html)      
[psycopg 3 documentation](https://www.psycopg.org/psycopg3/docs/basic/install.html)     

---   

[Advanced Python Scheduler (APScheduler) - User guide](https://apscheduler.readthedocs.io/en/master/)    
[Advanced Python Scheduler - User guide](https://apscheduler.readthedocs.io/en/3.x/index.html)    
[Advanced Python Scheduler - GitHub](https://github.com/agronholm/apscheduler)     


### SCRAM authentication requires libpq version 10 or above

[sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) SCRAM authentication requires libpq version 10 or above #1360](https://github.com/psycopg/psycopg2/issues/1360)   
[Fix Unable to connect to PostgreSQL server: SCRAM authentication requires libpq version 10 or above](https://dothanhlong.org/fix-unable-to-connect-to-postgresql-server-scram-authentication-requires-libpq-version-10-or-above/)    
[How can I solve Postgresql SCRAM authentication problem](https://stackoverflow.com/questions/62807717/how-can-i-solve-postgresql-scram-authentication-problem)    
[psycopg2/scripts/build/build_manylinux_2_24.sh](https://github.com/psycopg/psycopg2/blob/53bda13afa1aea458faec82145d0a5f511267bd5/scripts/build/build_manylinux_2_24.sh)    

### WeatherAPI    
---     

[Weather API Documentation](https://www.weatherapi.com/docs/)     

[Weather API Interactive API Explorer](https://www.weatherapi.com/api-explorer.aspx)     

[Weather API Base URL](http://api.weatherapi.com/v1)      

```bash
# API KEY b7ff015b30d4496180b90059230102
```

``` bash
curl "https://api.weatherapi.com/v1/current.json?key=b7ff015b30d4496180b90059230102&q=Voronezh&aqi=yes&lang=ru" | jq '.'

curl "https://api.weatherapi.com/v1/current.json?key=b7ff015b30d4496180b90059230102&q=51.672,39.1843&aqi=yes&lang=ru" | jq '.'

```    

---   

[RapidAPI](https://rapidapi.com/)     
[Meteostat JSON API](https://dev.meteostat.net/api/)    

---    

[Weather Forecast API](https://open-meteo.com/en/docs)    

---   

[Real-Time & Historical World Weather Data API](https://weatherstack.com/)    
[Weatherstack API Documentation](https://weatherstack.com/documentation)    

```bash
# Weatherstack API Key: 39f4d0bae7f4f1de14eb1caadf9e8275

curl "http://api.weatherstack.com/current?access_key=39f4d0bae7f4f1de14eb1caadf9e8275&query=51.672,39.1843&units=m" | jq '.'

curl "http://api.weatherstack.com/current?access_key=39f4d0bae7f4f1de14eb1caadf9e8275&query=Voronezh&units=m" | jq '.'

```

---
