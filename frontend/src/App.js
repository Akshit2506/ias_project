import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/student/login" element={<Login />} />
                <Route path="/student/dashboard" element={<h2>Welcome to Dashboard</h2>} />
            </Routes>
        </Router>
    );
}

export default App;
