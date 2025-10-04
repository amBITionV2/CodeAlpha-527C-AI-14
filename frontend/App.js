/**
 * SignSpeak AI - Main Application Component
 * Real-time sign language communication bridge
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  Dimensions,
  StatusBar,
  SafeAreaView,
} from 'react-native';
import { Camera } from 'expo-camera';
import { Audio } from 'expo-av';
import * as Speech from 'expo-speech';
import axios from 'axios';

const { width, height } = Dimensions.get('window');

const API_BASE_URL = 'http://localhost:5000'; // Backend API URL

export default function App() {
  // State management
  const [hasPermission, setHasPermission] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [recognizedText, setRecognizedText] = useState('');
  const [recognizedGesture, setRecognizedGesture] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [cameraRef, setCameraRef] = useState(null);
  const [recording, setRecording] = useState(null);
  const [sound, setSound] = useState(null);

  // Request permissions on app start
  useEffect(() => {
    requestPermissions();
  }, []);

  const requestPermissions = async () => {
    try {
      const { status: cameraStatus } = await Camera.requestCameraPermissionsAsync();
      const { status: audioStatus } = await Audio.requestPermissionsAsync();
      
      if (cameraStatus === 'granted' && audioStatus === 'granted') {
        setHasPermission(true);
      } else {
        setHasPermission(false);
        Alert.alert(
          'Permissions Required',
          'SignSpeak AI needs camera and microphone access to function properly.'
        );
      }
    } catch (error) {
      console.error('Error requesting permissions:', error);
      setHasPermission(false);
    }
  };

  // Camera gesture recognition
  const recognizeGesture = async (imageUri) => {
    try {
      setIsProcessing(true);
      
      // Convert image to base64
      const response = await fetch(imageUri);
      const blob = await response.blob();
      const base64 = await blobToBase64(blob);
      
      // Send to backend for gesture recognition
      const result = await axios.post(`${API_BASE_URL}/recognize_gesture`, {
        image: base64
      });
      
      if (result.data.gesture) {
        setRecognizedGesture(result.data.gesture);
        
        // Convert gesture to speech
        await Speech.speak(result.data.gesture, {
          language: 'en',
          pitch: 1.0,
          rate: 0.8,
        });
      }
      
    } catch (error) {
      console.error('Error recognizing gesture:', error);
      Alert.alert('Error', 'Failed to recognize gesture. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  // Speech recognition
  const startListening = async () => {
    try {
      setIsListening(true);
      
      // Start audio recording
      const recording = new Audio.Recording();
      await recording.prepareToRecordAsync(Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY);
      await recording.startAsync();
      setRecording(recording);
      
    } catch (error) {
      console.error('Error starting speech recognition:', error);
      Alert.alert('Error', 'Failed to start speech recognition.');
      setIsListening(false);
    }
  };

  const stopListening = async () => {
    try {
      setIsListening(false);
      
      if (recording) {
        await recording.stopAndUnloadAsync();
        const uri = recording.getURI();
        
        // Convert audio to base64 and send to backend
        const response = await fetch(uri);
        const blob = await response.blob();
        const base64 = await blobToBase64(blob);
        
        const result = await axios.post(`${API_BASE_URL}/speech_to_text`, {
          audio: base64
        });
        
        if (result.data.text) {
          setRecognizedText(result.data.text);
          
          // Convert text to gesture animation
          await convertTextToGesture(result.data.text);
        }
        
        setRecording(null);
      }
    } catch (error) {
      console.error('Error stopping speech recognition:', error);
      Alert.alert('Error', 'Failed to process speech.');
    }
  };

  // Convert text to gesture animation
  const convertTextToGesture = async (text) => {
    try {
      const result = await axios.post(`${API_BASE_URL}/text_to_gesture`, {
        text: text
      });
      
      if (result.data.gesture_sequence) {
        // TODO: Animate 3D avatar with gesture sequence
        console.log('Gesture sequence:', result.data.gesture_sequence);
      }
    } catch (error) {
      console.error('Error converting text to gesture:', error);
    }
  };

  // Utility function to convert blob to base64
  const blobToBase64 = (blob) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result.split(',')[1]);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  };

  // Render loading screen
  if (hasPermission === null) {
    return (
      <View style={styles.container}>
        <Text style={styles.loadingText}>Loading SignSpeak AI...</Text>
      </View>
    );
  }

  // Render permission denied screen
  if (hasPermission === false) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>
          Camera and microphone permissions are required for SignSpeak AI to function.
        </Text>
        <TouchableOpacity style={styles.button} onPress={requestPermissions}>
          <Text style={styles.buttonText}>Grant Permissions</Text>
        </TouchableOpacity>
      </View>
    );
  }

  // Main app interface
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#1a1a2e" />
      
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>SignSpeak AI</Text>
        <Text style={styles.subtitle}>Real-time Sign Language Communication</Text>
      </View>

      {/* Camera View */}
      <View style={styles.cameraContainer}>
        <Camera
          style={styles.camera}
          type={Camera.Constants.Type.front}
          ref={setCameraRef}
          onCameraReady={() => console.log('Camera ready')}
        >
          {/* Gesture recognition overlay */}
          <View style={styles.overlay}>
            <View style={styles.gestureBox}>
              <Text style={styles.gestureLabel}>Gesture Recognition</Text>
              {recognizedGesture ? (
                <Text style={styles.recognizedGesture}>{recognizedGesture}</Text>
              ) : (
                <Text style={styles.placeholderText}>Point camera at sign language</Text>
              )}
            </View>
          </View>
        </Camera>
      </View>

      {/* Control Buttons */}
      <View style={styles.controls}>
        {/* Gesture Recognition Button */}
        <TouchableOpacity
          style={[styles.controlButton, isProcessing && styles.processingButton]}
          onPress={() => {
            if (cameraRef) {
              cameraRef.takePictureAsync({
                quality: 0.8,
                base64: false,
                onPictureSaved: (photo) => {
                  recognizeGesture(photo.uri);
                }
              });
            }
          }}
          disabled={isProcessing}
        >
          <Text style={styles.controlButtonText}>
            {isProcessing ? 'Processing...' : 'Recognize Gesture'}
          </Text>
        </TouchableOpacity>

        {/* Speech Recognition Button */}
        <TouchableOpacity
          style={[styles.controlButton, isListening && styles.listeningButton]}
          onPress={isListening ? stopListening : startListening}
        >
          <Text style={styles.controlButtonText}>
            {isListening ? 'Stop Listening' : 'Start Speaking'}
          </Text>
        </TouchableOpacity>
      </View>

      {/* Recognition Results */}
      <View style={styles.results}>
        {recognizedText ? (
          <View style={styles.resultBox}>
            <Text style={styles.resultLabel}>Recognized Speech:</Text>
            <Text style={styles.resultText}>{recognizedText}</Text>
          </View>
        ) : null}
        
        {recognizedGesture ? (
          <View style={styles.resultBox}>
            <Text style={styles.resultLabel}>Recognized Gesture:</Text>
            <Text style={styles.resultText}>{recognizedGesture}</Text>
          </View>
        ) : null}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
  },
  loadingText: {
    color: '#fff',
    fontSize: 18,
    textAlign: 'center',
    marginTop: 50,
  },
  errorText: {
    color: '#ff6b6b',
    fontSize: 16,
    textAlign: 'center',
    margin: 20,
  },
  header: {
    padding: 20,
    alignItems: 'center',
    backgroundColor: '#16213e',
  },
  title: {
    color: '#fff',
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  subtitle: {
    color: '#a0a0a0',
    fontSize: 14,
  },
  cameraContainer: {
    flex: 1,
    margin: 10,
    borderRadius: 10,
    overflow: 'hidden',
  },
  camera: {
    flex: 1,
  },
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
  },
  gestureBox: {
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
  },
  gestureLabel: {
    color: '#fff',
    fontSize: 16,
    marginBottom: 10,
  },
  recognizedGesture: {
    color: '#4ecdc4',
    fontSize: 24,
    fontWeight: 'bold',
  },
  placeholderText: {
    color: '#a0a0a0',
    fontSize: 16,
  },
  controls: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 20,
    backgroundColor: '#16213e',
  },
  controlButton: {
    backgroundColor: '#4ecdc4',
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderRadius: 25,
    minWidth: 120,
    alignItems: 'center',
  },
  processingButton: {
    backgroundColor: '#ffa726',
  },
  listeningButton: {
    backgroundColor: '#ff6b6b',
  },
  controlButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  results: {
    padding: 20,
    backgroundColor: '#0f0f23',
  },
  resultBox: {
    backgroundColor: '#16213e',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
  },
  resultLabel: {
    color: '#a0a0a0',
    fontSize: 14,
    marginBottom: 5,
  },
  resultText: {
    color: '#fff',
    fontSize: 16,
  },
  button: {
    backgroundColor: '#4ecdc4',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 25,
    alignSelf: 'center',
    marginTop: 20,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
