from flask import request,session,Flask,render_template,make_response, \
    url_for,redirect,abort,g,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# from flask_moment import Moment
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:123456@localhost/bbq'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
boot = Bootstrap(app)
# moment = Moment(app)

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')


class User(db.Model):
    __tablename__ = 't_users'
    id = db.Column(db.BigInteger,primary_key=True)
    username = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255))
    roleid = db.Column(db.BigInteger,db.ForeignKey('t_roles.id'))

    def __init__(self,username,password,roleid):
        self.username = username
        self.password = password
        self.roleid = roleid


class Role(db.Model):
    __tablename__='t_roles'
    id = db.Column(db.BigInteger,primary_key=True)
    roletype = db.Column(db.String(30),unique=True)
    users = db.relationship('User',backref='role')

    def __init__(self,roletype):
        self.roletype = roletype


@app.before_first_request
def initContext():
    pass
    # app.config['username'] = 'allen'
    # app.config['password'] = 'beta'

@app.errorhandler(500)
def errorHandler(e):
    return render_template('/error.html')

@app.errorhandler(404)
def errorHandler(e):
    return render_template('/404.html')

@app.route("/")
def index():
    return render_template('/index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username = request.form.get('username',None)).first()
        if user is None or user.username is None :
            return render_template("/login.html")
        if user.password == request.form.get('password',None):
            session['user'] = request.form.get('username')
            logging.debug('username:%s,password:%s' % (request.form.get('username', None), request.form.get('password', None)))
            return render_template('/manager.html')
    return render_template("/login.html")


if __name__ == '__main__':
    app.secret_key = 'hard to guess'
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run()