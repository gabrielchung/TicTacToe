import ttt
import json
import login

from flask import Flask, request, escape

app = Flask(__name__)

t = None
login_sys = None

def check_init():
  global t
  global login_sys
  if t is None or login_sys is None:
    return False
  else:
    return True

@app.route('/init')
def init():
  global t
  global login_sys
  t = ttt.TTT(3)
  login_sys = login.Login_Sys(2)
  return json.dumps({'result': 'OK'})

@app.route('/register')
def register():
  global login_sys
  if check_init() == False:
    return json.dumps({'result': 'Please initialize'})
  token = login_sys.register()
  player_index = login_sys.login(token)
  if token != False:
    return json.dumps({'result': 'OK', 'player': player_index, 'token': token})
  else:
    return json.dumps({'result': 'All players have registered'})

@app.route('/board')
def get_board():
  if check_init() == False:
    return json.dumps({'result': 'Please initialize'})

  global t
  if t is not None:
    return json.dumps(t.get_board())
  else:
    return json.dumps({'result': 'NOT initialized'})

@app.route('/take', methods=['GET'])
def take():
  if check_init() == False:
    return json.dumps({'result': 'Please initialize'})

  if not 'token' in request.args:
    return json.dumps({'result': 'Please supply token'})

  global login_sys
  global t
  player_index = login_sys.login(request.args['token'])

  if player_index == -1:
    return json.dumps({'result': 'Invalid token'})
  if player_index != t.whose_turn():
    return json.dumps({'result': 'It is not your turn yet'})

  if not ('x' in request.args and 'y' in request.args) :
    return json.dumps({'result': 'Please supply x and y coordinates'})
  x = int(escape(request.args['x']))
  y = int(escape(request.args['y']))
  
  if (x, y) in t.possible_moves():
    won = t.take(x, y)
    if won:
      return json.dumps({'result': 'Player ' + str(t.whose_turn()) + ' won'})
    else:
      return json.dumps({'result': 'OK'})
  else:
    return json.dumps({'result': 'Invalid move'})

@app.route('/moves')
def moves():
  if check_init() == False:
    return json.dumps({'result': 'Please initialize'})

  global t
  return json.dumps(t.possible_moves())

@app.route('/turn')
def turn():
  if check_init() == False:
    return json.dumps({'result': 'Please initialize'})

  global t
  return json.dumps(t.whose_turn())