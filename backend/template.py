html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Person Detection Test</title>
</head>
<body>
    <h1>Person Detection Results:</h1>
    <div id="detectionResult"></div>
    <img id="streamedImage" src="#" alt="Streamed Image" width="640" height="480">
    <button onclick="toggleConnection()">Toggle Connection</button>

    <script>
        let socket;
        let isConnected = false;

        function toggleConnection() {
            if (isConnected) {
                socket.close();
                isConnected = false;
            } else {
                socket = new WebSocket('ws://localhost:8000/api/v1/exercise/ws'); // Change the URL accordingly
                socket.onopen = () => {
                    console.log('WebSocket connection established.');
                    isConnected = true;
                };

                socket.onmessage = (event) => {
                    const imageData = event.data;
                    const streamedImageElement = document.getElementById('streamedImage');
                    streamedImageElement.src = "data:image/jpeg;base64," + imageData;
                };
            }
        }
    </script>
</body>
</html>
"""