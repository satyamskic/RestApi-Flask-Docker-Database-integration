import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/create', methods=['POST'])
def create_emp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()   
        print('Create function called')
        _json = request.json
        _fullName = _json['fullName']
        _telephoneNumber = _json['telephoneNumber']
        _Age = _json['Age']
        print(_fullName+" "+_telephoneNumber)
        if _fullName and _telephoneNumber and _Age and request.method == 'POST':		
            sqlQuery = "INSERT INTO items(fullName, telephoneNumber, Age) VALUES(%s, %s, %s)"
            bindData = (_fullName, _telephoneNumber, _Age)
            cursor.execute(sqlQuery, bindData)
            d = conn.commit()
            print(d)         
            respone = jsonify('user added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        return{'error': str(e)}
    finally:
        cursor.close() 
        conn.close()          
     
@app.route('/emp')
def emp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM items")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  
        
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run(host='0.0.0.0')
