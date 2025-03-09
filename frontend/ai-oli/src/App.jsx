import React, { useRef, useState } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer'; 
import Home from '../components/Home';
import Upload from '../components/Upload'; 
import cameraIcon from './assets/camera_icon.png'; // Import the camera icon
import './App.css';

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);
  const [cameraOpen, setCameraOpen] = useState(false);
  const [capturedPhoto, setCapturedPhoto] = useState(null);
  const navigate = useNavigate();

  const openCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.onloadedmetadata = () => {
          videoRef.current.play();
        };
      }
      setCameraOpen(true);
    } catch (err) {
      console.error("Error accessing the camera: ", err);
      setCameraOpen(true); // Still set cameraOpen to true to display the black screen
    }
  };

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

  const handleSubmit = () => {
    // Handle the submission logic here
    console.log('Photo submitted:', capturedPhoto);
    setCapturedPhoto(null);
    setCameraOpen(false);
    navigate('/');
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <Header />
      <main className="flex-grow p-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
        </Routes>
        <div className="text-center mt-2 flex justify-center space-x-4">
          <button
            onClick={handleUploadClick}
            className="bg-blue-500 text-white px-4 py-2 rounded shadow hover:bg-blue-600"
          >
            Upload
          </button>
          <button
            onClick={openCamera}
            className="bg-green-500 text-white px-4 py-2 rounded shadow hover:bg-green-600"
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
        {capturedPhoto && (
          <div className="mt-4 flex flex-col items-center">
            <img src={capturedPhoto} alt="Captured" className="border border-gray-300 rounded-lg" width="640" height="480" />
            <div className="mt-4 flex space-x-4">
              <button
                onClick={handleSubmit}
                className="bg-blue-500 text-white px-4 py-2 rounded shadow hover:bg-blue-600"
              >
                Submit
              </button>
              <button
                onClick={handleCancel}
                className="bg-red-500 text-white px-4 py-2 rounded shadow hover:bg-red-600"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
        <div className="hidden">
          <canvas ref={canvasRef} width="640" height="480" className="hidden" />
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default App;
