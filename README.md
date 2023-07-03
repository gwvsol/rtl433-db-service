## RTL433DB SERVICE
---     

[rtl_433](https://triq.org/rtl_433)      

[RTL_433_SQL_Connection](https://github.com/Domifry/RTL_433_SQL_Connection)    
[SQL Connection for RTL_433 #1828](https://github.com/merbanan/rtl_433/issues/1828)    

---   

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

{"time" : "2023-05-31 15:09:10", "model" : "AlectoV1-Temperature", "id" : 227, "channel" : 1, "battery_ok" : 1, "temperature_C" : 28.300, "humidity" : 20, "mic" : "CHECKSUM"}

```

[inFactory-TH](https://github.com/merbanan/rtl_433/blob/master/src/devices/infactory.c) - Пример расчета CRC и пример данных         

[rtl_433_tests](https://github.com/gbraux/rtl_433_tests)    

[InFactroy-Temp-Humidity-Sensor-T05K-THC](https://github.com/gbraux/rtl_433_tests/tree/master/tests/InFactroy-Temp-Humidity-Sensor-T05K-THC)     

[Need some help to decode InFactory Temp/Hum Sensor (datas in rtl_443_test)](https://github.com/merbanan/rtl_433/issues/452)      


```log

time      : 2023-05-31 15:16:13
model     : AlectoV1-Temperature                   House Code: 227
Channel   : 1            Battery   : 1             Temperature: 28.30 C      Humidity  : 20 %          Integrity : CHECKSUM
pulse_demod_ppm(): AlectoV1 Weather Sensor (Alecto WS3500 WS4500 Ventus W155/W044 Oregon)
bitbuffer:: Number of rows: 9 
[00] { 0}                : 
[01] {36} c7 0d 88 04 f0 : 11000111 00001101 10001000 00000100 1111
[02] {36} c7 0d 88 04 f0 : 11000111 00001101 10001000 00000100 1111
[03] {36} c7 0d 88 04 f0 : 11000111 00001101 10001000 00000100 1111
[04] {36} c7 0d 88 04 f0 : 11000111 00001101 10001000 00000100 1111
[05] {36} c7 0d 88 04 f0 : 11000111 00001101 10001000 00000100 1111
[06] {36} c7 0d 88 04 f0 : 11000111 00001101 10001000 00000100 1111
[07] {36} c7 0d 88 04 f0 : 11000111 00001101 10001000 00000100 1111
[08] {25} c7 0d 88 00    : 11000111 00001101 10001000 0

time      : 2023-05-31 15:16:19
model     : AlectoV1-Temperature                   House Code: 227
Channel   : 1            Battery   : 1             Temperature: 28.30 C      Humidity  : 20 %          Integrity : CHECKSUM
pulse_demod_ppm(): AlectoV1 Weather Sensor (Alecto WS3500 WS4500 Ventus W155/W044 Oregon)
bitbuffer:: Number of rows: 9 
[00] { 0}                : 
[01] {36} c7 1d 88 04 e0 : 11000111 00011101 10001000 00000100 1110
[02] {36} c7 1d 88 04 e0 : 11000111 00011101 10001000 00000100 1110
[03] {36} c7 1d 88 04 e0 : 11000111 00011101 10001000 00000100 1110
[04] {36} c7 1d 88 04 e0 : 11000111 00011101 10001000 00000100 1110
[05] {36} c7 1d 88 04 e0 : 11000111 00011101 10001000 00000100 1110
[06] {36} c7 1d 88 04 e0 : 11000111 00011101 10001000 00000100 1110
[07] {36} c7 1d 88 04 e0 : 11000111 00011101 10001000 00000100 1110
[08] {24} c7 1d 88       : 11000111 00011101 10001000 

time      : 2023-05-31 15:16:30
model     : inFactory-TH ID        : 130
Channel   : 1            Battery OK: 1             Temperature: 77.90 F      Humidity  : 28 %          Integrity : CRC
pulse_demod_ppm(): inFactory, nor-tec, FreeTec NC-3982-913 temperature humidity sensor
bitbuffer:: Number of rows: 1 
[00] {40} 82 c2 68 f2 81 : 10000010 11000010 01101000 11110010 10000001 

time      : 2023-05-31 15:17:13                    brand     : OS
model     : Oregon-THN132N                         House Code: 18
Channel   : 2            Battery   : 1             Celsius   : 24.70 C
pulse_demod_manchester_zerobit(): Oregon Scientific Weather Sensor
bitbuffer:: Number of rows: 1 
[00] {168} 55 55 55 55 99 95 a5 a6 aa 9a 9a 6a aa 56 a6 9a aa aa 5a 65 aa 
OS v2.1 sync byte search - test_val=559995a5 pattern=55990000    mask=ffff0000
OS v2.1 Sync test val 559995a5 found, starting decode at bit 0
Found sensor_id (0000ec40)

```

```sql

SELECT sensors.model, temperature, humidity, temperature.datetime FROM temperature JOIN sensors ON temperature.sensor_id = sensors.id WHERE sensors.model='Oregon-THGR810' ORDER BY temperature.datetime DESC limit 1;

SELECT sensors.model, temperature, humidity, temperature.datetime FROM temperature JOIN sensors ON temperature.sensor_id = sensors.id WHERE sensors.model='AlectoV1-Temperature' ORDER BY temperature.datetime DESC limit 1;

SELECT sensors.model, temperature, humidity, temperature.datetime FROM temperature JOIN sensors ON temperature.sensor_id = sensors.id WHERE sensors.model='inFactory-TH' ORDER BY temperature.datetime DESC limit 1;

```

```sql
SELECT temperature.temperature AS temperature_temperature, temperature.humidity AS temperature_humidity, temperature.datetime AS temperature_datetime, sensors.model AS sensors_model 
FROM temperature JOIN sensors ON temperature.sensor_id = sensors.id 
WHERE sensors.model = 'Oregon-THN132N' ORDER BY temperature.datetime DESC limit 5;
```   