import eventlet
eventlet.monkey_patch()

from app import app, socketio
import foody_api
# import foody_web  (may add for Google API purpose)

if __name__ == '__main__':
    socketio.run(app, debug=True)
