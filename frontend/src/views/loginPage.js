import { useContext } from "react";
import AuthContext from "../context/AuthContext";
import './styles/loginPage.css';

const LoginPage = () => {
  const { loginUser } = useContext(AuthContext);
  const handleSubmit = e => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;
    username.length > 0 && loginUser(username, password);
  };

  return (
    <section className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h1 className="login-title">Login</h1>
        <hr className="login-hr" />
        <label className="login-label" htmlFor="username">Username</label>
        <input className="login-input" type="text" id="username" placeholder="Enter Username" />
        <label className="login-label" htmlFor="password">Password</label>
        <input className="login-input" type="password" id="password" placeholder="Enter Password" />
        <button className="login-button" type="submit">Login</button>
      </form>
    </section>
  );
};

export default LoginPage;
