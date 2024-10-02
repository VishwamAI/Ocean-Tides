import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ChakraProvider } from '@chakra-ui/react';
import './App.css';
import LoginPage from './LoginPage';
import DashboardPage from './DashboardPage';

const Home = () => <div>Home Page</div>;

function App() {
  return (
    <ChakraProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
          </Routes>
        </div>
      </Router>
    </ChakraProvider>
  );
}

export default App;
