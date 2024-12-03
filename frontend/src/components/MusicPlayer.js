import React, { useState } from "react";
import axios from "axios";

const MusicPlayer = () => {
  const [songPath, setSongPath] = useState("");
  const [status, setStatus] = useState(""); // Apenas string para mensagem
  const [volume, setVolume] = useState(0.5);

  const handlePlay = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/music/play/", {
        path: songPath,
      });
      setStatus(response.data.message);
    } catch (error) {
      setStatus(error.response?.data?.detail || "Error playing song.");
    }
  };

  const handlePause = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/music/pause/");
      setStatus(response.data.message);
    } catch (error) {
      setStatus(error.response?.data?.detail || "Error pausing song.");
    }
  };

  const handleResume = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/music/resume/");
      setStatus(response.data.message);
    } catch (error) {
      setStatus(error.response?.data?.detail || "Error resuming song.");
    }
  };

  const handleVolumeChange = async (type) => {
    try {
      const endpoint =
        type === "increase"
          ? "http://127.0.0.1:8000/music/volume/increase/"
          : "http://127.0.0.1:8000/music/volume/decrease/";
      const response = await axios.post(endpoint);
      setVolume(response.data.volume); // Atualiza apenas o volume
      setStatus(response.data.message);
    } catch (error) {
      setStatus(error.response?.data?.detail || "Error adjusting volume.");
    }
  };

  const handleVolumeSlider = async (event) => {
    const newVolume = parseFloat(event.target.value);
    try {
      const response = await axios.post("http://127.0.0.1:8000/music/volume/set/", {
        volume: newVolume,
      });
      setVolume(response.data.volume);
      setStatus(response.data.message);
    } catch (error) {
      setStatus(error.response?.data?.detail || "Error adjusting volume.");
    }
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h1>Music Player</h1>
      <input
        type="text"
        value={songPath}
        placeholder="Enter the path to the song"
        onChange={(e) => setSongPath(e.target.value)}
        style={{ width: "80%", padding: "10px", marginBottom: "10px" }}
      />
      <div>
        <button onClick={handlePlay} style={{ margin: "5px" }}>
          Play
        </button>
        <button onClick={handlePause} style={{ margin: "5px" }}>
          Pause
        </button>
        <button onClick={handleResume} style={{ margin: "5px" }}>
          Resume
        </button>
      </div>
      <div style={{ marginTop: "20px" }}>
        <h3>Volume</h3>
        <button
          onClick={() => handleVolumeChange("decrease")}
          style={{ margin: "5px" }}
        >
          -
        </button>
        <input
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={volume}
          onChange={handleVolumeSlider}
          style={{ margin: "0 10px" }}
        />
        <button
          onClick={() => handleVolumeChange("increase")}
          style={{ margin: "5px" }}
        >
          +
        </button>
        <p>Volume: {volume}</p>
      </div>
      <p>Status: {status}</p>
    </div>
  );
};

export default MusicPlayer;
