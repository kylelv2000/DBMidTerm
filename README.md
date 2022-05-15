# 配数据库的过程
## 1. 装SQL Server和配套的SMSS
## 2. SMSS启动, 打开CovidData.sql, 点运行. 这样创建好数据库了.
## 3. 右键CovidData数据库, 选数据平面, 导入Data下的2022_population.csv, 然后执行PreprocessCountry.sql. 这样导入了国家的数据.
## 4. 同样的方式导入Hospital.csv, 但是选数据类型的时候要把nvchar(*)都改成nvchar(256). 执行PreprocessHospital.sql. 导入了医院的数据.
## 5. 执行UpdatePatient.sql. 这是一个存储过程也就是函数, 会被导入数据库, 以后EXEC它就可以调用.