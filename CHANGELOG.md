#### v0.5    

Сервис получения информации о погоде с Weather API, а так же        
сенсоров погодных станций работающих на частоте 433МГц     
(например Oregon-THGR810, Oregon-THN132N, inFactory-TH,    
AlectoV1-Temperature или Nexus-TH)       
В качестве приемника ипользуеся например:      
```Astrometa DVB-T/T2/C FM & DAB receiver```      
или      
```Realtek Semiconductor Corp. RTL2838 DVB-T```       
Сервис имеет функцию отправки данных на ```narodmon.ru```   
и сохранять полученные данные в базу данных

- Создание образа ```rtl433db:2023-07-26-01-p3.11-bullseye```    

- Файл ```.env``` для настройки приложения     
  
```bash
# =============================================
# RTL433DB -> включение логирования сервиса
export RTL433DB_LOG=on
# =============================================
# WEATHERAPI -> получение данных о погоде
# с сервиса погоды Weather API https://www.weatherapi.com/
# необходимо получить на сервисе WEATHERAPI_KEY
# Параметр не обязательный, при отсуствии 
# WEATHERAPI_KEY и WEATHERAPI_LOCATION
# запрос данных о погоде не будет выполняться
# export WEATHERAPI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxx
# export WEATHERAPI_LOCATION=Voronezh
# Координаты населенного пункта => Широта,Долгота
# export WEATHERAPI_LOCATION=51.672,39.1843
# =============================================
# NARODMON -> отправка данных на https://narodmon.ru
# Параметр не обязательный, при отсуствии 
# NARODMON_HOST или NARODMON_PORT и NARODMON_LOGIN
# отправка данных о погоде не будет выполняться
export NARODMON_HOST=narodmon.ru
export NARODMON_PORT=8283
export NARODMON_LOGIN=xxxxxxxxxxxxxxxxxxxxxxxxxхх
# NARODMON_SENSOR_ID -> ID сенсора
# зарегистрированного на narodmon.ru
export NARODMON_SENSOR_ID=xxxxxxxxxxxxxxxxxxxxxxx
export NARODMON_SENSOR_MODEL=Oregon-THN132N
# Координаты (широта и долгота установки сенсора)
export NARODMON_SENSOR_LAT=51.658194
export NARODMON_SENSOR_LONG=39.200377
# =============================================
# POSTGRESQL -> подключение к базе данных
export POSTGRESQL_HOST=rtl433db-db
export POSTGRESQL_PORT=5432
export POSTGRESQL_USER=postgres
export POSTGRESQL_PASSWORD=RFVmjuIEDC
export POSTGRESQL_DBNAME=rtl433db
# =============================================
```      