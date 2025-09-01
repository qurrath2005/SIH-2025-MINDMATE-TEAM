import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyC4D12EqgORL6Ny4gChgQNv8jih_4m8JvY",
  authDomain: "mindmate-chat.firebaseapp.com",
  projectId: "mindmate-chat",
  storageBucket: "mindmate-chat.firebasestorage.app",
  messagingSenderId: "395088269379",
  appId: "1:395088269379:web:e0e47847e5bead7f6a44f6",
  measurementId: "G-GDV60Y6XX4"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

export const db = getFirestore(app);
export const auth = getAuth(app);
