import React, { useRef, useState, useEffect} from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import axios from 'axios'; // Import axios
import Header from '../components/Header';
import Footer from '../components/Footer'; 
import Home from '../components/Home';
import Upload from '../components/Upload'; 
import cameraIcon from './assets/camera_icon.png'; // Import the camera icon
import logo from './assets/logo2.png'; // Import the logo
import Plot from "react-plotly.js";
import './App.css';

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);
  const [cameraOpen, setCameraOpen] = useState(false);
  const [capturedPhoto, setCapturedPhoto] = useState(null);
  const [loading, setLoading] = useState(false);
  const [figureChat, setChat] = useState(null);
  const [figureData, setPlotUrl] = useState(null);
  const navigate = useNavigate();

  // Function to open the camera
  const openCamera = async () => {
    setCameraOpen(true); // Change state to open the camera
  };

  // useEffect hook to initialize the camera stream when cameraOpen is true
  useEffect(() => {
    if (cameraOpen && videoRef.current) {
      const initializeStream = async () => {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'user' }, // User-facing camera
          });
          videoRef.current.srcObject = stream;
          videoRef.current.play();
        } catch (err) {
          console.error("Error accessing the camera: ", err);
          alert('Camera access failed. Please make sure you have granted permission.');
        }
      };

      initializeStream();
    }
  }, [cameraOpen]); // The effect runs when cameraOpen state changes


  const takePhoto = () => {
    const context = canvasRef.current.getContext('2d');
    context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
    const dataUrl = canvasRef.current.toDataURL('image/png');
    setCapturedPhoto(dataUrl); // Set the captured photo to state
  };

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setCapturedPhoto(e.target.result); // Set the uploaded photo to state
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCancel = () => {
    setCapturedPhoto(null);
    setCameraOpen(false);
    navigate('/');
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await axios.post('https://fastapi-backend-401162466994.us-central1.run.app/upload', {
        image: capturedPhoto
      });
      console.log('Photo submitted:', response);
      const data = response.data;
      console.log("data")
      console.log(data)
      // Assuming response contains a URL to the Plotly graph
      setChat(data.chat)
      setPlotUrl(data.figure); 
    } catch (error) {
      console.error('Error submitting photo:', error);
    } finally {
      setLoading(false);
      navigate('/');
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow p-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
        </Routes>
        <div className="font-custom text-center mt-2 flex justify-center space-x-4">
          <button
            onClick={handleUploadClick}
            className="bg-blue-500 text-white px-4 py-2 rounded shadow hover:bg-blue-600 font-bold"
          >
            Upload
          </button>
          <button
            onClick={openCamera}
            className="bg-green-500 text-white px-4 py-2 rounded shadow hover:bg-green-600 font-bold"
          >
            Open Camera
          </button>
          <input
            type="file"
            accept="image/*"
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
          />
        </div>
        {cameraOpen && !capturedPhoto && (
          <>
            <div className="mt-4 flex justify-center">
              <video ref={videoRef} className="border border-gray-300 rounded-lg bg-black" width="640" height="480" autoPlay />
            </div>
            <div className="mt-4 flex justify-center">
              <img
                src={cameraIcon}
                alt="Take Picture"
                onClick={takePhoto}
                className="cursor-pointer"
                style={{ width: '50px', height: '50px' }}
              />
            </div>
          </>
        )}
        {loading && (
          <div className="flex flex-col items-center justify-center mt-4">
            <img src={logo} alt="Loading" className="animate-bounce-stretch" style={{ width: '100px', height: '100px' }} />
            <p className="text-xl font-bold mt-4">Please wait... we are analyzing your meal</p>
          </div>
        )}
        {!loading && capturedPhoto && (
          <div className="mt-4 flex flex-col items-center">
            <img src={capturedPhoto} alt="Captured" className="border border-gray-300 rounded-lg" width="640" height="480" />
            <div className="mt-4 flex space-x-4">
              <button
                onClick={handleSubmit}
                className="bg-blue-500 text-white px-4 py-2 rounded shadow hover:bg-blue-600 font-bold"
              >
                Submit
              </button>
              <button
                onClick={handleCancel}
                className="bg-red-500 text-white px-4 py-2 rounded shadow hover:bg-red-600 font-bold"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
        <div className="hidden">
          <canvas ref={canvasRef} width="640" height="480" className="hidden" />
        </div>
        {figureData && (
            <div className="mt-6 flex flex-col items-center">
              {figureChat && (
                <div className="bg-white shadow-lg rounded-2xl p-6 mb-4 text-center max-w-lg">
                  <p className="text-lg font-semibold text-gray-800">{figureChat}</p>
                </div>
              )}
              <div className="w-full h-auto min-h-[400px] overflow-x-auto">
              <Plot
                data={figureData.data}
                layout={{
                  ...figureData.layout,
                  autosize: true,  // Automatically adjust the plot size based on the parent container
                  width: 420,   // Set width to 100% of the parent container
                  margin: {
                    l: 0,  // Adjust left margin to fit the plot
                    r: 50,  // Adjust right margin to fit the plot
                    t: 50,  // Optional: Adjust top margin
                    b: 50,  // Optional: Adjust bottom margin
                  },
                }}
                config={figureData.config}
              />
            </div>
            </div>
      )}
      </main>
      <Footer />
    </div>
  );
}

export default App;
