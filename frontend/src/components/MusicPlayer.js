import React, { useState, useEffect } from "react";
import axios from "axios";
import SongUploader from "./SongUploader";

const MusicPlayer = () => {
  const [songs, setSongs] = useState([]);
  const [selectedSong, setSelectedSong] = useState("");
  const [status, setStatus] = useState(""); // Para exibir mensagens
  const [volume, setVolume] = useState(0.5); // Volume inicial em 50%

  // Busca as músicas disponíveis no servidor ao carregar o componente
  useEffect(() => {
    fetchSongs();
  }, []);

  const fetchSongs = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/music/list/");
      setSongs(response.data.songs);
    } catch (error) {
      setStatus("Error fetching songs.");
    }
  };

  const handlePlay = async () => {
    if (!selectedSong) {
      setStatus("Please select a song to play.");
      return;
    }
    try {
      console.log("Selected song:", selectedSong); // Verifica o nome da música
      const response = await axios.post("http://127.0.0.1:8000/music/play/", {
        song_name: selectedSong,
      });
      console.log("Play response:", response.data); // Log para debug
      setStatus(response.data.message || "Song is playing.");
    } catch (error) {
      console.error("Error playing song:", error.response?.data); // Log detalhado
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

      {/* Lista de músicas disponíveis */}
      <h3>Available Songs</h3>
      <select
        value={selectedSong}
        onChange={(e) => setSelectedSong(e.target.value)}
        style={{ marginBottom: "10px" }}
      >
        <option value="">Select a song</option>
        {songs.map((song, index) => (
          <option key={index} value={song}>
            {song}
          </option>
        ))}
      </select>
      <button onClick={handlePlay} style={{ margin: "10px" }}>
        Play
      </button>
      <p>Status: {status}</p>

      {/* Controles de reprodução */}
      <div>
        <button onClick={handlePause} style={{ margin: "5px" }}>
          Pause
        </button>
        <button onClick={handleResume} style={{ margin: "5px" }}>
          Resume
        </button>
      </div>

      {/* Controles de volume */}
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

      {/* Componente de Upload */}
      <h3>Upload Songs</h3>
      <SongUploader onUploadComplete={fetchSongs} />
    </div>
  );
};

export default MusicPlayer;
