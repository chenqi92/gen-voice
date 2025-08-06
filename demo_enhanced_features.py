#!/usr/bin/env python3
"""
Enhanced TTS System Demo
Demonstrates all the new features implemented
"""

import requests
import json
import time
import os

BASE_URL = "http://127.0.0.1:5000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {data['status']}")
        print(f"✅ Engines loaded: {data['engines_loaded']}")
        print(f"✅ Current engine: {data['current_engine']}")
        print(f"✅ Available voices: {data['available_voices']}")
    else:
        print(f"❌ Health check failed: {response.status_code}")
    print()

def test_engines():
    """Test TTS engines"""
    print("🤖 Testing TTS Engines...")
    response = requests.get(f"{BASE_URL}/api/models")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Available engines: {len(data['engines'])}")
        for engine in data['engines']:
            status = "🟢 CURRENT" if engine['current'] else "⚪"
            print(f"  {status} {engine['name']}: {engine['description']}")
        print(f"✅ Current engine: {data['current_engine']}")
    else:
        print(f"❌ Engines test failed: {response.status_code}")
    print()

def test_voices():
    """Test available voices"""
    print("🎤 Testing Available Voices...")
    response = requests.get(f"{BASE_URL}/api/voices")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Available voices: {len(data['voices'])}")
        for voice in data['voices'][:5]:  # Show first 5
            print(f"  🔊 {voice['name']} ({voice['gender']})")
        if len(data['voices']) > 5:
            print(f"  ... and {len(data['voices']) - 5} more voices")
    else:
        print(f"❌ Voices test failed: {response.status_code}")
    print()

def test_speech_generation():
    """Test speech generation"""
    print("🗣️ Testing Speech Generation...")
    
    test_texts = [
        "Hello! This is a test of the enhanced TTS system.",
        "Welcome to the future of text-to-speech technology!",
        "This system supports multiple engines and voice options."
    ]
    
    # Get available voices
    voices_response = requests.get(f"{BASE_URL}/api/voices")
    if voices_response.status_code != 200:
        print("❌ Failed to get voices")
        return
    
    voices = voices_response.json()['voices']
    
    for i, text in enumerate(test_texts):
        voice = voices[i % len(voices)]
        print(f"  🎯 Generating: '{text[:30]}...' with {voice['name']}")
        
        response = requests.post(f"{BASE_URL}/api/generate", 
                               json={"text": text, "voice": voice['id']})
        
        if response.status_code == 200:
            data = response.json()
            audio_size = len(data['audio']) * 3 // 4  # Approximate size from base64
            print(f"    ✅ Generated {audio_size:,} bytes of audio")
        else:
            print(f"    ❌ Generation failed: {response.status_code}")
        
        time.sleep(1)  # Brief pause between requests
    print()

def test_history():
    """Test history functionality"""
    print("📚 Testing History Functionality...")
    
    response = requests.get(f"{BASE_URL}/api/history")
    if response.status_code == 200:
        data = response.json()
        history = data['history']
        stats = data['stats']
        
        print(f"✅ History entries: {len(history)}")
        print(f"✅ Total files: {stats['total_files']}")
        print(f"✅ Total size: {stats['total_size_mb']} MB")
        print(f"✅ Storage directory: {stats['storage_dir']}")
        print(f"✅ Auto cleanup: {stats['auto_cleanup_days']} days")
        
        if history:
            print("  📝 Recent entries:")
            for entry in history[:3]:  # Show first 3
                size_kb = entry['size'] // 1024
                timestamp = entry['timestamp'][:19].replace('T', ' ')
                print(f"    🎵 {entry['text'][:40]}... ({size_kb}KB, {timestamp})")
    else:
        print(f"❌ History test failed: {response.status_code}")
    print()

def test_cleanup():
    """Test cleanup functionality"""
    print("🧹 Testing Cleanup Functionality...")
    
    response = requests.get(f"{BASE_URL}/api/cleanup")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Cleanup completed: {data['message']}")
    else:
        print(f"❌ Cleanup test failed: {response.status_code}")
    print()

def show_feature_summary():
    """Show summary of implemented features"""
    print("🎉 ENHANCED TTS SYSTEM - FEATURE SUMMARY")
    print("=" * 50)
    
    features = [
        "✅ Multi-Engine TTS Support",
        "  🤖 Google TTS (Online)",
        "  🤖 OpenAI TTS (API Key Required)",
        "  🤖 Azure TTS (API Key Required)",
        "  🤖 Extensible Architecture",
        "",
        "✅ Enhanced Voice Options",
        "  🎤 8+ Google TTS Voices",
        "  🌍 Multiple Languages & Accents",
        "  🎭 Different Voice Characteristics",
        "",
        "✅ History Management",
        "  📚 Automatic Audio Storage",
        "  🗂️ Metadata Tracking",
        "  🧹 Automatic Cleanup (7 days)",
        "  📊 Storage Statistics",
        "",
        "✅ Advanced API Features",
        "  🔄 Engine Switching",
        "  📥 Audio Download",
        "  🗑️ Individual/Batch Deletion",
        "  🎵 Audio Playback Support",
        "",
        "✅ Web Interface",
        "  📱 Responsive Design",
        "  🎨 Modern UI/UX",
        "  🌐 Multi-language Support",
        "  ⚡ Real-time Updates"
    ]
    
    for feature in features:
        print(feature)
    
    print("\n🚀 Ready for Production Use!")
    print("=" * 50)

def main():
    """Run complete demo"""
    print("🎯 ENHANCED TTS SYSTEM DEMO")
    print("=" * 50)
    print()
    
    try:
        test_health()
        test_engines()
        test_voices()
        test_speech_generation()
        test_history()
        test_cleanup()
        
        print()
        show_feature_summary()
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Please make sure the TTS server is running:")
        print("   python app.py")
        print()
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    main()
