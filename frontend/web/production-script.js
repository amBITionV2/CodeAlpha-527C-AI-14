/**
 * SignSpeak AI - Production Frontend Script
 * Real-time gesture recognition, speech processing, and 3D avatar animation
 */

class ProductionSignSpeakAI {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5000';
        this.isConnected = false;
        this.isListening = false;
        this.isCameraActive = false;
        this.avatar = null;
        this.stream = null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        
        // DOM elements
        this.elements = {};
        
        // Initialize
        this.init();
    }
    
    async init() {
        this.initializeElements();
        this.setupEventListeners();
        await this.checkApiConnection();
        await this.initializeAvatar();
        this.startStatusUpdates();
    }
    
    initializeElements() {
        // Status elements
        this.elements.statusDot = document.getElementById('statusDot');
        this.elements.statusText = document.getElementById('statusText');
        this.elements.apiStatus = document.getElementById('apiStatus');
        this.elements.gestureStatus = document.getElementById('gestureStatus');
        this.elements.speechStatus = document.getElementById('speechStatus');
        this.elements.avatarStatus = document.getElementById('avatarStatus');
        
        // Camera elements
        this.elements.cameraFeed = document.getElementById('cameraFeed');
        this.elements.startCameraBtn = document.getElementById('startCamera');
        this.elements.stopCameraBtn = document.getElementById('stopCamera');
        this.elements.captureGestureBtn = document.getElementById('captureGesture');
        this.elements.detectionOverlay = document.getElementById('detectionOverlay');
        
        // Gesture recognition elements
        this.elements.gestureName = document.getElementById('gestureName');
        this.elements.confidenceFill = document.getElementById('confidenceFill');
        this.elements.confidenceText = document.getElementById('confidenceText');
        
        // Speech elements
        this.elements.startListeningBtn = document.getElementById('startListening');
        this.elements.stopListeningBtn = document.getElementById('stopListening');
        this.elements.languageSelect = document.getElementById('languageSelect');
        this.elements.waveform = document.getElementById('waveform');
        this.elements.speechStatus = document.getElementById('speechStatus');
        this.elements.recognizedText = document.getElementById('recognizedText');
        
        // TTS elements
        this.elements.ttsInput = document.getElementById('ttsInput');
        this.elements.textToSpeechBtn = document.getElementById('textToSpeechBtn');
        this.elements.audioOutput = document.getElementById('audioOutput');
        
        // Text processing elements
        this.elements.textInput = document.getElementById('textInput');
        this.elements.convertToGestureBtn = document.getElementById('convertToGestureBtn');
        this.elements.gestureSequence = document.getElementById('gestureSequence');
        
        // Avatar elements
        this.elements.resetAvatarBtn = document.getElementById('resetAvatar');
        this.elements.testAnimationBtn = document.getElementById('testAnimation');
        this.elements.currentGestureName = document.getElementById('currentGestureName');
        this.elements.gestureProgress = document.getElementById('gestureProgress');
        
        // Loading and toast elements
        this.elements.loadingOverlay = document.getElementById('loadingOverlay');
        this.elements.toastContainer = document.getElementById('toastContainer');
    }
    
    setupEventListeners() {
        // Camera controls
        this.elements.startCameraBtn.addEventListener('click', () => this.startCamera());
        this.elements.stopCameraBtn.addEventListener('click', () => this.stopCamera());
        this.elements.captureGestureBtn.addEventListener('click', () => this.captureGesture());
        
        // Speech controls
        this.elements.startListeningBtn.addEventListener('click', () => this.startListening());
        this.elements.stopListeningBtn.addEventListener('click', () => this.stopListening());
        this.elements.textToSpeechBtn.addEventListener('click', () => this.textToSpeech());
        
        // Text processing
        this.elements.convertToGestureBtn.addEventListener('click', () => this.convertTextToGesture());
        
        // Avatar controls
        this.elements.resetAvatarBtn.addEventListener('click', () => this.resetAvatar());
        this.elements.testAnimationBtn.addEventListener('click', () => this.testAvatarAnimation());
        
        // Language change
        this.elements.languageSelect.addEventListener('change', () => this.updateLanguage());
    }
    
    async checkApiConnection() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            
            if (response.ok) {
                this.isConnected = true;
                this.updateConnectionStatus(true, 'Connected');
                this.updateSystemStatus(data.systems);
            } else {
                throw new Error(data.error || 'API connection failed');
            }
        } catch (error) {
            this.isConnected = false;
            this.updateConnectionStatus(false, 'Disconnected');
            this.showToast('API connection failed. Please start the backend server.', 'error');
        }
    }
    
    updateConnectionStatus(connected, message) {
        this.elements.statusDot.className = `status-dot ${connected ? 'connected' : ''}`;
        this.elements.statusText.textContent = message;
        this.elements.apiStatus.textContent = message;
        this.elements.apiStatus.className = `status-value ${connected ? 'connected' : 'error'}`;
    }
    
    updateSystemStatus(systems) {
        if (systems) {
            this.elements.gestureStatus.textContent = systems.gesture_recognition ? 'Ready' : 'Not Available';
            this.elements.gestureStatus.className = `status-value ${systems.gesture_recognition ? 'connected' : 'error'}`;
            
            this.elements.speechStatus.textContent = systems.speech_processing ? 'Ready' : 'Not Available';
            this.elements.speechStatus.className = `status-value ${systems.speech_processing ? 'connected' : 'error'}`;
        }
    }
    
    async initializeAvatar() {
        try {
            // Initialize Three.js avatar
            this.avatar = new ThreeJSAvatar('threejs-container');
            this.elements.avatarStatus.textContent = 'Ready';
            this.elements.avatarStatus.className = 'status-value connected';
        } catch (error) {
            console.error('Avatar initialization failed:', error);
            this.elements.avatarStatus.textContent = 'Error';
            this.elements.avatarStatus.className = 'status-value error';
        }
    }
    
    async startCamera() {
        try {
            this.showLoading('Starting camera...');
            
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: { 
                    width: 1280, 
                    height: 720,
                    facingMode: 'user'
                },
                audio: false
            });
            
            this.elements.cameraFeed.srcObject = this.stream;
            this.isCameraActive = true;
            
            this.elements.startCameraBtn.disabled = true;
            this.elements.stopCameraBtn.disabled = false;
            this.elements.captureGestureBtn.disabled = false;
            
            this.hideLoading();
            this.showToast('Camera started successfully', 'success');
            
        } catch (error) {
            console.error('Camera start failed:', error);
            this.hideLoading();
            this.showToast('Failed to start camera. Please check permissions.', 'error');
        }
    }
    
    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        
        this.elements.cameraFeed.srcObject = null;
        this.isCameraActive = false;
        
        this.elements.startCameraBtn.disabled = false;
        this.elements.stopCameraBtn.disabled = true;
        this.elements.captureGestureBtn.disabled = true;
        
        this.showToast('Camera stopped', 'info');
    }
    
    async captureGesture() {
        if (!this.isCameraActive || !this.isConnected) {
            this.showToast('Camera not active or API not connected', 'error');
            return;
        }
        
        try {
            this.showLoading('Recognizing gesture...');
            
            // Capture frame from video
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = this.elements.cameraFeed.videoWidth;
            canvas.height = this.elements.cameraFeed.videoHeight;
            ctx.drawImage(this.elements.cameraFeed, 0, 0);
            
            // Convert to base64
            const imageData = canvas.toDataURL('image/jpeg', 0.8);
            const base64Data = imageData.split(',')[1];
            
            // Send to API
            const response = await fetch(`${this.apiBaseUrl}/recognize_gesture`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: base64Data })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.displayGestureResult(result);
                this.animateAvatarGesture(result.gesture);
            } else {
                throw new Error(result.error || 'Gesture recognition failed');
            }
            
            this.hideLoading();
            
        } catch (error) {
            console.error('Gesture recognition failed:', error);
            this.hideLoading();
            this.showToast('Gesture recognition failed: ' + error.message, 'error');
        }
    }
    
    displayGestureResult(result) {
        this.elements.gestureName.textContent = result.gesture;
        this.elements.confidenceFill.style.width = `${result.confidence * 100}%`;
        this.elements.confidenceText.textContent = `${Math.round(result.confidence * 100)}%`;
        
        // Update confidence bar color
        if (result.confidence > 0.8) {
            this.elements.confidenceFill.style.background = 'linear-gradient(90deg, #4ecdc4, #44a08d)';
        } else if (result.confidence > 0.6) {
            this.elements.confidenceFill.style.background = 'linear-gradient(90deg, #ffa500, #ff8c00)';
        } else {
            this.elements.confidenceFill.style.background = 'linear-gradient(90deg, #ff6b6b, #ff5252)';
        }
        
        this.showToast(`Gesture recognized: ${result.gesture} (${Math.round(result.confidence * 100)}%)`, 'success');
    }
    
    async startListening() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(this.stream);
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };
            
            this.mediaRecorder.onstop = () => {
                this.processAudio();
            };
            
            this.mediaRecorder.start();
            this.isListening = true;
            
            this.elements.startListeningBtn.disabled = true;
            this.elements.stopListeningBtn.disabled = false;
            this.elements.speechStatus.textContent = 'Listening...';
            this.elements.speechStatus.style.color = '#4ecdc4';
            
            // Animate waveform
            this.animateWaveform(true);
            
            this.showToast('Started listening for speech', 'info');
            
        } catch (error) {
            console.error('Speech listening failed:', error);
            this.showToast('Failed to start speech recognition. Please check microphone permissions.', 'error');
        }
    }
    
    stopListening() {
        if (this.mediaRecorder && this.isListening) {
            this.mediaRecorder.stop();
            this.stream.getTracks().forEach(track => track.stop());
            this.isListening = false;
            
            this.elements.startListeningBtn.disabled = false;
            this.elements.stopListeningBtn.disabled = true;
            this.elements.speechStatus.textContent = 'Processing...';
            this.elements.speechStatus.style.color = '#ffa500';
            
            // Stop waveform animation
            this.animateWaveform(false);
        }
    }
    
    async processAudio() {
        try {
            this.showLoading('Processing speech...');
            
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
            const base64Audio = await this.blobToBase64(audioBlob);
            
            const language = this.elements.languageSelect.value;
            
            const response = await fetch(`${this.apiBaseUrl}/speech_to_text`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    audio: base64Audio,
                    language: language
                })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.displaySpeechResult(result);
                // Auto-convert to gesture
                await this.convertTextToGesture(result.text);
            } else {
                throw new Error(result.error || 'Speech recognition failed');
            }
            
            this.hideLoading();
            
        } catch (error) {
            console.error('Speech processing failed:', error);
            this.hideLoading();
            this.showToast('Speech recognition failed: ' + error.message, 'error');
        }
    }
    
    displaySpeechResult(result) {
        this.elements.recognizedText.textContent = result.text;
        this.elements.speechStatus.textContent = `Confidence: ${Math.round(result.confidence * 100)}%`;
        
        // Update status color
        if (result.confidence > 0.8) {
            this.elements.speechStatus.style.color = '#4ecdc4';
        } else if (result.confidence > 0.6) {
            this.elements.speechStatus.style.color = '#ffa500';
        } else {
            this.elements.speechStatus.style.color = '#ff6b6b';
        }
        
        this.showToast(`Speech recognized: "${result.text}" (${Math.round(result.confidence * 100)}%)`, 'success');
    }
    
    async textToSpeech() {
        const text = this.elements.ttsInput.value.trim();
        if (!text) {
            this.showToast('Please enter text to convert to speech', 'warning');
            return;
        }
        
        try {
            this.showLoading('Converting text to speech...');
            
            const language = this.elements.languageSelect.value;
            
            const response = await fetch(`${this.apiBaseUrl}/text_to_speech`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    text: text,
                    language: language
                })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                // Play audio
                const audioBlob = this.base64ToBlob(result.audio, 'audio/wav');
                const audioUrl = URL.createObjectURL(audioBlob);
                this.elements.audioOutput.src = audioUrl;
                this.elements.audioOutput.play();
                
                this.showToast('Text converted to speech successfully', 'success');
            } else {
                throw new Error(result.error || 'Text-to-speech conversion failed');
            }
            
            this.hideLoading();
            
        } catch (error) {
            console.error('Text-to-speech failed:', error);
            this.hideLoading();
            this.showToast('Text-to-speech conversion failed: ' + error.message, 'error');
        }
    }
    
    async convertTextToGesture(text = null) {
        const inputText = text || this.elements.textInput.value.trim();
        if (!inputText) {
            this.showToast('Please enter text to convert to gestures', 'warning');
            return;
        }
        
        try {
            this.showLoading('Converting text to gestures...');
            
            const response = await fetch(`${this.apiBaseUrl}/text_to_gesture`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: inputText })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.displayGestureSequence(result.gesture_sequence);
                this.animateGestureSequence(result.gesture_sequence);
            } else {
                throw new Error(result.error || 'Text-to-gesture conversion failed');
            }
            
            this.hideLoading();
            
        } catch (error) {
            console.error('Text-to-gesture conversion failed:', error);
            this.hideLoading();
            this.showToast('Text-to-gesture conversion failed: ' + error.message, 'error');
        }
    }
    
    displayGestureSequence(gestures) {
        this.elements.gestureSequence.innerHTML = '';
        
        if (gestures.length === 0) {
            this.elements.gestureSequence.innerHTML = '<div class="sequence-placeholder">No gestures found</div>';
            return;
        }
        
        gestures.forEach((gesture, index) => {
            const gestureItem = document.createElement('div');
            gestureItem.className = 'gesture-item';
            gestureItem.innerHTML = `
                <div>
                    <div class="gesture-name">${gesture.gesture}</div>
                    <div class="gesture-description">${gesture.description || ''}</div>
                </div>
                <div class="gesture-duration">${gesture.duration.toFixed(1)}s</div>
            `;
            this.elements.gestureSequence.appendChild(gestureItem);
        });
    }
    
    animateGestureSequence(gestures) {
        if (!this.avatar || gestures.length === 0) return;
        
        this.avatar.animateGestureSequence(gestures, () => {
            this.elements.currentGestureName.textContent = 'Ready';
            this.elements.gestureProgress.style.width = '0%';
        });
    }
    
    animateAvatarGesture(gestureName) {
        if (!this.avatar) return;
        
        this.avatar.animateGesture(gestureName, () => {
            this.elements.currentGestureName.textContent = 'Ready';
        });
    }
    
    resetAvatar() {
        if (this.avatar) {
            this.avatar.resetPose();
            this.elements.currentGestureName.textContent = 'Ready';
            this.elements.gestureProgress.style.width = '0%';
            this.showToast('Avatar pose reset', 'info');
        }
    }
    
    testAvatarAnimation() {
        if (!this.avatar) return;
        
        const testGestures = [
            { gesture: 'HELLO', duration: 1.0 },
            { gesture: 'THANK_YOU', duration: 1.2 },
            { gesture: 'YES', duration: 0.8 }
        ];
        
        this.animateGestureSequence(testGestures);
        this.showToast('Playing test animation', 'info');
    }
    
    updateLanguage() {
        const language = this.elements.languageSelect.value;
        this.showToast(`Language changed to ${language}`, 'info');
    }
    
    animateWaveform(animate) {
        const waveBars = this.elements.waveform.querySelectorAll('.wave-bar');
        
        if (animate) {
            waveBars.forEach(bar => {
                bar.style.animationPlayState = 'running';
            });
        } else {
            waveBars.forEach(bar => {
                bar.style.animationPlayState = 'paused';
                bar.style.height = '10px';
            });
        }
    }
    
    startStatusUpdates() {
        // Update status every 30 seconds
        setInterval(() => {
            this.checkApiConnection();
        }, 30000);
    }
    
    // Utility functions
    blobToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result.split(',')[1]);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }
    
    base64ToBlob(base64, mimeType) {
        const byteCharacters = atob(base64);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        return new Blob([byteArray], { type: mimeType });
    }
    
    showLoading(message = 'Processing...') {
        this.elements.loadingOverlay.querySelector('p').textContent = message;
        this.elements.loadingOverlay.classList.add('show');
    }
    
    hideLoading() {
        this.elements.loadingOverlay.classList.remove('show');
    }
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        this.elements.toastContainer.appendChild(toast);
        
        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Remove toast after 5 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 5000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.signspeakAI = new ProductionSignSpeakAI();
});
