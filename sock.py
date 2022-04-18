from routes import app
from main import SocketIO


'''the scoketio init'''
socketio = SocketIO(app,async_mode=None)



###############socket###########
users = {}


# connected
@socketio.on('connected')
def connect(data):
    print(data)


#disconnected
@socketio.on('disconnect')
def disconnected(data_):
    print(data_)
    socketio.on('disconnect',data_)
