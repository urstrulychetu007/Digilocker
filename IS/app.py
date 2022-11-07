import re
from select import select
from urllib import request
from encrypt import decrypt_file, encrypt_file
from flask  import *
import sqlite3
from random import *
import base64
import requests
from test import digilocker
app = Flask(__name__)
db = sqlite3.connect('database.db',check_same_thread=False)



def add_user_to_db(query):
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()

def validate_users(user,pin):
    try:
        if len(user)==10:
            id = 0
            query = f'select phone from users'
            cursor =db.cursor()
            cursor.execute(query)
            pins = cursor.fetchall()
            # if encrypt_file(pin.encode()) == decrypt_file(pins[0][0])
            for i in pins[0]:
                if decrypt_file(i[2:-1].encode()).decode() == user:
                    break
                else:
                    id+=1
            query = f'select password,username,phone from users where phone = "{pins[0][id]}"'
            cursor =db.cursor()
            cursor.execute(query)
            pins = cursor.fetchall()  
            
            # return pins 
            if decrypt_file(pins[0][0][2:-1].encode()).decode() == pin:
                user = decrypt_file(pins[0][1][2:-1].encode()).decode()
                phone = decrypt_file(pins[0][2][2:-1].encode()).decode()

                print(user)
                return True,user,phone
            return False,'',''
    except:
        return False,'',''   


# @app.rou

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/home/<user>/<phone>')
def home(user,phone):
    data = digilocker(phone[:5],'A')
    data1 = digilocker(phone[:5],'C')
    file_=open('static/aadhaar/images/'+data,'rb')
    file1_=open('static/collegeid/images/'+data1,'rb')
    data = file_.read()
    decoded_img = decrypt_file(data)
    base64_encoded_data = base64.b64encode(decoded_img)
    base64_message = base64_encoded_data.decode('utf-8')
    data1 = file1_.read()
    decoded1_img = decrypt_file(data1)
    base641_encoded_data = base64.b64encode(decoded1_img)
    base641_message = base641_encoded_data.decode('utf-8')
    # print(base64_message)
    user=user.upper()
    return render_template('home.html',data=base64_message,user=user,data1=base641_message)


@app.route('/signin',methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        user = request.form['user']
        pin = request.form['pin']
        pins,username,mobile = validate_users(user,pin)
        
        if pins:
            return redirect(url_for('home',user=username,phone=mobile))
        else:
            return 'Logged In Failed'    

    return render_template('login.html')

@app.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        pin = request.form['pin']

        name = encrypt_file(name.encode())
        number = encrypt_file(number.encode())
        pin = encrypt_file(pin.encode())
        unid = randint(00000000000,99999999999)
        query = f'insert into users values("{name}","{number}","{unid}","{pin}")'
        add_user_to_db(query)
        return redirect(url_for('signin'))
        # return f'{name} {number} {pin}'


    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)