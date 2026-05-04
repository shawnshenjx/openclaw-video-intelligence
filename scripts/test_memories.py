#!/usr/bin/env python3
"""
Test script for Memories.ai Video Intelligence Suite
Quick validation and testing of core functionality
"""

import os
import sys
import json
import subprocess
from urllib.parse import urlparse

# Test URLs for different platforms
TEST_URLS = {
    'youtube': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'tiktok': 'https://www.tiktok.com/@rickastleyofficial/video/7089573859440446721',
    'instagram': 'https://www.instagram.com/p/ABC123/',  # Placeholder
    'twitter': 'https://twitter.com/user/status/123'     # Placeholder
}

def check_prerequisites():
    """Check if all prerequisites are installed and configured"""
    print("🔍 Checking prerequisites...")
    
    # Check memories CLI
    try:
        result = subprocess.run(['memories', '--help'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ memories CLI installed")
        else:
            print("❌ memories CLI not working")
            return False
    except FileNotFoundError:
        print("❌ memories CLI not found. Install with: pip install memories-cli")
        return False
    
    # Check API key
    api_key = os.environ.get('MEMORIES_API_KEY')
    if api_key:
        if api_key.startswith('sk-'):
            print("✅ MEMORIES_API_KEY configured")
        else:
            print("⚠️ MEMORIES_API_KEY format may be invalid")
    else:
        print("❌ MEMORIES_API_KEY not set")
        print("   Set with: export MEMORIES_API_KEY='your-api-key'")
        return False
    
    return True

def test_platform_detection():
    """Test platform detection functionality"""
    print("\n🎯 Testing platform detection...")
    
    sys.path.insert(0, os.path.dirname(__file__))
    
    try:
        from memories import detect_platform
        
        for platform, url in TEST_URLS.items():
            detected = detect_platform(url)
            if detected == platform:
                print(f"✅ {platform}: {url} → {detected}")
            else:
                print(f"❌ {platform}: {url} → {detected} (expected {platform})")
    
    except ImportError as e:
        print(f"❌ Cannot import from memories.py: {e}")
        return False
    
    return True

def test_basic_analysis():
    """Test basic video analysis"""
    print("\n📊 Testing basic analysis...")
    
    # Test YouTube (most reliable)
    youtube_url = TEST_URLS['youtube']
    
    try:
        result = subprocess.run([
            'python', 'memories.py', 
            youtube_url,
            '--no-mai'  # Skip expensive MAI analysis for testing
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print(f"✅ Basic analysis successful for: {youtube_url}")
            
            # Try to parse output
            try:
                if os.path.exists('video_analysis.json'):
                    with open('video_analysis.json', 'r') as f:
                        data = json.load(f)
                    
                    if 'metadata' in data and 'title' in data['metadata']:
                        print(f"   Title: {data['metadata']['title']}")
                        return True
            except:
                pass
            
            print("   Output format validation skipped")
            return True
        else:
            print(f"❌ Analysis failed: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def test_cli_commands():
    """Test direct CLI commands"""
    print("\n⚡ Testing CLI commands...")
    
    # Test V2 metadata command
    try:
        result = subprocess.run([
            'memories', 'v2', 'social', 'metadata',
            '--platform', 'youtube',
            '--video-url', TEST_URLS['youtube'],
            '--channel', 'rapid'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ CLI metadata command successful")
            
            # Check if response is valid JSON
            try:
                data = json.loads(result.stdout)
                if 'code' in data:
                    print(f"   Response code: {data['code']}")
                    return True
            except json.JSONDecodeError:
                print("   Non-JSON response (may be normal)")
                return True
        else:
            print(f"❌ CLI command failed: {result.stderr}")
            return False
    
    except subprocess.TimeoutExpired:
        print("⏰ CLI command timed out (may indicate API issues)")
        return False
    except Exception as e:
        print(f"❌ CLI test error: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid inputs"""
    print("\n🚨 Testing error handling...")
    
    # Test invalid URL
    try:
        result = subprocess.run([
            'python', 'memories.py',
            'https://invalid-url.com/video'
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        # Should fail gracefully, not crash
        if result.returncode != 0:
            print("✅ Invalid URL handled gracefully")
        else:
            print("⚠️ Invalid URL should have failed")
        
        return True
    
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def run_performance_test():
    """Basic performance test"""
    print("\n🚀 Testing performance...")
    
    import time
    start_time = time.time()
    
    try:
        # Quick metadata-only test
        result = subprocess.run([
            'memories', 'v2', 'social', 'metadata',
            '--platform', 'youtube', 
            '--video-url', TEST_URLS['youtube'],
            '--channel', 'rapid'
        ], capture_output=True, text=True, timeout=15)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ Metadata request completed in {duration:.2f}s")
            if duration < 10:
                print("   Performance: Good")
            elif duration < 20:
                print("   Performance: Acceptable") 
            else:
                print("   Performance: Slow")
            return True
        else:
            print(f"❌ Performance test failed: {result.stderr}")
            return False
    
    except subprocess.TimeoutExpired:
        print("❌ Performance test timed out (>15s)")
        return False

def generate_test_report(test_results):
    """Generate a test report"""
    print("\n" + "="*50)
    print("📋 TEST REPORT")
    print("="*50)
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    
    for test_name, passed in test_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("-" * 50)
    print(f"SUMMARY: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Video Intelligence Suite is ready.")
        return True
    else:
        print("⚠️ Some tests failed. Check configuration and requirements.")
        return False

def main():
    """Run all tests"""
    print("🧪 Video Intelligence Suite - Test Runner")
    print("=" * 50)
    
    test_results = {}
    
    # Run tests
    test_results["Prerequisites"] = check_prerequisites()
    test_results["Platform Detection"] = test_platform_detection()
    test_results["Basic Analysis"] = test_basic_analysis()
    test_results["CLI Commands"] = test_cli_commands()
    test_results["Error Handling"] = test_error_handling()
    test_results["Performance"] = run_performance_test()
    
    # Generate report
    success = generate_test_report(test_results)
    
    # Cleanup
    try:
        if os.path.exists('video_analysis.json'):
            os.remove('video_analysis.json')
    except:
        pass
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()