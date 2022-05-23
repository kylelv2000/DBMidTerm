#! /usr/bin/env python3
from flask import Flask, request, render_template, redirect, url_for, jsonify
import sqlsolve
import graphs

app = Flask(__name__)
app._static_folder = "./templates/static"

@app.route('/')
def hello_world():
    return render_template('index.html'
                            )
@app.route('/', methods=['POST'])
def post_index():
    page = request.form['options']
    if(page == '1'):
        return redirect(url_for('get_p1'))
    elif(page == '2'):
        return redirect(url_for('get_p2'))
    elif(page == '3'):
        return redirect(url_for('get_p3'))


@app.route('/p1', methods=['POST'])
def post_p1():
    date1 = request.form['begintime']    #'2019/01/01'
    date2 = request.form['endtime']
    if date2 < date1:                    # 按字符串比较即可
        date1, date2 = date2, date1
    country = request.form['countries']

    infos, time_list = sqlsolve.searchInfo(date1,date2,country)   #return [[新增],[死亡],[康复]], 对应长度日期数组
    c = graphs.makeLineGraph(infos, time_list)
    
    return render_template('p1.html',
                           countries = [country],
                           begintime = date1,
                           endtime = date2,
                           graphdate = c.dump_options()
                            )


@app.route('/p1', methods=['GET'])
def get_p1():
    countries = sqlsolve.getAllCountries() #返回数组 例：['zg','sa','sd']
    return render_template('p1.html',
                           countries = countries,
                           begintime = "",
                           endtime = "",
                           graphdate = ""
                            )


@app.route('/p2', methods=['POST'])
def post_p2():
    date = request.form['begintime']    #'2019/01/01'

    infos = sqlsolve.searchGlobal(date)   #return [[国家名, 现存?], ...]
    c = graphs.makeMapGraph(infos, date)
    
    return render_template('p2.html',
                           begintime = date,
                           graphdate = c.dump_options_with_quotes()
                            )


@app.route('/p2', methods=['GET'])
def get_p2():
    return render_template('p2.html',
                           begintime = "",
                           graphdate = ""
                            )


@app.route('/p3', methods=['POST'])
def post_p3():
    data = request.get_json()
    country = data['country']
    city = data['city']
    hospital = data['hospital']
    passwd = data['passwd']
    number = data['number']
    state = data['state']
    code,msg = sqlsolve.update(country, city, hospital, passwd, number, state)
    tables = sqlsolve.get_hospital_table(hospital, passwd)
    
    return jsonify([code,msg,tables])


@app.route('/p3', methods=['GET'])
def get_p3():
    countries = sqlsolve.getAllCountries() #返回数组 例：['zg','sa','sd']
    return render_template('p3.html',
                            countries = countries,
                            )

@app.route('/updatehospital', methods=['POST'])
def updatehospital():
    data = request.get_json()
    hospital = data['hospital']
    passwd = data['passwd']
    code,msg = sqlsolve.update_hospital(hospital, passwd)
    tables = sqlsolve.get_hospital_table(hospital, passwd)
    
    return jsonify([code,msg,tables])

@app.route('/selectfieldcity/', methods=['GET', 'POST'])
def selectfieldcity():
    if request.method == "POST":
        data = request.get_json()
        country = data['name']
        city = sqlsolve.getCity(country)  #返回数组 例：['zg','sa','sd']
        return jsonify(city)
    else:
        return {}

@app.route('/selectfieldhospital/', methods=['GET', 'POST'])
def selectfieldhospital():
    if request.method == "POST":
        data = request.get_json()
        country = data['country']
        city = data['name']
        hospital = sqlsolve.getHospital(country, city)  #返回数组 例：['zg','sa','sd']
        return jsonify(hospital)
    else:
        return {}

if __name__ =="__main__":
    app.run(debug=True, port=8080)
