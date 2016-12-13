from flask import request,session,Flask,render_template,make_response, \
    url_for,redirect,abort,g,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# from flask_moment import Moment
import logging,markdown2
from fk_tools import blogfile_tool

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:123456@localhost/bbq'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['BLOGFILE_BASEDIR'] = 'E:\\blogfile\\'

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

class LogFile(db.Model):
    __tablename__ = 't_logfiles'
    id = db.Column(db.BigInteger,primary_key=True)
    title = db.Column(db.String(255),unique=True)
    keyword = db.Column(db.String(255))
    cturl = db.Column(db.String(255))

    def __init__(self,title,keyword,cturl):
        self.title = title
        self.keyword = keyword
        self.cturl = cturl

def query_files():
    return LogFile.query.all()

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
    files = query_files()
    prefix = 'http://test/'
    return render_template('/index.html',logfiles = files,prefix = prefix)

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username = request.form.get('username',None)).first()
        if user is None or user.username is None :
            return render_template("/login.html")
        if user.password == request.form.get('password',None):
            session['user'] = request.form.get('username')
            logging.debug('username:%s,password:%s' % (request.form.get('username', None), request.form.get('password', None)))
            return redirect(url_for('manager'))
    return render_template("/login.html")

@app.route('/addBlog',methods =['GET','POST'])
def addBlog():
    if request.method == 'GET':
        return render_template('/addblog.html')
    elif request.method == 'POST':
        title = request.form.get('blogTitle')
        content = request.form.get('blogContent')
        mkctt = markdown2.markdown(content)
        # 生成日志保存路径，将日志内容保存入文件，日志标题和路径保存如数据库
        fileName = blogfile_tool.saveBlogFile(app.config['BLOGFILE_BASEDIR'],mkctt)
        bkFile = LogFile(title,None,fileName)
        db.session.add(bkFile)
        db.session.commit()
        return redirect(url_for('manager'))

@app.route('/showLogDetail/<fileId>',methods =['GET'])
def showLogDetail(fileId):
    file = LogFile.query.filter_by(id=fileId).first()
    if file is not None:
        fileFullPath = app.config['BLOGFILE_BASEDIR'] + file.cturl
        title = file.title;
        str = list()
        with open(fileFullPath,'r') as f:
            for i in f.readlines():
                str.append(i)
        content = '\n'.join(str)
        return render_template('/blogDetail.html',title = title,content = content)
    return render_template('/404.html')


@app.route('/manager')
def manager():
    files = query_files()
    prefix = request.host_url
    return render_template('/manager.html',logfiles = files,prefix = prefix)


if __name__ == '__main__':
    app.secret_key = 'hard to guess'
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run()