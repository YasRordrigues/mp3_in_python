import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/MusicPlayer.css"; // Importando estilos CSS
import SongUploader from "./SongUploader";

const MusicPlayer = () => {
  const [songs, setSongs] = useState([]);
  const [selectedSong, setSelectedSong] = useState("");
  const [status, setStatus] = useState("");
  const [volume, setVolume] = useState(0.5);
  const [progress, setProgress] = useState(0); // Barra de progresso
  const [isPaused, setIsPaused] = useState(true); // Estado para gerenciar pausa

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
      const response = await axios.post("http://127.0.0.1:8000/music/play/", {
        song_name: selectedSong,
      });
      setStatus(response.data.message || "Song is playing.");
      setProgress(10); // Simula progresso inicial
      setIsPaused(false); // Define o estado como "reproduzindo"
    } catch (error) {
      setStatus(error.response?.data?.detail || "Error playing song.");
    }
  };

  const handlePause = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/music/pause/");
      setStatus(response.data.message);
      setIsPaused(true); // Define o estado como "pausado"
    } catch (error) {
      setStatus(error.response?.data?.detail || "Error pausing song.");
    }
  };

  const togglePlayPause = async () => {
    if (isPaused) {
      await handlePlay(); // Reproduz ou retoma
    } else {
      await handlePause(); // Pausa
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
    <div className="music-player">
      <h1>MP3 Player</h1>

      <div className="player-display">
        <h3>Now Playing:</h3>
        <p className="song-title">{selectedSong || "Select a song"}</p>
        <div className="progress-bar">
          <div className="progress" style={{ width: `${progress}%` }}></div>
        </div>
      </div>

      <div className="controls">
        <select
          value={selectedSong}
          onChange={(e) => setSelectedSong(e.target.value)}
          className="song-selector"
        >
          <option value="">Select a song</option>
          {songs.map((song, index) => (
            <option key={index} value={song}>
              {song}
            </option>
          ))}
        </select>
        <button onClick={togglePlayPause} className="btn">
          {isPaused ? "▶ Play" : "⏸ Pause"}
        </button>
      </div>

      <div className="volume-control">
        <h3>Volume</h3>
        <input
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={volume}
          onChange={handleVolumeSlider}
          className="volume-slider"
        />
        <p>{(volume * 100).toFixed(0)}%</p>
      </div>

      <SongUploader onUploadComplete={fetchSongs} />

      <div className={`status ${status.includes("Error") ? "error" : "success"}`}>
        {status}
      </div>
    </div>
  );
};

export default MusicPlayer;
