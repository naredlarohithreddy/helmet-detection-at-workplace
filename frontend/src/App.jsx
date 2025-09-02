import { useState, useRef } from 'react';
import { Upload, Shield, AlertTriangle, CheckCircle, X, Camera } from 'lucide-react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [resultImage, setResultImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (selectedFile) => {
    if (selectedFile) {
      setFile(selectedFile);
      setResultImage(null);
      setError(null);
      
      const reader = new FileReader();
      reader.onload = (e) => setPreview(e.target.result);
      reader.readAsDataURL(selectedFile);
    }
  };

  const handleInputChange = (event) => {
    handleFileChange(event.target.files[0]);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Please select an image first.");
      return;
    }

    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try { 
      const apiUrl = "https://hardhat-detection-backend.onrender.com";
      const response = await fetch(`${apiUrl}/predict`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to analyze image. Please try again.");
      }

      const data = await response.json();
      setResultImage(data.annotated_image);

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const clearSelection = () => {
    setFile(null);
    setPreview(null);
    setResultImage(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="app-container">
      <div className="main-wrapper">
        {}
        <div className="header">
          <div className="header-icon-title">
            <div className="header-icon">
              <Shield className="icon-large" />
            </div>
            <h1 className="main-title">
              Hard Hat Safety Detection
            </h1>
          </div>
          <p className="header-description">
            AI-powered safety compliance monitoring. Upload workplace images to automatically detect 
            and verify hard hat usage across your construction sites.
          </p>
        </div>

        {/* Main Card */}
        <div className="main-card">
          {/* Upload Section */}
          <div className="upload-section">
            <div className="upload-form">
              {/* Drag & Drop Area */}
              <div
                className={`upload-area ${
                  dragActive 
                    ? 'upload-area-active' 
                    : file 
                    ? 'upload-area-success' 
                    : 'upload-area-default'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  onChange={handleInputChange}
                  accept="image/*"
                  className="file-input"
                />
                
                {!file ? (
                  <div className="upload-content">
                    <Camera className="upload-icon" />
                    <p className="upload-title">
                      Drop your image here, or click to browse
                    </p>
                    <p className="upload-subtitle">
                      Supports JPG, PNG, and other image formats
                    </p>
                  </div>
                ) : (
                  <div className="file-selected">
                    <CheckCircle className="file-success-icon" />
                    <p className="file-name">
                      {file.name}
                    </p>
                    <p className="file-size">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                    <button
                      type="button"
                      onClick={clearSelection}
                      className="remove-button"
                    >
                      <X className="remove-icon" />
                      Remove
                    </button>
                  </div>
                )}
              </div>

              {/* Preview */}
              {preview && (
                <div className="preview-section">
                  <h3 className="preview-title">Preview</h3>
                  <img 
                    src={preview} 
                    alt="Preview" 
                    className="preview-image"
                  />
                </div>
              )}

              {/* Analyze Button */}
              <button 
                onClick={handleSubmit} 
                disabled={isLoading || !file}
                className={`analyze-button ${
                  isLoading || !file ? 'analyze-button-disabled' : 'analyze-button-enabled'
                }`}
              >
                {isLoading ? (
                  <div className="button-content">
                    <div className="loading-spinner"></div>
                    Analyzing Safety Compliance...
                  </div>
                ) : (
                  <div className="button-content">
                    <Upload className="button-icon" />
                    Analyze Hard Hat Detection
                  </div>
                )}
              </button>
            </div>

            {/* Error Message */}
            {error && (
              <div className="error-message">
                <AlertTriangle className="error-icon" />
                <p className="error-text">{error}</p>
              </div>
            )}
          </div>

          {/* Results Section */}
          {resultImage && (
            <div className="results-section">
              <div className="results-header">
                <CheckCircle className="results-icon" />
                <h2 className="results-title">Analysis Complete</h2>
              </div>
              
              <div className="results-content">
                <img 
                  src={resultImage} 
                  alt="Safety analysis results with hard hat detection annotations" 
                  className="results-image"
                />
                <p className="results-description">
                  Detected individuals and hard hat compliance status are highlighted in the image above.
                </p>
              </div>

              {/* Action Buttons */}
              <div className="action-buttons">
                <button
                  onClick={clearSelection}
                  className="secondary-button"
                >
                  Analyze Another Image
                </button>
                <a
                  href={resultImage}
                  download="safety-analysis-result.jpg"
                  className="primary-button download-link"
                >
                  Download Result
                </a>
              </div>
            </div>
          )}
        </div>

        {/* Features Section */}
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon feature-icon-blue">
              <Shield className="feature-icon-svg" />
            </div>
            <h3 className="feature-title">Real-time Detection</h3>
            <p className="feature-description">
              Instantly identify hard hat compliance across multiple individuals in workplace images.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon feature-icon-green">
              <CheckCircle className="feature-icon-svg" />
            </div>
            <h3 className="feature-title">High Accuracy</h3>
            <p className="feature-description">
              Advanced AI model trained specifically for construction safety equipment detection.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon feature-icon-orange">
              <Camera className="feature-icon-svg" />
            </div>
            <h3 className="feature-title">Easy Integration</h3>
            <p className="feature-description">
              Simple upload interface with detailed annotations and downloadable results.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="footer">
          <p>Ensuring workplace safety through intelligent monitoring</p>
        </div>
      </div>
    </div>
  );
}

export default App;