
from .. import create_app
from ..views.blogblue import blog

app = create_app('dev')

app.register_blueprint(blog)

@app.before_first_request
def initContext():
    pass
    # logapp.config['username'] = 'allen'
    # logapp.config['password'] = 'beta'



def run():
    # if __name__ == '__main__':
    app.secret_key = 'hard to guess'
    # logapp.config['SESSION_TYPE'] = 'filesystem'
    # app.register_blueprint()
    app.run()