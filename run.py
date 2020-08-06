from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient
import pymongo
import bcrypt

from parse_ttn import num_catalog
from test_mongodb import sp_catalog

app = Flask(__name__)

#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#app.config['MONGO_DBNAME'] = 'bktlist'
#app.config['MONGO_URI'] = 'mongodb://kihara:kihara@ds151752.mlab.com:51752/bktlist'

#Yy6HEg3jKWh#ah7


client = pymongo.MongoClient("mongodb+srv://atlasAdmin:123@cluster0.l91mz.mongodb.net/user?retryWrites=true&w=majority")
db = client.user
collection = db.user


#client = MongoClient('mongodb+srv://atlasAdmin:Yy6HEg3jKWh#ah7@cluster0.l91mz.mongodb.net/users?retryWrites=true&w=majority')
#db = client.users


@app.route('/')
def home():
    if 'username' in session:
        log = 'You are logged in as ' + session['username']
        name_input = 'Выход'
        name = session['username']
        return render_template('home.html', name_input=name_input, name=name)
    else:
        name_input = 'Вход'
        return render_template('home.html', name_input=name_input)

@app.route('/main')
def main():
    sp = list()
    if 'username' in session:
        log = 'You are logged in as ' + session['username']
        name_input = 'Выход'
        name = session['username']
        #print(sp_catalog(name))


        return render_template('main.html', name_input=name_input, name=name, result=sp_catalog(name))
    else:
        name_input = 'Вход'
        return 'Не авторизированным пользователям страница недоступна'
        #return render_template('main.html', name_input=name_input)

@app.route('/index')
def index():
    if 'username' in session:
        log = 'You are logged in as ' + session['username']
        name_input = 'Выход'
        name = session['username']
        return render_template('index.html', name_input=name_input, name=name)
        #return 'You are logged in as ' + session['username']
    else:
        name_input = 'Вход'
        return render_template('index.html', name_input=name_input)


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if collection.find_one({'name': request.form['username']}):
            results = collection.find_one({'name': request.form['username']})
            if bcrypt.checkpw(request.form['pass'].encode('utf-8'), results['password']):
                session['username'] = request.form['username']
                return redirect(url_for('index'))
    return 'Invalid username or password'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if collection.find_one({'name': request.form['username']}):
            print(request.form['username'])
            return 'That username already exists!'
        else:
            print("нету такого имени")
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            collection.insert_one({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        #return 'That username already exists!'

    return render_template('register.html', name_input='Выход')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/parse')
def parse():
    if 'username' in session:
        log = 'You are logged in as ' + session['username']
        name_input = 'Выход'
        name = session['username']
        return render_template('index.html', name_input=name_input, name=name)
        #return 'You are logged in as ' + session['username']
    else:
        name_input = 'Вход'
        return render_template('index.html', name_input=name_input)
    return render_template('parse.html')

@app.route('/parse_url', methods=['POST'])
def parse_url():
    url = request.form['url']
    obj = request.form['obj']
    num_page = int(request.form['num_page'])
    name = session['username']
    db = client.price_catalog
    coll = db[name]
    coll.delete_many({})
    num_catalog(url, obj, num_page, name)
    return redirect(url_for('main'))

@app.route('/base')
def base():
    if 'username' in session:
        log = 'You are logged in as ' + session['username']
        name_input = 'Выход'
        name = session['username']
        return render_template('home.html', name=name)
    else:
        name_input = 'Вход'
        return 'Не авторизированным пользователям страница недоступна'
        #return render_template('main.html', name_input=name_input)



if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)