from flask import Blueprint,render_template,request,redirect,url_for,session,abort
from ..models.logmodel import User,LogFile
from ..fk_tools import blogfile_tool
from ..fk_tools.logutil import getLogger
import markdown2
from .. import db,loginManager
from ..config import Config
from flask_login import current_user,login_user,logout_user,fresh_login_required

blog = Blueprint('blog',__name__, static_folder='static',template_folder='templates')
log = getLogger()
loginManager.login_view = 'blog.login'

@loginManager.user_loader
def load_user(user_id):

    user = User.query.filter_by(id=user_id).first()
    return user

@loginManager.unauthorized_handler
def unauthorized():
    return redirect(url_for('blog.login'))

@blog.route("/")
# @cache.cached(timeout=60)
def index():
    files = query_files()
    prefix = request.host_url
    return render_template('/index.html',logfiles = files,prefix = prefix)

@blog.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username = request.form.get('username',None)).first()
        if user is None or user.username is None :
            return render_template("/login.html")
        if user.password == request.form.get('password',None):
            session['user'] = request.form.get('username')
            log.debug('username:%s,password:%s' % (request.form.get('username', None), request.form.get('password', None)))
            login_user(user)
            print('in',session)
            return redirect(url_for('blog.manager'))
    return render_template("/login.html")

@blog.route('/logout',methods=['GET'])
def logout():
    logout_user()
    print('out',session)
    return redirect(url_for('blog.index'))

@blog.route('/addBlog',methods =['GET','POST'])
def addBlog():
    if request.method == 'GET':
        return render_template('/addblog.html')
    elif request.method == 'POST':
        title = request.form.get('blogTitle')
        content = request.form.get('blogContent')
        mkctt = markdown2.markdown(content)
        # 生成日志保存路径，将日志内容保存入文件，日志标题和路径保存如数据库
        fileName = blogfile_tool.save_file(Config.BLOGFILE_BASEDIR,mkctt)
        bkFile = LogFile(title,None,fileName)
        db.session.add(bkFile)
        db.session.commit()
        return redirect(url_for('blog.manager'))
    return abort(400)

@blog.route('/showLogDetail/<fileId>',methods =['GET'])
def showLogDetail(fileId):
    file = LogFile.query.filter_by(id=fileId).first()
    if file is not None:
        fileFullPath = Config.BLOGFILE_BASEDIR + file.cturl
        title = file.title
        str = list()
        with open(fileFullPath,'r') as f:
            for i in f.readlines():
                str.append(i)
        content = '\n'.join(str)
        return render_template('/blogDetail.html',title = title,content = content)
    return render_template('/404.html')

@blog.route('/manager')
@fresh_login_required
def manager():
    files = query_files()
    prefix = request.host_url
    return render_template('/manager.html',logfiles = files,prefix = prefix)

def query_files():
    return LogFile.query.all()