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