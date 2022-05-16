from flask import Flask, request, render_template

import sqlsolve
import graphs

app = Flask(__name__)
app._static_folder = "./templates/static"

@app.route('/')
def hello_world():
    return 'Hello, World!'


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

    infos = sqlsolve.searchGlobal(date)   #return [(国家名, 现存？)]
    c = graphs.makeMapGraph(infos, date)
    
    return render_template('p2.html',
                           begintime = date,
                           graphdate = c.dump_options_with_quotes()
                            )


@app.route('/p2', methods=['GET'])
def get_p2():
    countries = sqlsolve.getAllCountries() #返回数组 例：['zg','sa','sd']
    return render_template('p2.html',
                           begintime = "",
                           graphdate = ""
                            )


if __name__ =="__main__":
    app.run(debug=True, port=8080)
