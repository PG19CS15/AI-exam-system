import { useState, useContext } from "react";
import AuthContext from "../context/AuthContext";
import './styles/registerPage.css'
function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const { registerUser } = useContext(AuthContext);

  const handleSubmit = async e => {
    e.preventDefault();
    registerUser(username, password, password2);
  };

  return (
    <section className="register-container">
      <form onSubmit={handleSubmit} className="register-form">
        <h1 className="register-title">Create an account</h1>
        <hr className="register-hr" />
        <div className="register-input-container">
          <label htmlFor="username" className="register-label">Username</label>
          <input
            type="text"
            id="username"
            onChange={e => setUsername(e.target.value)}
            placeholder="Username"
            required
            className="register-input"
          />
        </div>
        <div className="register-input-container">
          <label htmlFor="password" className="register-label">Password</label>
          <input
            type="password"
            id="password"
            onChange={e => setPassword(e.target.value)}
            placeholder="Password"
            required
            className="register-input"
          />
        </div>
        <div className="register-input-container">
          <label htmlFor="confirm-password" className="register-label">Confirm Password</label>
          <input
            type="password"
            id="confirm-password"
            onChange={e => setPassword2(e.target.value)}
            placeholder="Confirm Password"
            required
            className="register-input"
          />
          <p className="register-password-error">{password2 !== password ? "Passwords do not match" : ""}</p>
        </div>
        <button className="register-button">Register</button>
      </form>
    </section>
  );
}

export default Register;