
from .. import create_app
from ..views.blogblue import blog

app = create_app('dev')

app.register_blueprint(blog)

@app.before_first_request
def initContext():
    pass

def run():
    app.secret_key = 'hard to guess'
    app.run()