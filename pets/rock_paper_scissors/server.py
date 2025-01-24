import os
import json
import random
import wifi
import socketpool
import microcontroller
import storage
from adafruit_httpserver import Server, Request, Response, FileResponse, JSONResponse
from adafruit_httpserver.mime_types import MIMETypes

WIFI_SSID = "RockPaperScissors"

# Game state
class GameRoom:
    def __init__(self, room_id):
        self.id = room_id
        self.players = {}
        self.rounds_played = 0

class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.choice = None
        self.score = 0

active_rooms = {}

print("Creating AP...")
wifi.radio.start_ap(ssid=WIFI_SSID)
print(f"AP created, IP: {wifi.radio.ipv4_address}")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

def generate_id(length=6):
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(chars) for _ in range(length))

@server.route("/")
def base(request: Request):
    return FileResponse(request, "index.html", "/www")

@server.route("/create_room", "POST")
def create_room(request: Request):
    try:
        form_data = request.form_data
        player_name = form_data.get('player_name', 'Player 1')
        
        room_id = generate_id()
        player_id = generate_id(4)
        
        room = GameRoom(room_id)
        room.players[player_id] = Player(player_id, player_name)
        active_rooms[room_id] = room
        
        return JSONResponse(request, {"room_id": room_id, "player_id": player_id})
    except Exception as e:
        return JSONResponse(request, {"error": str(e)}, status_code=500)

@server.route("/join_room", "POST")
def join_room(request: Request):
    try:
        form_data = request.form_data
        room_id = form_data.get('room_id')
        player_name = form_data.get('player_name', 'Player 2')
        
        if room_id not in active_rooms:
            return JSONResponse(request, {"error": "Room not found"}, status_code=404)
        
        room = active_rooms[room_id]
        if len(room.players) >= 2:
            return JSONResponse(request, {"error": "Room is full"}, status_code=400)
        
        player_id = generate_id(4)
        room.players[player_id] = Player(player_id, player_name)
        
        return JSONResponse(request, {"room_id": room_id, "player_id": player_id})
    except Exception as e:
        return JSONResponse(request, {"error": str(e)}, status_code=500)

@server.route("/room/<room_id>")
def get_room(request: Request, room_id):
    try:
        if room_id not in active_rooms:
            return JSONResponse(request, {"error": "Room not found"}, status_code=404)
        
        room = active_rooms[room_id]
        return JSONResponse(request, {
            "id": room.id,
            "rounds_played": room.rounds_played,
            "players": {
                p.id: {
                    "name": p.name,
                    "score": p.score,
                    "has_chosen": p.choice is not None
                } for p in room.players.values()
            }
        })
    except Exception as e:
        return JSONResponse(request, {"error": str(e)}, status_code=500)

@server.route("/make_move", "POST")
def make_move(request: Request):
    try:
        data = json.loads(request.body)
        room_id = data.get('room_id')
        player_id = data.get('player_id')
        choice = data.get('choice')
        
        if room_id not in active_rooms:
            return JSONResponse(request, {"error": "Room not found"}, status_code=404)
        
        room = active_rooms[room_id]
        if player_id not in room.players:
            return JSONResponse(request, {"error": "Player not found"}, status_code=404)
        
        player = room.players[player_id]
        player.choice = choice
        
        choices = [p.choice for p in room.players.values()]
        if None not in choices and len(choices) == 2:
            determine_winner(room)
            room.rounds_played += 1
            for p in room.players.values():
                p.choice = None
            
            return JSONResponse(request, {
                "round_complete": True,
                "players": {
                    p.id: {
                        "name": p.name,
                        "score": p.score,
                        "choice": choices[i]
                    } for i, p in enumerate(room.players.values())
                },
                "round": room.rounds_played
            })
        
        return JSONResponse(request, {"message": "Move recorded"})
    except Exception as e:
        return JSONResponse(request, {"error": str(e)}, status_code=500)

def determine_winner(room):
    players = list(room.players.values())
    choices = [p.choice for p in players]
    
    if choices[0] == choices[1]:
        return  # Tie
        
    winning_moves = {
        'rock': 'scissors',
        'paper': 'rock',
        'scissors': 'paper'
    }
    
    if winning_moves[choices[0]] == choices[1]:
        players[0].score += 1
    else:
        players[1].score += 1