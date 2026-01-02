import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { GameProvider } from './context/GameContext';
import Home from './pages/Home';
import ConfigPage from './pages/ConfigPage';
import Activity1 from './pages/Activity1';
import Activity2 from './pages/Activity2';
import ImageVerifier from './pages/ImageVerifier';

function App() {
  return (
    <GameProvider>
      <Router>
        <div className="app-container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/config/:activityId" element={<ConfigPage />} />
            <Route path="/activity1" element={<Activity1 />} />
            <Route path="/activity2" element={<Activity2 />} />
            <Route path="/verify" element={<ImageVerifier />} />
          </Routes>
        </div>
      </Router>
    </GameProvider>
  );
}

export default App;
