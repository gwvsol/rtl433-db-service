## RTL433DB SERVICE
---     

[rtl_433](https://triq.org/rtl_433)    

[RTL_433_SQL_Connection](https://github.com/Domifry/RTL_433_SQL_Connection)    
[SQL Connection for RTL_433 #1828](https://github.com/merbanan/rtl_433/issues/1828)    

---   

Зависимости для сборки ```psycopg2``` из исходников         

``` shell
sudo apt install libpq5 libpq-dev

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