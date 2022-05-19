# %%
from dataclasses import dataclass
import pymssql
from datetime import datetime, timedelta


# 导入阶段初始化，连接数据库
conn = pymssql.connect(host='127.0.0.1', user='sa', password='123456', database='CovidData')
cursor = conn.cursor()
# %%
def get_hospital_table(hospital, passwd):
    # 获得某个医院所有病人的表格
    hospital_id = hospital[hospital.find('(') + 1:hospital.find(')')]
    cursor.execute('''
        SELECT 1 FROM Hospital
        WHERE Hospital# = %s AND Password = %s
    ''', (hospital_id, passwd))
    if not cursor.fetchall():
        return 1, "密码错误"
    cursor.execute('''
        SELECT ID, Status, "Date Admitted", "Date Leave"
        FROM Patients
        WHERE Patients.Hospital# = %s
        ORDER BY "Date Admitted" ASC, "Date Leave" ASC
        ''',
        hospital_id
    )
    rs = cursor.fetchall()
    convert_fn = lambda x: 'null' if x is None else datetime.strftime(x, '%Y-%m-%d')
    rs = [(entry[0], entry[1], convert_fn(entry[2]), convert_fn(entry[3]))
        for entry in rs]
    # 返回的表格rs格式：元组的列表, 每个元组对应域（ID, 状态, 入院日期, 出院日期）, 均为字符串
    return 0, rs
# %%
x = get_hospital_table('(100)', '123456')
# %%
x[1][0][1]
# %%
