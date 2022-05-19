import pymssql
from datetime import datetime, timedelta


# 导入阶段初始化，连接数据库
conn = pymssql.connect(host='127.0.0.1', user='sa', password='123456', database='CovidData')
cursor = conn.cursor()


def getAllCountries():
    # 返回格式：['Afghanistan', 'Albania', 'Algeria', ...]
    cursor.execute('SELECT "Name" FROM Country ORDER BY "Name" ASC')
    rs = cursor.fetchall()
    return [entry[0] for entry in rs]

def searchInfo(date1,date2,country):
    # 假设date1, date2的查询是双闭的
    cursor.execute('''
    SELECT "Date", "New Cases", "New Deaths", "New Recovered" 
    FROM Infection, Country
    WHERE Infection.ISO = Country.ISO 
        AND Country."Name" = %s
        AND DATEDIFF(DAY, %s, "Date") >= 0 AND DATEDIFF(DAY, "Date", %s) >= 0
    ORDER BY "Date" ASC
    ''', (country, date1, date2))  # 调用execute的字符串格式化接口可以防止注入攻击
    rs = cursor.fetchall()
    # 假设日期格式是 yyyy-mm-dd
    date1 = datetime.strptime(date1, '%Y-%m-%d').date()
    date2 = datetime.strptime(date2, '%Y-%m-%d').date()
    # 数据库不一定覆盖了日期区间，用0补齐
    if not rs:
        pad = (date2 - date1).days + 1
        infos = [[0 for _ in range(pad)], [0 for _ in range(pad)], [0 for _ in range(pad)]]
    else:
        pad_before = (rs[0][0] - date1).days
        pad_after = (date2 - rs[-1][0]).days
        infos = [
            [0 for _ in range(pad_before)] + [entry[1] for entry in rs] + [0 for _ in range(pad_after)],
            [0 for _ in range(pad_before)] + [entry[2] for entry in rs] + [0 for _ in range(pad_after)],
            [0 for _ in range(pad_before)] + [entry[3] for entry in rs] + [0 for _ in range(pad_after)],
        ]
    tl = []
    ptr = date1
    while ptr <= date2:
        tl.append(datetime.strftime(ptr, '%m-%d'))
        ptr += timedelta(days=1)
    return infos, tl

def searchGlobal(date):
    # 查询所有国家现存病例, (总病例-总死亡-总康复)
    cursor.execute('''
    SELECT "Name", "Total Cases" - "Total Deaths" - "Total Recovered"
    FROM Infection, Country
    WHERE Infection.ISO = Country.ISO
        AND "Date" = (SELECT DISTINCT MAX("Date") 
                      FROM Infection AS I 
                      WHERE I.ISO = Country.ISO AND DATEDIFF(DAY, I."Date", %s) >= 0)
    ORDER BY "Name" ASC
    ''', date)
    rs = cursor.fetchall()
    return rs

def getCity(country):
    # 这里的city可能都改成了state, 因为city实在太多了, 下拉7000多项不太好
    cursor.execute('''
    SELECT DISTINCT "State"
    FROM Hospital, Country
    WHERE Hospital.ISO = Country.ISO AND Country."Name" = %s
    ORDER BY "State" ASC
    ''', country)
    rs = cursor.fetchall()
    return [entry[0] for entry in rs]

def getHospital(country, state):
    # 医院可能会重名，显示的医院命名为 医院名(医院ID)
    cursor.execute('''
    SELECT Hospital."Name", Hospital#
    FROM Hospital, Country
    WHERE Hospital.ISO = Country.ISO AND Country."Name" = %s AND Hospital."State" = %s
    ORDER BY Hospital."Name" ASC
    ''', (country, state))
    rs = cursor.fetchall()
    return ['%s(%s)' % entry for entry in rs]

def update(country, city, hospital, passwd, number, state):
    hospital_id = hospital[hospital.find('(') + 1:hospital.find(')')]
    patient_id = str(number)
    if state == '患病':
        state = 'In Hospital'
    elif state == '死亡':
        state = 'Dead'
    elif state == '康复':
        state = 'Recovered'
    cursor.execute(
        'ReportPatient @Hospital# = %s, @Password = %s, @ID = %s, @Status = %s', 
        (hospital_id, passwd, patient_id, state)
    )
    return True
