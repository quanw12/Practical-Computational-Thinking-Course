// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getAnalytics } from "firebase/analytics";

// Your web app's Firebase configuration  
const firebaseConfig = {
  apiKey: "AIzaSyAjPpcNCuiU1hp4N5L_ts4ZlMfhenMbqrM",
  authDomain: "lab-62a34.firebaseapp.com",
  projectId: "lab-62a34",
  storageBucket: "lab-62a34.firebasestorage.app",
  messagingSenderId: "532797072454",
  appId: "1:532797072454:web:41b0490bfb3d3ea752d647",
  measurementId: "G-X0TK87BXQG"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();

// Cấu hình Google provider với custom parameters
googleProvider.setCustomParameters({
  'prompt': 'select_account',
  'hd': '' // Allow all domains
});

// Initialize Analytics (optional)
export const analytics = typeof window !== 'undefined' ? getAnalytics(app) : null;

export default app;