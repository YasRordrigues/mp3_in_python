import React, { useState } from 'react';
import axios from 'axios';

const SongUploader = () => {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setStatus('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/music/play/upload/',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      // Atualiza o estado com a mensagem do backend
      setStatus(response.data.message || 'File uploaded and playing!');
    } catch (error) {
      // Exibe mensagem de erro
      setStatus(error.response?.data?.detail || 'Error uploading file.');
    }
  };

  return (
    <div style={{ marginTop: '20px', textAlign: 'center' }}>
      <h2>Upload a Song</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ margin: '10px' }}>
        Upload
      </button>
      <p>Status: {status}</p>
    </div>
  );
};

export default SongUploader;
