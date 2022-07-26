from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

# in terminal:
# pip install uvicorn[standard]
# uvicorn main:app --reload

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Задание</title>
        <style>
        li {
        list-style-type: none; 
        }
        ul {
        margin-left: 0; 
        padding-left: 0; 
        }
        </style>
    </head>
    <body>
        <h1>Сообщения</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Отправить</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var text = JSON.parse(JSON.parse(event.data)['t'])
                var number = JSON.parse(event.data)['n']
                var content = document.createTextNode(`${number} ${text}`)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(JSON.stringify(input.value))
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    num = 1
    while True:
        data = await websocket.receive_text()
        await websocket.send_json({'n': num, 't': data})
        num += 1
