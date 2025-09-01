import React from "react";
import Chatroom from "./Chatroom"; // Import the Chatroom component

function App() {
  return (
    <div className="App" style={{ fontFamily: "Arial, sans-serif", padding: "20px" }}>
      <h1>MindMate 🚀</h1>
      <p>Welcome to the Peer Chatroom!</p>
      <Chatroom />  {/* Chatroom component */}
    </div>
  );
}

export default App;
