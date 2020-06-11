basic url:

contains main page


GET:`127.0.0.1:8000/`

**MAIN API**

Basic url: `127.0.0.1:8000/api/`

**Boards**

**Auth:**

LOGIN POST:`127.0.0.1:8000/api/login/` DATA = {"username":"","password":""}

LOGOUT POST:`127.0.0.1:8000/api/logout/`

REGISTER POST:`127.0.0.1:8000/api/registration/`DATA = {"username":"","password1":"","password1":""}

**Basic url:**

GET:`127.0.0.1:8000/api/boards/` List of all boards and their todos
GET:`127.0.0.1:8000/api/todos/` List of all todos

GET:`127.0.0.1:8000/api/boards/?type=1&board=1` List of all todos at board

GET:`127.0.0.1:8000/api/boards/?type=2&board=1` List of all todos at board with done=False

GET:`127.0.0.1:8000/api/todos/?type=1` List of all todos with done=False

POST:`127.0.0.1:8000/api/todos/` DATA = {"todos":[{"title":str,"board":board_id},...]} Create a todos

POST:`127.0.0.1:8000/api/boards/` DATA = {"names":[list of names,...]} Create a boards


PUT:`127.0.0.1:8000/api/boards/` DATA = `{"boards":[
                                        {"title":"one","id":"1"}..]
                                        } `Edit a boards



PUT:`127.0.0.1:8000/api/todos/` DATA = `{"todos":[
                                        {"title":"one","id":"1","done":true},
                                        {"title":"four","id":"3","done":true,"board":1},
                                        {"title":"six","id":"6","board":null}]
                                        }` Edit todos

DELETE:`127.0.0.1:8000/api/todos/` DATA = {"id_s":[list of ids]}

DELETE:`127.0.0.1:8000/api/boards/` DATA = {"id_s":[list of ids]}

                                        
