from flask_socketio import Namespace, emit, join_room, leave_room
from collections import defaultdict
from flask import request
import json

class Socket(Namespace):
    # holds the connectionID to callID mapping
    conn_to_call = defaultdict(lambda: None)
    # holds the connectionID to groupID mapping
    groupDictionary = defaultdict(lambda: None)
    # holds the groupID to Classroom info mapping
    groupInformation = defaultdict(lambda: {
                "can_chat": True,
                "participants": {}
            })

        
    def on_connect(self):
        print("Client has connected")

    def on_SendMute(self, call_id, group_name):
        emit("MakeMute", call_id, room=group_name)

    def on_SendUnMute(self, call_id, group_name):
        emit("MakeUnMute", call_id, room=group_name)

    def on_disconnect(self):
        print("Client has disconnected")
        call_id = Socket.conn_to_call[request.sid]
        group_name = Socket.groupDictionary[request.sid]
        if (call_id != None):
            leave_room(group_name)
            emit("UserDisconnected", call_id, room=group_name)
            
            classInfo = Socket.groupInformation[group_name]
            if (classInfo != None):
                classInfo["participants"].pop(call_id)
            emit("ClassInfo", json.dumps(classInfo["participants"]), room=group_name)

    def on_JoinRoom(self, call_id, group_name, token):
        from VirtualClassroom.models import Instructors, Students
        from flask_jwt_extended import decode_token
        res = decode_token(token)
        print(res)
        role = res["role"]
        userId = res["sub"]
        # TODO: Get role and id from token
        if role == "Instructor":
            instructor = Instructors.query.filter_by(InstructorID=userId).first()
        else:
            user = Students.query.filter_by(StudentID=userId).first()

        class_info = Socket.groupInformation[group_name]

        class_info["participants"][call_id] = {
            'UserName' : user.FirstName + " " + user.LastName,
            'Role' : role,
            'ConnectionId' : request.sid,
            'CallId' : call_id,
            'HasAudio' : True,
            'HasVideo' : True
        }
        emit("ClassInfo", json.dumps(class_info["participants"]), room=request.sid)
        print(class_info["participants"])
        print(request.sid)
        emit("UserConnected", json.dumps(class_info["participants"][call_id]), room=group_name)
        join_room(group_name)
        Socket.conn_to_call[request.sid] = call_id
        Socket.groupDictionary[request.sid] = group_name
        

    def on_ScreenShare(self, call_id, group_name):
        print("Got to screen share")
        class_info = Socket.groupInformation[group_name]

        stream_info = {
            "UserName" : "Instructor's stream}",
            "Role" : "Instructor",
            "ConnectionId" : request.sid,
            "CallId" : call_id,
            "HasAudio" : False,
            "HasVideo" : True
        }

        class_info["participants"][call_id] = stream_info
        print(class_info["participants"])        
        emit("UserConnected", json.dumps(class_info["participants"][call_id]), room=group_name)
        join_room(group_name)
        Socket.conn_to_call[request.sid] = call_id
        Socket.groupDictionary[request.sid] = group_name

    def on_my_event(self, data):
        emit('my_response', data)

def register_websocket(socket_io):
    socket_io.on_namespace(Socket())