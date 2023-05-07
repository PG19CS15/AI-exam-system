import React, { useEffect, useState } from 'react';
import './styles/testRules.css'; // Import the CSS file for styling

const TestRules = () => {
    const [rules, setRules] = useState([]);

    useEffect(() => {
        fetchRules();
    }, []);

    const fetchRules = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/rules'); // Change the endpoint to match your Django backend API URL
            const data = await response.json();
            setRules(data);
        } catch (error) {
            console.log('Error fetching rules:', error);
        }
    };

    return (
        <div className="test-rules">
            <h2 className="rules-title">Rules</h2>
            <ul className="rules-list">
                {rules.map((rule, index) => (
                    <li key={index}>{rule}</li>
                ))}
            </ul>
        </div>
    );
}

export default TestRules;