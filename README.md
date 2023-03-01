## RTL433DB SERVICE
---     

[rtl_433](https://triq.org/rtl_433)      

Зависимости для работы ```TUNER DVB-T/T2/C FM & DAB```   

``` shell
# sudo dnf install rtl-433
sudo apt install rtl-433

```

[RTL_433_SQL_Connection](https://github.com/Domifry/RTL_433_SQL_Connection)    
[SQL Connection for RTL_433 #1828](https://github.com/merbanan/rtl_433/issues/1828)    

---   

Зависимости для сборки ```psycopg2``` из исходников         

``` shell
sudo apt install libpq5 libpq-dev

sudo dnf install libpq libpq-devel
sudo dnf install automake jq gcc gcc-c++ kernel-devel \
    git zip unzip tzdata curl wget bzip2 xz cmake autoconf \
    python3-devel python3-pip python3-setuptools python3-wheel

pip install psycopg2

```

```python
import psycopg2

print(psycopg2.__version__)
# 2.9.5 (dt dec pq3 ext lo64)

# Проверяем версию libpq
print(psycopg2.__libpq_version__)
# 130003 <= для корректной работы версия должна быть не ниже

# Проверяем версию extensions.libpq
print(psycopg2.extensions.libpq_version())
# 130003 <= для корректной работы версия должна быть не ниже

# Если версия будет в районе 90623, получим ошибку sqlalchemy
# sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) 
# SCRAM authentication requires libpq version 10 or above

```

```SQL
select t.id, t.datetime, t.temperature, s.model, s.sensor_id from temperature t left join sensors s on t.sensor_id=s.id;
```

```json
{"time" : "2023-03-01 09:24:34", "model" : "inFactory-TH", "id" : 130, "channel" : 1, "battery_ok" : 1, "temperature_F" : 78.900, "humidity" : 38, "mic" : "CRC"}

{"time" : "2023-03-01 09:25:41", "brand" : "OS", "model" : "Oregon-THN132N", "id" : 18, "channel" : 2, "battery_ok" : 1, "temperature_C" : -0.400}
```

[inFactory-TH](https://github.com/merbanan/rtl_433/blob/master/src/devices/infactory.c) - Пример расчета CRC и пример данных         

[rtl_433_tests](https://github.com/gbraux/rtl_433_tests)    

[InFactroy-Temp-Humidity-Sensor-T05K-THC](https://github.com/gbraux/rtl_433_tests/tree/master/tests/InFactroy-Temp-Humidity-Sensor-T05K-THC)     

[Need some help to decode InFactory Temp/Hum Sensor (datas in rtl_443_test)](https://github.com/merbanan/rtl_433/issues/452)    
