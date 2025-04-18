import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            let response = await fetch("http://127.0.0.1:8000/student/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",  // JSON data send karo
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                }),
            });

            let data = await response.json();

            if (data.message === "Login Successful") {
                navigate(data.redirect); // Redirect to dashboard
            } else {
                alert("Invalid credentials! Try again.");
            }
        } catch (error) {
            console.error("Login Error:", error);
            alert("Something went wrong! Please try again.");
        }
    };

    return (
        <div>
            <h2>Student Login</h2>
            <form onSubmit={handleSubmit}>
                <label>Username:</label>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <label>Password:</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;
