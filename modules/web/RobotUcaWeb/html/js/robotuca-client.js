// Create a WebSocket connection
const socket = new WebSocket("ws://localhost:8080/video");

// Connection opened
socket.addEventListener("open", (event) => {
  console.log("Connected to the WebSocket server.");
  // You can send messages here, for example:
  socket.send("Hello, WebSocket!");
});

// Listen for messages
socket.addEventListener("message", (event) => {
  console.log(`Received message: ${event.data}`);
  // Handle incoming messages from the server
});

// Connection closed
socket.addEventListener("close", (event) => {
  if (event.wasClean) {
    console.log(`Connection closed cleanly, code=${event.code}, reason=${event.reason}`);
  } else {
    console.error("Connection abruptly closed");
  }
});

// Connection error
socket.addEventListener("error", (event) => {
  console.error("WebSocket error:", event);
});
