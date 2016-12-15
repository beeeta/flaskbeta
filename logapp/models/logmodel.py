from .. import db

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