#!/usr/bin/env python3
"""
SignSpeak AI - Setup Script
Automated setup for SignSpeak AI project
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("SignSpeak AI - Automated Setup")
    print("=" * 60)
    print("Setting up real-time sign language communication bridge")
    print("=" * 60)

def check_python():
    """Check Python installation"""
    print("\n1. Checking Python installation...")
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 9:
            print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
            return True
        else:
            print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.9+")
            return False
    except Exception as e:
        print(f"   ❌ Python check failed: {e}")
        return False

def check_node():
    """Check Node.js installation"""
    print("\n2. Checking Node.js installation...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   ✅ Node.js {version} - OK")
            return True
        else:
            print("   ❌ Node.js not found - Please install Node.js 18+")
            return False
    except Exception as e:
        print(f"   ❌ Node.js check failed: {e}")
        return False

def install_python_deps():
    """Install Python dependencies"""
    print("\n3. Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("   ✅ Python dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed to install Python dependencies: {e}")
        return False

def install_node_deps():
    """Install Node.js dependencies"""
    print("\n4. Installing Node.js dependencies...")
    try:
        os.chdir('frontend')
        subprocess.run(['npm', 'install'], check=True)
        os.chdir('..')
        print("   ✅ Node.js dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed to install Node.js dependencies: {e}")
        return False

def test_backend():
    """Test backend API"""
    print("\n5. Testing backend API...")
    try:
        import requests
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend API is running")
            return True
        else:
            print("   ⚠️ Backend API not running - Start with: python backend/app.py")
            return False
    except Exception as e:
        print(f"   ⚠️ Backend API not accessible: {e}")
        return False

def show_next_steps():
    """Show next steps"""
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Start Backend: python backend/app.py")
    print("2. Start Frontend: cd frontend && npm start")
    print("3. Access API: http://localhost:5000")
    print("4. Access Frontend: http://localhost:8081")
    print("\nDocumentation:")
    print("- README.md - Project overview")
    print("- QUICK_START.md - Quick start guide")
    print("- SETUP.md - Detailed setup instructions")
    print("\nReady to bridge communication gaps! 🌟")

def main():
    """Main setup function"""
    print_banner()
    
    # Check prerequisites
    python_ok = check_python()
    node_ok = check_node()
    
    if not python_ok or not node_ok:
        print("\n❌ Prerequisites not met. Please install:")
        if not python_ok:
            print("   - Python 3.9+ from https://python.org")
        if not node_ok:
            print("   - Node.js 18+ from https://nodejs.org")
        return False
    
    # Install dependencies
    python_deps_ok = install_python_deps()
    node_deps_ok = install_node_deps()
    
    if not python_deps_ok or not node_deps_ok:
        print("\n❌ Dependency installation failed")
        return False
    
    # Test backend
    test_backend()
    
    # Show next steps
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
