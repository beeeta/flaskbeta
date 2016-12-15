# from fk import db
#
#
# class User(db.Model):
#     __tablename__ = 't_users'
#     id = db.Column(db.BigInteger,primary_key=True)
#     username = db.Column(db.String(255),unique=True)
#     password = db.Column(db.String(255))
#     roleid = db.Column(db.BigInteger,db.ForeignKey('t_roles.id'))
#
#     def __init__(self,username,password,roleid):
#         self.username = username
#         self.password = password
#         self.roleid = roleid
#
#     # def __repr__(self):
#     #     return '<User %s>' % self.username+','+self.password+','+self.roleid
#
# class Role(db.Model):
#     __tablename__='t_roles'
#     id = db.Column(db.BigInteger,primary_key=True)
#     roletype = db.Column(db.String(30),unique=True)
#     users = db.relationship('User',backref='role')
#
#     def __init__(self,roletype):
#         self.roletype = roletype
#
#     # def __repr__(self):
#     #     return '<Role %r>' % self.roletype