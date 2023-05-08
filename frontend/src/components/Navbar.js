import { useContext } from "react";
import { Link } from "react-router-dom";
import AuthContext from "../context/AuthContext";

import "../views/styles/Navbar.css"; // Import the CSS file for styling
import ExamForm from "../views/ExamForm";
const Navbar = ({ startProctoring }) => {
  const { user, logoutUser } = useContext(AuthContext);

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <h1 className="navbar-logo">Examination System</h1>
        <div className="navbar-links">
          {user ? (
            <>

              {/* <Link to="/protected" className="navbar-link">Protected Page</Link> */}
              {startProctoring ? (
                <>
                  <button onClick={logoutUser} className="" disabled={true}>Exam in progress</button>

                </>
              ) : (
                <>
                  <Link to="/" className="navbar-link">Home</Link>
                  <button onClick={logoutUser} className="navbar-button">Logout</button>
                </>
              )}


            </>
          ) : (
            <>
              <Link to="/login" className="navbar-button">Login</Link>
              &nbsp;&nbsp;&nbsp;
              <Link to="/register" className="navbar-button">Register</Link>

            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
