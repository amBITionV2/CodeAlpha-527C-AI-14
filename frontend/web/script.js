/**
 * SignSpeak AI - Web Frontend JavaScript
 * Real-time sign language communication interface
 */

class SignSpeakAI {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5000';
        this.isListening = false;
        this.isCameraActive = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.cameraStream = null;
        
        this.initializeElements();
        this.setupEventListeners();
        this.checkBackendConnection();
    }

    initializeElements() {
        // Status elements
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
        
        // Camera elements
        this.cameraFeed = document.getElementById('cameraFeed');
        this.startCameraBtn = document.getElementById('startCamera');
        this.captureGestureBtn = document.getElementById('captureGesture');
        this.gestureText = document.getElementById('gestureText');
        this.confidenceFill = document.getElementById('confidenceFill');
        this.confidenceText = document.getElementById('confidenceText');
        
        // Speech elements
        this.startListeningBtn = document.getElementById('startListening');
        this.stopListeningBtn = document.getElementById('stopListening');
        this.speechStatus = document.getElementById('speechStatus');
        this.recognizedText = document.getElementById('recognizedText');
        this.waveform = document.getElementById('waveform');
        
        // Text elements
        this.textInput = document.getElementById('textInput');
        this.convertToGestureBtn = document.getElementById('convertToGesture');
        
        // Output elements
        this.gestureSequence = document.getElementById('gestureSequence');
        this.avatarPreview = document.getElementById('avatarPreview');
        this.currentGesture = document.getElementById('currentGesture');
        this.gestureName = document.getElementById('gestureName');
        
        // API testing elements
        this.testHealthBtn = document.getElementById('testHealth');
        this.testSpeechBtn = document.getElementById('testSpeech');
        this.testGestureBtn = document.getElementById('testGesture');
        this.apiResponse = document.getElementById('apiResponse');
        
        // Loading overlay
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.toastContainer = document.getElementById('toastContainer');
    }

    setupEventListeners() {
        // Camera controls
        this.startCameraBtn.addEventListener('click', () => this.startCamera());
        this.captureGestureBtn.addEventListener('click', () => this.captureGesture());
        
        // Speech controls
        this.startListeningBtn.addEventListener('click', () => this.startListening());
        this.stopListeningBtn.addEventListener('click', () => this.stopListening());
        
        // Text controls
        this.convertToGestureBtn.addEventListener('click', () => this.convertTextToGesture());
        
        // API testing
        this.testHealthBtn.addEventListener('click', () => this.testHealth());
        this.testSpeechBtn.addEventListener('click', () => this.testSpeechToText());
        this.testGestureBtn.addEventListener('click', () => this.testTextToGesture());
        
        // Footer links
        document.getElementById('helpLink').addEventListener('click', (e) => {
            e.preventDefault();
            this.showToast('Help documentation coming soon!', 'info');
        });
        
        document.getElementById('settingsLink').addEventListener('click', (e) => {
            e.preventDefault();
            this.showToast('Settings panel coming soon!', 'info');
        });
        
        document.getElementById('aboutLink').addEventListener('click', (e) => {
            e.preventDefault();
            this.showAbout();
        });
    }

    async checkBackendConnection() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            if (response.ok) {
                this.updateConnectionStatus(true);
                this.showToast('Backend connected successfully!', 'success');
            } else {
                this.updateConnectionStatus(false);
                this.showToast('Backend connection failed', 'error');
            }
        } catch (error) {
            this.updateConnectionStatus(false);
            this.showToast('Cannot connect to backend. Make sure it\'s running on port 5000', 'error');
        }
    }

    updateConnectionStatus(connected) {
        if (connected) {
            this.statusDot.classList.add('connected');
            this.statusText.textContent = 'Connected';
        } else {
            this.statusDot.classList.remove('connected');
            this.statusText.textContent = 'Disconnected';
        }
    }

    async startCamera() {
        try {
            this.cameraStream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480 },
                audio: false
            });
            
            this.cameraFeed.srcObject = this.cameraStream;
            this.isCameraActive = true;
            
            this.startCameraBtn.disabled = true;
            this.captureGestureBtn.disabled = false;
            
            this.showToast('Camera started successfully!', 'success');
        } catch (error) {
            this.showToast('Failed to access camera: ' + error.message, 'error');
        }
    }

    async captureGesture() {
        if (!this.isCameraActive) {
            this.showToast('Please start camera first', 'warning');
            return;
        }

        this.showLoading(true);
        
        try {
            // Capture frame from video
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = this.cameraFeed.videoWidth;
            canvas.height = this.cameraFeed.videoHeight;
            context.drawImage(this.cameraFeed, 0, 0);
            
            const imageData = canvas.toDataURL('image/jpeg');
            const base64Data = imageData.split(',')[1];
            
            const response = await fetch(`${this.apiBaseUrl}/recognize_gesture`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image: base64Data })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.gestureText.textContent = result.gesture;
                this.confidenceFill.style.width = `${result.confidence * 100}%`;
                this.confidenceText.textContent = `${Math.round(result.confidence * 100)}%`;
                
                // Update confidence bar color based on confidence level
                if (result.confidence > 0.8) {
                    this.confidenceFill.style.backgroundColor = '#4CAF50';
                } else if (result.confidence > 0.6) {
                    this.confidenceFill.style.backgroundColor = '#FF9800';
                } else {
                    this.confidenceFill.style.backgroundColor = '#F44336';
                }
                
                this.showToast(`Gesture recognized: ${result.gesture} (${Math.round(result.confidence * 100)}% confidence)`, 'success');
            } else {
                this.showToast('Gesture recognition failed: ' + result.error, 'error');
            }
        } catch (error) {
            this.showToast('Error recognizing gesture: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async startListening() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };
            
            this.mediaRecorder.onstop = () => {
                this.processAudio();
            };
            
            this.mediaRecorder.start();
            this.isListening = true;
            
            this.startListeningBtn.disabled = true;
            this.stopListeningBtn.disabled = false;
            this.speechStatus.textContent = 'Listening... Speak now';
            this.waveform.style.display = 'block';
            
            this.showToast('Started listening...', 'success');
        } catch (error) {
            this.showToast('Failed to access microphone: ' + error.message, 'error');
        }
    }

    stopListening() {
        if (this.mediaRecorder && this.isListening) {
            this.mediaRecorder.stop();
            this.isListening = false;
            
            this.startListeningBtn.disabled = false;
            this.stopListeningBtn.disabled = true;
            this.speechStatus.textContent = 'Processing speech...';
            this.waveform.style.display = 'none';
        }
    }

    async processAudio() {
        this.showLoading(true);
        
        try {
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
            const base64Audio = await this.blobToBase64(audioBlob);
            
            const response = await fetch(`${this.apiBaseUrl}/speech_to_text`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ audio: base64Audio })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.recognizedText.textContent = result.text;
                this.speechStatus.textContent = `Confidence: ${Math.round(result.confidence * 100)}%`;
                
                // Update status color based on confidence
                if (result.confidence > 0.8) {
                    this.speechStatus.style.color = '#4CAF50';
                } else if (result.confidence > 0.6) {
                    this.speechStatus.style.color = '#FF9800';
                } else {
                    this.speechStatus.style.color = '#F44336';
                }
                
                this.showToast(`Speech recognized: "${result.text}" (${Math.round(result.confidence * 100)}% confidence)`, 'success');
                
                // Auto-convert to gesture
                await this.convertTextToGesture(result.text);
            } else {
                this.showToast('Speech recognition failed: ' + result.error, 'error');
                this.speechStatus.textContent = 'Speech recognition failed';
                this.speechStatus.style.color = '#F44336';
            }
        } catch (error) {
            this.showToast('Error processing speech: ' + error.message, 'error');
            this.speechStatus.textContent = 'Error processing speech';
        } finally {
            this.showLoading(false);
        }
    }

    async convertTextToGesture(text = null) {
        const textToConvert = text || this.textInput.value.trim();
        
        if (!textToConvert) {
            this.showToast('Please enter some text to convert', 'warning');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/text_to_gesture`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: textToConvert })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.displayGestureSequence(result.gesture_sequence);
                this.animateAvatar(result.gesture_sequence);
                this.showToast(`Converted to ${result.gesture_sequence.length} gestures`, 'success');
            } else {
                this.showToast('Text to gesture conversion failed: ' + result.error, 'error');
            }
        } catch (error) {
            this.showToast('Error converting text to gesture: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    displayGestureSequence(gestures) {
        this.gestureSequence.innerHTML = '';
        
        gestures.forEach((gesture, index) => {
            const gestureItem = document.createElement('div');
            gestureItem.className = 'gesture-item';
            gestureItem.innerHTML = `
                <span class="gesture-name">${gesture.gesture}</span>
                <span class="gesture-duration">${gesture.duration}s</span>
            `;
            this.gestureSequence.appendChild(gestureItem);
        });
    }

    animateAvatar(gestures) {
        // Enhanced avatar animation with gesture display
        const avatar = this.avatarPreview.querySelector('.avatar-skeleton');
        const leftArm = avatar.querySelector('.left-arm');
        const rightArm = avatar.querySelector('.right-arm');
        const head = avatar.querySelector('.head');
        const torso = avatar.querySelector('.torso');
        
        let currentGesture = 0;
        
        // Clear any existing animation
        avatar.style.transform = '';
        leftArm.style.transform = '';
        rightArm.style.transform = '';
        head.style.transform = '';
        
        const animateNext = () => {
            if (currentGesture < gestures.length) {
                const gesture = gestures[currentGesture];
                
                // Display current gesture name
                this.gestureName.textContent = gesture.gesture;
                this.showToast(`Performing: ${gesture.gesture}`, 'info');
                
                // Create gesture-specific animations
                this.performGestureAnimation(gesture.gesture, leftArm, rightArm, head, torso);
                
                setTimeout(() => {
                    currentGesture++;
                    animateNext();
                }, gesture.duration * 1000);
            } else {
                // Reset to neutral position
                this.resetAvatarPosition(leftArm, rightArm, head, torso);
                this.gestureName.textContent = 'Ready';
                this.showToast('Gesture sequence completed!', 'success');
            }
        };
        
        animateNext();
    }
    
    performGestureAnimation(gestureName, leftArm, rightArm, head, torso) {
        // Gesture-specific animations
        const gestureAnimations = {
            'HELLO': () => {
                rightArm.style.transform = 'rotate(-45deg) translateY(-20px)';
                leftArm.style.transform = 'rotate(45deg) translateY(-20px)';
                head.style.transform = 'rotate(5deg)';
            },
            'THANK_YOU': () => {
                rightArm.style.transform = 'rotate(-90deg) translateX(-10px)';
                leftArm.style.transform = 'rotate(90deg) translateX(10px)';
            },
            'YES': () => {
                head.style.transform = 'rotate(15deg)';
                rightArm.style.transform = 'rotate(-30deg) translateY(-15px)';
            },
            'NO': () => {
                head.style.transform = 'rotate(-15deg)';
                leftArm.style.transform = 'rotate(30deg) translateY(-15px)';
            },
            'GOOD': () => {
                rightArm.style.transform = 'rotate(-60deg) translateY(-25px)';
                leftArm.style.transform = 'rotate(60deg) translateY(-25px)';
                head.style.transform = 'rotate(10deg)';
            },
            'BAD': () => {
                rightArm.style.transform = 'rotate(60deg) translateY(15px)';
                leftArm.style.transform = 'rotate(-60deg) translateY(15px)';
                head.style.transform = 'rotate(-10deg)';
            },
            'PLEASE': () => {
                rightArm.style.transform = 'rotate(-120deg) translateX(-20px)';
                leftArm.style.transform = 'rotate(120deg) translateX(20px)';
            },
            'SORRY': () => {
                head.style.transform = 'rotate(-20deg)';
                rightArm.style.transform = 'rotate(-45deg) translateY(-10px)';
                leftArm.style.transform = 'rotate(45deg) translateY(-10px)';
            },
            'WELCOME': () => {
                rightArm.style.transform = 'rotate(-90deg) translateY(-30px)';
                leftArm.style.transform = 'rotate(90deg) translateY(-30px)';
                head.style.transform = 'rotate(5deg)';
            },
            'GOODBYE': () => {
                rightArm.style.transform = 'rotate(-45deg) translateY(-20px)';
                leftArm.style.transform = 'rotate(45deg) translateY(-20px)';
                head.style.transform = 'rotate(-5deg)';
            }
        };
        
        // Apply gesture animation or default
        if (gestureAnimations[gestureName]) {
            gestureAnimations[gestureName]();
        } else {
            // Default animation for unknown gestures
            rightArm.style.transform = 'rotate(-30deg) translateY(-15px)';
            leftArm.style.transform = 'rotate(30deg) translateY(-15px)';
            head.style.transform = 'rotate(5deg)';
        }
    }
    
    resetAvatarPosition(leftArm, rightArm, head, torso) {
        leftArm.style.transform = '';
        rightArm.style.transform = '';
        head.style.transform = '';
        torso.style.transform = '';
    }

    // API Testing Methods
    async testHealth() {
        this.showLoading(true);
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const result = await response.json();
            
            this.apiResponse.textContent = JSON.stringify(result, null, 2);
            this.showToast('Health check successful!', 'success');
        } catch (error) {
            this.apiResponse.textContent = `Error: ${error.message}`;
            this.showToast('Health check failed', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async testSpeechToText() {
        this.showLoading(true);
        
        try {
            // Create dummy audio data
            const dummyAudio = 'dGVzdF9hdWRpb19kYXRh';
            
            const response = await fetch(`${this.apiBaseUrl}/speech_to_text`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ audio: dummyAudio })
            });
            
            const result = await response.json();
            this.apiResponse.textContent = JSON.stringify(result, null, 2);
            this.showToast('Speech test completed!', 'success');
        } catch (error) {
            this.apiResponse.textContent = `Error: ${error.message}`;
            this.showToast('Speech test failed', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async testTextToGesture() {
        this.showLoading(true);
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/text_to_gesture`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: 'Hello, how are you?' })
            });
            
            const result = await response.json();
            this.apiResponse.textContent = JSON.stringify(result, null, 2);
            this.showToast('Text to gesture test completed!', 'success');
        } catch (error) {
            this.apiResponse.textContent = `Error: ${error.message}`;
            this.showToast('Text to gesture test failed', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    // Utility Methods
    async blobToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }

    showLoading(show) {
        if (show) {
            this.loadingOverlay.classList.add('show');
        } else {
            this.loadingOverlay.classList.remove('show');
        }
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        this.toastContainer.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 5000);
    }

    showAbout() {
        const aboutContent = `
            SignSpeak AI v1.0.0
            
            Real-time sign language communication bridge
            for the deaf and hard-of-hearing community.
            
            Features:
            • ISL Gesture Recognition
            • Speech Processing
            • 3D Avatar Animation
            • Real-time Communication
            
            Built with ❤️ for accessibility
        `;
        
        this.apiResponse.textContent = aboutContent;
        this.showToast('About SignSpeak AI', 'info');
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SignSpeakAI();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Page is hidden, pause camera if active
        console.log('Page hidden, pausing camera');
    } else {
        // Page is visible, resume if needed
        console.log('Page visible, resuming');
    }
});

// Handle beforeunload to cleanup resources
window.addEventListener('beforeunload', () => {
    // Cleanup camera stream
    if (window.signSpeakAI && window.signSpeakAI.cameraStream) {
        window.signSpeakAI.cameraStream.getTracks().forEach(track => track.stop());
    }
});
