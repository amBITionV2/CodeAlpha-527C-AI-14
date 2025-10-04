/**
 * SignSpeak AI - Entry Point
 * React Native application entry point
 */

import { AppRegistry } from 'react-native';
import App from './App';
import { name as appName } from './package.json';

// Register the main component
AppRegistry.registerComponent(appName, () => App);
