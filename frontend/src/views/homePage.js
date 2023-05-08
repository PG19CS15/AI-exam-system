import { useContext } from "react";
import { useHistory } from "react-router-dom";
import Navbar from "../components/Navbar";
import UserInfo from "../components/UserInfo";
import AuthContext from "../context/AuthContext";
import "./styles/Home.css"; // Import the CSS file for styling
const Home = () => {
  const history = useHistory();
  const { user } = useContext(AuthContext);

  const handleStartExam = () => {
    history.push('/exam');
  };

  return (
    <div className="home-container">
      <Navbar startProctoring={false} />
      <div className="home-content">
        {user ? (
          <>
            <h1 className="welcome-message">
              Welcome to the Home Page <UserInfo user={user} />
            </h1>
            <button className="start-button" onClick={handleStartExam}>
              Start Exam
            </button>
          </>
        ) : (
          <h1 className="login-message">Please log in to start the exam.</h1>
        )}
      </div>
    </div>
  );
};

export default Home;
