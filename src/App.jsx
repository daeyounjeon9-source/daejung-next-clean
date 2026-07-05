import { useState } from "react";
import { auth, provider } from "./firebase";
import { signInWithPopup, signOut } from "firebase/auth";

export default function App() {
  const [user, setUser] = useState(null);

  const login = async () => {
    const result = await signInWithPopup(auth, provider);
    setUser(result.user);
  };

  const logout = async () => {
    await signOut(auth);
    setUser(null);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>쇼핑몰</h1>

      {user ? (
        <div>
          <p>{user.displayName}</p>
          <img src={user.photoURL} width="50" />
          <br />
          <button onClick={logout}>로그아웃</button>
        </div>
      ) : (
        <button onClick={login}>Google 로그인</button>
      )}
    </div>
  );
}