import React, { useState, useEffect } from "react";
import { db } from "./firebaseConfig";
import { collection, addDoc, query, onSnapshot, orderBy } from "firebase/firestore";
import "./Chatroom.css";

// Dummy avatars for users
const avatars = [
  "https://i.pravatar.cc/40?img=1",
  "https://i.pravatar.cc/40?img=2",
  "https://i.pravatar.cc/40?img=3",
  "https://i.pravatar.cc/40?img=4",
];

function Chatroom() {
  const [messages, setMessages] = useState([]);
  const [newMsg, setNewMsg] = useState("");

  useEffect(() => {
    const q = query(collection(db, "chatroom"), orderBy("timestamp"));
    const unsubscribe = onSnapshot(q, (snapshot) => {
      setMessages(snapshot.docs.map((doc) => doc.data()));
    });
    return () => unsubscribe();
  }, []);

  const sendMessage = async () => {
    if (newMsg.trim() === "") return;

    // Fake username + avatar for now
    const randomAvatar = avatars[Math.floor(Math.random() * avatars.length)];
    const username = "User" + Math.floor(Math.random() * 100);

    await addDoc(collection(db, "chatroom"), {
      text: newMsg,
      user: username,
      avatar: randomAvatar,
      timestamp: new Date()
    });
    setNewMsg("");
  };

  return (
    <div className="chat-container">
      <div className="chat-header">💬 MindMate Peer Chat</div>

      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div key={idx} className="chat-message">
            <img src={msg.avatar} alt="avatar" className="chat-avatar" />
            <div className="chat-bubble">
              <strong className="chat-username">{msg.user}</strong>
              <p>{msg.text}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="chat-input-container">
        <input
          type="text"
          value={newMsg}
          onChange={(e) => setNewMsg(e.target.value)}
          placeholder="Type a friendly message..."
          className="chat-input"
        />
        <button onClick={sendMessage} className="chat-button">
          ➤
        </button>
      </div>
    </div>
  );
}

export default Chatroom;
