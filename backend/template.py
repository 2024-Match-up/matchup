html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Exercise WebSocket</title>
    </head>
    <body>
        <h1>Exercise WebSocket</h1>
        <form id="exerciseForm" onsubmit="sendExercise(event)">
            <label for="exerciseId">Exercise ID:</label>
            <input type="text" id="exerciseId" name="exerciseId" required><br><br>
            <label for="coordinates">Coordinates:</label>
            <input type="text" id="coordinates" name="coordinates" required><br><br>
            <button type="submit">Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws;
            function sendExercise(event) {
                event.preventDefault();
                var exerciseId = document.getElementById('exerciseId').value;
                var coordinates = document.getElementById('coordinates').value;
                var message = {
                    exerciseId: exerciseId,
                    coordinates: coordinates
                };
                ws.send(JSON.stringify(message));
            }

            function connectWebSocket() {
                ws = new WebSocket("ws://localhost:8000/api/v1/exercise/ws");
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                };
                ws.onopen = function(event) {
                    console.log("WebSocket connected");
                };
            }

            connectWebSocket();
        </script>
    </body>
</html>
"""