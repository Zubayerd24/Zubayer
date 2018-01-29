#qpy:webapp:WebAppSample
#qpy://127.0.0.1:8080/
from bottle import route, run, template

@route('/')
def index():
    return template('<b>Hello {{name}}</b>!', name='QPython WebApp')

@route('/__exit')
def exit():
    import os,signal
    os.kill(os.getpid(), signal.SIGKILL)

run(host='127.0.0.1', port=8080)
