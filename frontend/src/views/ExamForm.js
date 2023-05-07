import React, { useState, useEffect, useRef } from 'react';
import { useContext } from 'react';
import AuthContext from '../context/AuthContext';
import './styles/ExamForm.css';
import Navbar from '../components/Navbar';
import TestRules from './testRules';
const ExamForm = () => {
    const handleNextQuestion = () => {
        setCurrentQuestion((prevQuestion) => prevQuestion + 1);
    };

    const handlePreviousQuestion = () => {
        setCurrentQuestion((prevQuestion) => prevQuestion - 1);
    };
    const [proctoringStarted, setProctoringStarted] = useState(false);
    const mediaStreamRef = useRef(null);
    const videoRef = useRef(null);

    useEffect(() => {
        if (proctoringStarted) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then((stream) => {
                    mediaStreamRef.current = stream;
                    if (videoRef.current) {
                        videoRef.current.srcObject = stream;
                        videoRef.current.play();
                    }
                })
                .catch((error) => {
                    console.error('Error accessing webcam:', error);
                });
        } else {
            // Stop capturing webcam feed
            if (mediaStreamRef.current) {
                const tracks = mediaStreamRef.current.getTracks();
                tracks.forEach((track) => track.stop());
            }
        }
    }, [proctoringStarted]);

    const startProctoring = () => {
        const confirmed = window.confirm('Are you sure you want to start the exam?');
        if (confirmed) {
            setProctoringStarted(true);
            setTimeRemaining(60 * 60);
        }
    };


    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState({});
    const [examEnded, setExamEnded] = useState(false);
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [timeRemaining, setTimeRemaining] = useState(0);
    const [examSubmitted, setexamSubmitted] = useState(false);

    const [score, setScore] = useState(0);
    const { user, logoutUser } = useContext(AuthContext);

    useEffect(() => {
        const fetchQuestions = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/exam-questions/');
                const data = await response.json();
                setQuestions(data);
                console.log(data);
            } catch (error) {
                console.error('Error fetching exam questions:', error);
            }
        };

        fetchQuestions();
    }, []);

    const handleAnswerChange = (questionId, answer) => {
        setAnswers((prevAnswers) => ({
            ...prevAnswers,
            [questionId]: answer,
        }));
    };

    const handleSubmit = (e) => {
        const submitconfirmed = window.confirm('Are you sure you want to submit?');
        if (submitconfirmed) {
            e.preventDefault();
            const submissionData = {
                ...answers,
                // Send the answers object directly as the request body
            };
            fetch('http://localhost:8000/api/submit-exam/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(submissionData),
            })
                .then((response) => response.json())
                .then((data) => {
                    // Handle the result
                    console.log('Score:', data.score);
                    setScore(data.score);
                    handleEndExam(); // End the exam and proctoring together
                })
                .catch((error) => {
                    console.error('Error submitting exam:', error);
                });
            setexamSubmitted(true);
            setExamEnded(true);
            console.log(examEnded);
            setProctoringStarted(false);
        }
    };
    useEffect(() => {
        // Automatically submit the exam when the timer ends
        if (timeRemaining === 0 && proctoringStarted) {
            handleSubmit(); // Call the handleSubmit function to submit the exam
        }
    }, [timeRemaining, proctoringStarted]);

    useEffect(() => {
        // Start the timer when proctoring starts
        if (proctoringStarted) {
            const timer = setInterval(() => {
                setTimeRemaining((prevTime) => prevTime - 1);
            }, 1000);

            return () => {
                // Clean up the timer when proctoring ends or component unmounts
                clearInterval(timer);
            };
        }
    }, [proctoringStarted]);
    const handleEndExam = () => {

        fetch('http://localhost:8000/api/end-exam/', {
            method: 'POST',
        })
            .then((response) => response.json())
            .then((data) => {
                // Handle the response from the backend
                console.log('Exam ended:', data.message);
            });
        stopProctoring();
        console.log('Proctoring ended');
    };

    const stopProctoring = () => {
        // Stop capturing webcam feed
        if (mediaStreamRef.current) {
            const tracks = mediaStreamRef.current.getTracks();
            tracks.forEach((track) => track.stop());
            console.log("entered track stop")
        }

        // Add any additional logic to stop the proctoring process

        setProctoringStarted(false); // Set proctoringStarted state to false
    };

    const formatTime = (timeInSeconds) => {
        const hours = Math.floor(timeInSeconds / 3600);
        const minutes = Math.floor((timeInSeconds % 3600) / 60);
        const seconds = timeInSeconds % 60;

        const formattedHours = hours.toString().padStart(2, '0');
        const formattedMinutes = minutes.toString().padStart(2, '0');
        const formattedSeconds = seconds.toString().padStart(2, '0');

        return `${formattedHours}:${formattedMinutes}:${formattedSeconds}`;
    };



    const handleQuestionClick = (index) => {
        setCurrentQuestion(index);
    };
    return (

        <div className="container">


            {!examSubmitted ? (<>
                {!proctoringStarted && !examEnded ? (
                    <div className="start-exam-container">
                        <button type="button" className="start-exam-button" onClick={startProctoring}>
                            Start Exam
                        </button>

                        <TestRules />
                    </div>
                ) : (

                    <><div className='timer-row'>


                        <div className="timer">Time Remaining: {formatTime(timeRemaining)}</div>

                    </div>
                        <Navbar startProctoring={startProctoring} />
                        <div className="wrapper">

                            {/* Question column */}
                            <div className="question-column sidebar">
                                <h3 className='sidebar-title'>Questions</h3>
                                <br></br>
                                <div className="question-buttons">
                                    {/* Question buttons */}
                                    {questions.map((question, index) => (
                                        <button
                                            key={question.id}
                                            className={`question-button ${currentQuestion === index ? 'active' : ''}`}
                                            onClick={() => handleQuestionClick(index)}
                                        >
                                            {index + 1}
                                        </button>
                                    ))}
                                </div>
                                {proctoringStarted && (
                                    <div>
                                        <video ref={videoRef} autoPlay playsInline class="webcam-video" />
                                        {/* {console.log(proctoringStarted)} */}
                                    </div>
                                )}
                            </div>



                            {/* Question display */}
                            <div className="question-column">

                                {questions.length > 0 ? (
                                    <div className="question-container">
                                        {/* Display current question */}
                                        <h4 className="question-text">Q{`${currentQuestion + 1}. ${questions[currentQuestion].question_text}`}</h4>
                                        <ul className="options-list">
                                            {/* Display question options */}
                                            <li>
                                                <label>
                                                    <input
                                                        type="radio"
                                                        name={`answer-${questions[currentQuestion].id}`}
                                                        value={questions[currentQuestion].option1}
                                                        onChange={() => handleAnswerChange(questions[currentQuestion].id, questions[currentQuestion].option1)}
                                                        checked={answers[questions[currentQuestion].id] === questions[currentQuestion].option1}
                                                    />
                                                    {questions[currentQuestion].option1}
                                                </label>
                                            </li>
                                            <li>
                                                <label>
                                                    <input
                                                        type="radio"
                                                        name={`answer-${questions[currentQuestion].id}`}
                                                        value={questions[currentQuestion].option2}
                                                        onChange={() => handleAnswerChange(questions[currentQuestion].id, questions[currentQuestion].option2)}
                                                        checked={answers[questions[currentQuestion].id] === questions[currentQuestion].option2}
                                                    />
                                                    {questions[currentQuestion].option2}
                                                </label>
                                            </li>
                                            <li>
                                                <label>
                                                    <input
                                                        type="radio"
                                                        name={`answer-${questions[currentQuestion].id}`}
                                                        value={questions[currentQuestion].option3}
                                                        onChange={() => handleAnswerChange(questions[currentQuestion].id, questions[currentQuestion].option3)}
                                                        checked={answers[questions[currentQuestion].id] === questions[currentQuestion].option3}
                                                    />
                                                    {questions[currentQuestion].option3}
                                                </label>
                                            </li>
                                            <li>
                                                <label>
                                                    <input
                                                        type="radio"
                                                        name={`answer-${questions[currentQuestion].id}`}
                                                        value={questions[currentQuestion].option4}
                                                        onChange={() => handleAnswerChange(questions[currentQuestion].id, questions[currentQuestion].option4)}
                                                        checked={answers[questions[currentQuestion].id] === questions[currentQuestion].option4}
                                                    />
                                                    {questions[currentQuestion].option4}
                                                </label>
                                            </li>
                                        </ul>
                                        <div className="navigation-buttons">
                                            <button
                                                type="button"
                                                className="previous-button"
                                                onClick={handlePreviousQuestion}
                                                disabled={currentQuestion === 0}
                                            >
                                                Previous
                                            </button>&nbsp;&nbsp;
                                            <button
                                                type="button"
                                                className="next-button"
                                                onClick={handleNextQuestion}
                                                disabled={currentQuestion === questions.length - 1}
                                            >
                                                Next
                                            </button>
                                        </div>




                                    </div>

                                ) : (
                                    <div>Loading questions...</div>
                                )}
                            </div>

                        </div>

                        {/* Submit button */}
                        <div className="submit-container">
                            <button type="submit" className="submit-button" onClick={handleSubmit}>
                                Submit
                            </button>
                        </div>
                    </>
                )}

            </>
            ) : (
                <>{!proctoringStarted && examEnded && examSubmitted ? (
                    <div className="exam-ended-container">
                        <h2>Exam Ended</h2>
                        <p>Score: {score}</p>
                        <button
                            className="end-exam-button"
                            onClick={() => {
                                handleEndExam();
                                logoutUser();
                            }}
                        >
                            End Exam
                        </button>
                    </div>
                ) : null}</>
            )}


        </div>
    );

}
export default ExamForm;