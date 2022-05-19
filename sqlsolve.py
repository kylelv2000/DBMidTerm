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
    cursor.execute('''
        DECLARE @return int;
        EXEC @return = ReportPatient @Hospital# = %s, @Password = %s, @ID = %s, @Status = %s;
        SELECT @return;
        ''',
        (hospital_id, passwd, patient_id, state)
    )
    return_code = cursor.fetchall()[0][0]
    if return_code == 0:
        conn.commit()
        return_msg = '操作成功'
    elif return_code == 1:
        return_msg = '密码错误'
    elif return_code == 2:
        return_msg = '非法的病人状态'
    elif return_code == 3:
        return_msg = '待插入的病人信息已经存在'
    elif return_code == 4:
        return_msg = '待更新的住院病人信息不存在'
    return return_code, return_msg

def update_hospital(hospital, passwd):
    # 把医院的病人信息更新到Updates表
    hospital_id = hospital[hospital.find('(') + 1:hospital.find(')')]
    cursor.execute('''
        DECLARE @return int;
        EXEC @return = ReportHospital @Hospital# = %s, @Password = %s;
        SELECT @return;
        ''',
        (hospital_id, passwd)
    )
    return_code = cursor.fetchall()[0][0]
    if return_code == 0:
        conn.commit()
        return_msg = '操作成功'
    else:
        return_msg = '密码错误'
    return return_code, return_msg

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