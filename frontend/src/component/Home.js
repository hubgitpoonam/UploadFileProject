// src/components/Home.js
import React, { useState } from 'react';
import axios from 'axios';
import './Home.css'; // Import CSS file for styling

const Home = () => {
    const [files, setFiles] = useState([]);
    const [progress, setProgress] = useState({});
    const [errorMessage, setErrorMessage] = useState('');

    const handleFileChange = (event) => {
        const selectedFiles = event.target.files;
        let validFiles = [];
        let invalidFiles = [];

        // Validate file size
        Array.from(selectedFiles).forEach(file => {
            if (file.size <= 20 * 1024 * 1024) {
                validFiles.push(file);
            } else {
                invalidFiles.push(file.name);
            }
        });

        // Set valid files to state and show error message for invalid files
        setFiles(validFiles);
        if (invalidFiles.length > 0) {
            setErrorMessage(`Files ${invalidFiles.join(', ')} are larger than 20MB and cannot be uploaded.`);
        } else {
            setErrorMessage('');
        }
    };

    const uploadFiles = () => {
        if (files.length === 0) {
            alert('Please select files to upload.');
            return;
        }

        const formData = new FormData();
        files.forEach(file => {
            formData.append('file', file);
        });

        axios.post(`${process.env.REACT_APP_API_URL}/api/upload/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: (progressEvent) => {
                const { name } = files[0]; // Assuming you want to track progress of the first file
                const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                setProgress(prevProgress => ({
                    ...prevProgress,
                    [name]: percentCompleted
                }));
            }
        }).then(response => {
            console.log('Files uploaded:', response.data);
            // Clear files and progress after successful upload
            setFiles([]);
            setProgress({});
        }).catch(error => {
            console.error('Error uploading files:', error);
        });
    };

    return (
        <div className="container">
            <input type="file" multiple onChange={handleFileChange} />
            <button className="upload-btn" onClick={uploadFiles}>Upload Files</button>
            {errorMessage && (
                <div className="error-message">{errorMessage}</div>
            )}
            {files.length > 0 && (
                <div className="progress-container">
                    <h3>Upload Progress</h3>
                    {Array.from(files).map(file => (
                        <div key={file.name} className="file-progress">
                            <p>{file.name}</p>
                            <progress value={progress[file.name] || 0} max="100" />
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Home;
