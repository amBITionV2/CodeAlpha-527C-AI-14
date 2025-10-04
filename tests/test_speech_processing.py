"""
Unit tests for Speech Processing Module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models.speech_processing import SpeechProcessor

class TestSpeechProcessor(unittest.TestCase):
    """Test cases for Speech Processor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = SpeechProcessor()
        self.test_audio_data = b"fake_audio_data"
        self.test_text = "Hello, this is a test"
    
    def test_initialization(self):
        """Test SpeechProcessor initialization"""
        self.assertIsNotNone(self.processor.recognizer)
        self.assertIsNotNone(self.processor.microphone)
        self.assertIsNotNone(self.processor.tts_engine)
        self.assertFalse(self.processor.is_listening)
    
    @patch('speech_recognition.Recognizer.recognize_google')
    def test_speech_to_text_success(self, mock_recognize):
        """Test successful speech to text conversion"""
        mock_recognize.return_value = "Hello world"
        
        text, confidence = self.processor.speech_to_text(self.test_audio_data)
        
        self.assertEqual(text, "Hello world")
        self.assertEqual(confidence, 0.85)  # Placeholder confidence
        mock_recognize.assert_called_once()
    
    @patch('speech_recognition.Recognizer.recognize_google')
    def test_speech_to_text_unknown_value(self, mock_recognize):
        """Test speech to text with unknown value error"""
        from speech_recognition import UnknownValueError
        mock_recognize.side_effect = UnknownValueError()
        
        text, confidence = self.processor.speech_to_text(self.test_audio_data)
        
        self.assertEqual(text, "")
        self.assertEqual(confidence, 0.0)
    
    @patch('speech_recognition.Recognizer.recognize_google')
    def test_speech_to_text_request_error(self, mock_recognize):
        """Test speech to text with request error"""
        from speech_recognition import RequestError
        mock_recognize.side_effect = RequestError("Service unavailable")
        
        text, confidence = self.processor.speech_to_text(self.test_audio_data)
        
        self.assertEqual(text, "")
        self.assertEqual(confidence, 0.0)
    
    @patch('pyttsx3.init')
    def test_text_to_speech(self, mock_tts_init):
        """Test text to speech conversion"""
        mock_engine = Mock()
        mock_engine.say = Mock()
        mock_engine.save_to_file = Mock()
        mock_engine.runAndWait = Mock()
        mock_tts_init.return_value = mock_engine
        
        # Mock file operations
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('os.remove') as mock_remove:
                audio_data = self.processor.text_to_speech(self.test_text)
                
                mock_engine.say.assert_called_once_with(self.test_text)
                mock_engine.save_to_file.assert_called_once()
                mock_engine.runAndWait.assert_called_once()
    
    def test_get_available_languages(self):
        """Test getting available languages"""
        languages = self.processor.get_available_languages()
        
        self.assertIsInstance(languages, list)
        self.assertIn('en-IN', languages)
        self.assertIn('hi-IN', languages)
        self.assertGreater(len(languages), 5)
    
    def test_set_tts_voice(self):
        """Test setting TTS voice"""
        with patch.object(self.processor.tts_engine, 'getProperty') as mock_get_property:
            mock_voices = [
                Mock(id='voice1', name='Voice 1'),
                Mock(id='voice2', name='Voice 2')
            ]
            mock_get_property.return_value = mock_voices
            
            with patch.object(self.processor.tts_engine, 'setProperty') as mock_set_property:
                result = self.processor.set_tts_voice('voice1')
                
                self.assertTrue(result)
                mock_set_property.assert_called_once_with('voice', 'voice1')
    
    def test_set_tts_voice_not_found(self):
        """Test setting non-existent TTS voice"""
        with patch.object(self.processor.tts_engine, 'getProperty') as mock_get_property:
            mock_voices = [Mock(id='voice1', name='Voice 1')]
            mock_get_property.return_value = mock_voices
            
            result = self.processor.set_tts_voice('nonexistent_voice')
            
            self.assertFalse(result)
    
    def test_get_available_voices(self):
        """Test getting available voices"""
        with patch.object(self.processor.tts_engine, 'getProperty') as mock_get_property:
            mock_voices = [
                Mock(id='voice1', name='Voice 1'),
                Mock(id='voice2', name='Voice 2')
            ]
            mock_get_property.return_value = mock_voices
            
            voices = self.processor.get_available_voices()
            
            self.assertEqual(len(voices), 2)
            self.assertEqual(voices[0]['id'], 'voice1')
            self.assertEqual(voices[0]['name'], 'Voice 1')
    
    def test_continuous_listening_start_stop(self):
        """Test starting and stopping continuous listening"""
        callback_func = Mock()
        
        # Start listening
        thread = self.processor.start_continuous_listening(callback_func)
        
        self.assertTrue(self.processor.is_listening)
        self.assertIsNotNone(thread)
        
        # Stop listening
        self.processor.stop_continuous_listening()
        
        self.assertFalse(self.processor.is_listening)

class TestSpeechProcessorIntegration(unittest.TestCase):
    """Integration tests for Speech Processor"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.processor = SpeechProcessor()
    
    def test_speech_pipeline(self):
        """Test complete speech processing pipeline"""
        # Test text to speech
        with patch('pyttsx3.init') as mock_tts_init:
            mock_engine = Mock()
            mock_engine.say = Mock()
            mock_engine.save_to_file = Mock()
            mock_engine.runAndWait = Mock()
            mock_tts_init.return_value = mock_engine
            
            with patch('builtins.open', mock_open()) as mock_file:
                with patch('os.remove') as mock_remove:
                    audio_data = self.processor.text_to_speech("Test speech")
                    self.assertIsInstance(audio_data, bytes)
    
    def test_error_handling(self):
        """Test error handling in speech processing"""
        # Test with invalid audio data
        text, confidence = self.processor.speech_to_text(b"invalid_audio")
        self.assertEqual(text, "")
        self.assertEqual(confidence, 0.0)

def mock_open():
    """Mock open function for file operations"""
    mock_file = MagicMock()
    mock_file.read.return_value = b"fake_audio_data"
    mock_file.__enter__.return_value = mock_file
    mock_file.__exit__.return_value = None
    return mock_file

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
