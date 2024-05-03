html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image and Text WebSocket Example</title>
    <style>
        #result img {
            width: 640px;
            height: 480px;
        }
    </style>
</head>
<body>
    <h1>Image and Text WebSocket Example</h1>
    <div id="result"></div>
    <button id="toggleButton">Toggle WebSocket Connection</button>

    <script>
        let socket;

        document.getElementById('toggleButton').addEventListener('click', () => {
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.close();
                console.log('WebSocket connection closed.');
            } else {
                socket = new WebSocket('ws://localhost:8000/api/v1/exercise/ws');
                socket.onopen = () => {
                    console.log('WebSocket connection established.');
                };
                socket.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    const imageSrc = data.frame;
                    const textMessage = data.message;

                    // Replace the existing content of the result div
                    document.getElementById('result').innerHTML = '';

                    // Display the image
                    const imageElement = document.createElement('img');
                    imageElement.src = 'data:image/jpeg;base64,' + imageSrc;
                    document.getElementById('result').appendChild(imageElement);

                    // Display the text message
                    const textElement = document.createElement('p');
                    textElement.textContent = textMessage;
                    document.getElementById('result').appendChild(textElement);
                };
            }
        });
    </script>
</body>
</html>
"""