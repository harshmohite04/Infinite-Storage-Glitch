import "./App.css";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import File2video from "./Pages/file2video";
import Video2file from "./Pages/video2file";

function App() {
  return (
    <div className="container">
      <BrowserRouter>
        <nav className="tab-navigation">
          <Link to="/" className="tab">File to Video</Link>
          <Link to="/ogFile" className="tab">Video to File</Link>
        </nav>

        <div className="content">
          <Routes>
            <Route path="/" element={<File2video />} />
            <Route path="/ogFile" element={<Video2file />} />
          </Routes>
        </div>
      </BrowserRouter>
    </div>
  );
}

export default App;
