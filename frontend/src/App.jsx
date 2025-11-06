import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Questionnaire from './components/Questionnaire';
import Report from './components/Report';

function App() {
  return (
    <Router>
      <div className="min-h-screen">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/questionnaire" element={<Questionnaire />} />
          <Route path="/report/:reportId" element={<Report />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
