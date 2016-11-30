from flask import request,session,Flask,render_template,make_response, \
    url_for,redirect,abort,g,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:123456@localhost/flask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
boot = Bootstrap(app)
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

@app.before_first_request
def initContext():
    app.config['username'] = 'allen'
    app.config['password'] = 'beta'

@app.errorhandler(500)
def errorHandler(e):
    return render_template('/error.html')

@app.route("/")
def index():
    if session.get('user') is None:
        return redirect(url_for("login"))
    return render_template('/index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        if app.config['username'] == request.form.get('username',None) \
            and app.config['password'] == request.form.get('password',None):
            session['user'] = request.form.get('username')
            logging.debug('username:%s,password:%s' %(request.form.get('username',None),request.form.get('password',None)))
            return redirect(url_for('index'))
        else:
            flash("用户名或密码错误")
            logging.debug('login failed,%s,%s' % (request.form.get('username',None),request.form.get('password',None)))
            print("login failed,%s,%s" % (request.form.get('username',None),request.form.get('password',None)))
    return render_template("/login.html")


class User(db.Model):
    __tablename__ = 't_users'
    id = db.Column(db.BigInteger,primary_key=True)
    username = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255))
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username+','+self.password




















if __name__ == '__main__':
    app.secret_key = 'hard to guess'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()