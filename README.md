# 配数据库的过程
## 1. 装SQL Server和配套的SMSS
## 2. SMSS启动, 打开CovidData.sql, 点运行. 这样创建好数据库了.
## 3. 右键CovidData数据库, 选数据平面, 导入Data下的2022_population.csv, 然后执行PreprocessCountry.sql. 这样导入了国家的数据.
## 4. 同样的方式导入Hospital.csv, 但是选数据类型的时候要把nvchar(*)都改成nvchar(256). 执行PreprocessHospital.sql. 导入了医院的数据.
## 5. 执行UpdatePatient.sql. 这是一个存储过程也就是函数, 会被导入数据库, 以后EXEC它就可以调用.

# web
运行app.py

网站运行在 http://localhost:8080

# 更新
## p1点过一次查询之后没法更新新的国家了
## 所有的日期框一次查询后会变成普通的输入框
## 实际传过来的日期是'yyyy-mm-dd'格式的, 分隔符不是'/'
## 提交页面的状态下面有两个"康复", 要改成"患病, 死亡, 康复"