import React, { useState, useEffect, useRef } from 'react';
import { useContext } from 'react';
import AuthContext from '../context/AuthContext';
import './styles/ExamForm.css';
import Navbar from '../components/Navbar';
import TestRules from './testRules';
const ExamForm = () => {
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState({});
    const [examEnded, setExamEnded] = useState(false);
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [timeRemaining, setTimeRemaining] = useState(0);
    const [examSubmitted, setexamSubmitted] = useState(false);
    const [score, setScore] = useState(0);
    const { user, logoutUser } = useContext(AuthContext);
    const [proctoringStarted, setProctoringStarted] = useState(false);
    const mediaStreamRef = useRef(null);
    const videoRef = useRef(null);
    const handleNextQuestion = () => {
        setCurrentQuestion((prevQuestion) => prevQuestion + 1);
    };
    const handlePreviousQuestion = () => {
        setCurrentQuestion((prevQuestion) => prevQuestion - 1);
    };
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

                    <></>
                )}

            </>
            ) : (
                <>{!proctoringStarted && examEnded && examSubmitted ? (
                    <div className="exam-ended-container">
                        
                    </div>
                ) : null}</>
            )}


        </div>
    );

}
export default ExamForm;