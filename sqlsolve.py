def getAllCountries():
    return ['zg','sa','sd']

def searchInfo(date1,date2,country):
    infos = [[331,122,324,123,452,213,432,213],[1,2,3,4,2,3,1,3],[100,100,111,222,111,222,111,113]]
    tl = [1,2,3,4,5,6,7,8]
    return infos, tl

def searchGlobal(data):
    value = [95.1, 23.2, 43.3, 66.4, 88.5]
    attr = ["China", "Canada", "Brazil", "Russia", "United States"] 
    qaz=[]
    for i in range(5):
        qaz.append([attr[i],value[i]])
    return qaz
