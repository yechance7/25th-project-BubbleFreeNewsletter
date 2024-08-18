// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import SearchBar from './components/SearchBar';
import HomePage from './pages/HomePage';
import MyPage from './pages/MyPage';
import './App.css';

const App = () => {
    return (
        <Router>
            <div className="App">
                <nav>
                    <ul>
                        <li><Link to="/">Main Page</Link></li>
                        <li><Link to="/mypage">My Page</Link></li>
                    </ul>
                </nav>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/mypage" element={<MyPage />} />
                </Routes>
                <SearchBar />
            </div>
        </Router>
    );
};

export default App;
