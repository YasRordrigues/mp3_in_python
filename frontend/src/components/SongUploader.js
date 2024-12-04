import React, { useState } from "react";
import axios from "axios";

const SongUploader = ({ onUploadComplete }) => {
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState("");

  const handleFileChange = (event) => {
    setFiles(event.target.files); // Define os arquivos selecionados
  };

  const handleUpload = async () => {
    if (!files || files.length === 0) {
      setStatus("Please select at least one file.");
      return;
    }

    const formData = new FormData();
    Array.from(files).forEach((file) => formData.append("files", file)); // Adiciona todos os arquivos ao FormData

    try {
      const response = await axios.post("http://127.0.0.1:8000/music/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setStatus(response.data.message || "Files uploaded successfully!");
      if (onUploadComplete) onUploadComplete(); // Atualiza a lista de músicas no frontend após o upload
    } catch (error) {
      setStatus(error.response?.data?.detail || "Error uploading files.");
    }
  };

  return (
    <div style={{ marginTop: "20px", textAlign: "center" }}>
      <h2>Upload Songs</h2>
      <input type="file" multiple onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ margin: "10px" }}>
        Upload
      </button>
      <p>Status: {status}</p>
    </div>
  );
};

export default SongUploader;
