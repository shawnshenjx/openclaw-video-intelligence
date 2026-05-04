"""
Tests for platform detection functionality.

This module tests the detect_platform() function which identifies
video platforms from URLs (YouTube, TikTok, Instagram, Twitter).

Test Coverage:
- Valid URL patterns for each platform
- Edge cases and variations 
- Invalid URLs and error handling
- Performance and response time
"""

import pytest
from unittest.mock import patch, Mock
import sys
from pathlib import Path

# Add the scripts directory to path for importing
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

try:
    from analyze_video import detect_platform
except ImportError:
    # Fallback if import fails
    detect_platform = None

pytestmark = pytest.mark.unit

class TestPlatformDetection:
    """Test suite for platform detection functionality."""
    
    def test_detect_platform_function_exists(self):
        """Test that the detect_platform function exists and is importable."""
        assert detect_platform is not None, "detect_platform function should be importable"
        assert callable(detect_platform), "detect_platform should be callable"

    @pytest.mark.parametrize("url,expected_platform", [
        # YouTube variants
        ("https://www.youtube.com/watch?v=jNQXAC9IVRw", "youtube"),
        ("https://youtube.com/watch?v=jNQXAC9IVRw", "youtube"),
        ("https://youtu.be/jNQXAC9IVRw", "youtube"),
        ("https://www.youtu.be/jNQXAC9IVRw", "youtube"),
        ("https://m.youtube.com/watch?v=jNQXAC9IVRw", "youtube"),
        ("http://youtube.com/watch?v=jNQXAC9IVRw", "youtube"),
        
        # TikTok variants  
        ("https://www.tiktok.com/@user/video/1234567890123456789", "tiktok"),
        ("https://tiktok.com/@user/video/1234567890123456789", "tiktok"),
        ("https://vm.tiktok.com/ABC123/", "tiktok"),
        ("https://vt.tiktok.com/ABC123/", "tiktok"),
        ("https://www.tiktok.com/t/ABC123/", "tiktok"),
        ("https://m.tiktok.com/@user/video/1234567890123456789", "tiktok"),
        
        # Instagram variants
        ("https://www.instagram.com/p/ABC123DEF456/", "instagram"),
        ("https://instagram.com/p/ABC123DEF456/", "instagram"), 
        ("https://www.instagram.com/reel/ABC123DEF456/", "instagram"),
        ("https://instagram.com/reel/ABC123DEF456/", "instagram"),
        ("https://www.instagram.com/tv/ABC123DEF456/", "instagram"),
        ("https://instagr.am/p/ABC123DEF456/", "instagram"),
        
        # Twitter variants
        ("https://twitter.com/user/status/1234567890123456789", "twitter"),
        ("https://www.twitter.com/user/status/1234567890123456789", "twitter"),
        ("https://x.com/user/status/1234567890123456789", "twitter"),
        ("https://www.x.com/user/status/1234567890123456789", "twitter"),
        ("https://mobile.twitter.com/user/status/1234567890123456789", "twitter"),
    ])
    def test_detect_platform_valid_urls(self, url, expected_platform):
        """Test platform detection with valid URLs."""
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        result = detect_platform(url)
        assert result == expected_platform, f"URL {url} should be detected as {expected_platform}"

    @pytest.mark.parametrize("invalid_url", [
        "https://example.com/video.mp4",
        "https://vimeo.com/123456789", 
        "https://facebook.com/video/123456",
        "https://linkedin.com/posts/activity-123",
        "not-a-url-at-all",
        "",
        None,
        "ftp://youtube.com/watch?v=123",
        "https://youtube-fake.com/watch?v=123",
        "https://mytiktok.com/@user/video/123",
    ])
    def test_detect_platform_invalid_urls(self, invalid_url):
        """Test platform detection with invalid URLs."""
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        result = detect_platform(invalid_url)
        assert result is None or result == "unknown", \
            f"Invalid URL {invalid_url} should return None or 'unknown'"

    def test_detect_platform_case_insensitive(self):
        """Test that platform detection is case insensitive."""
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        urls_to_test = [
            ("HTTPS://WWW.YOUTUBE.COM/WATCH?V=jNQXAC9IVRw", "youtube"),
            ("https://WWW.TIKTOK.COM/@user/video/123", "tiktok"),
            ("HTTPS://instagram.com/p/ABC123/", "instagram"),
            ("https://TWITTER.com/user/status/123", "twitter"),
        ]
        
        for url, expected in urls_to_test:
            result = detect_platform(url)
            assert result == expected, f"Case insensitive test failed for {url}"

    def test_detect_platform_with_query_params(self):
        """Test platform detection with additional query parameters.""" 
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        urls_with_params = [
            ("https://www.youtube.com/watch?v=jNQXAC9IVRw&t=30s&list=123", "youtube"),
            ("https://www.youtube.com/watch?v=jNQXAC9IVRw&feature=youtu.be", "youtube"),
            ("https://www.instagram.com/p/ABC123/?utm_source=ig_web_copy_link", "instagram"),
            ("https://twitter.com/user/status/123?ref_src=twsrc%5Etfw", "twitter"),
        ]
        
        for url, expected in urls_with_params:
            result = detect_platform(url)
            assert result == expected, f"URL with params {url} should be detected as {expected}"

    def test_detect_platform_with_fragments(self):
        """Test platform detection with URL fragments."""
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        urls_with_fragments = [
            ("https://www.youtube.com/watch?v=jNQXAC9IVRw#t=30", "youtube"),
            ("https://www.instagram.com/p/ABC123/#comments", "instagram"),
            ("https://twitter.com/user/status/123#reply", "twitter"),
        ]
        
        for url, expected in urls_with_fragments:
            result = detect_platform(url)
            assert result == expected, f"URL with fragment {url} should be detected as {expected}"

class TestPlatformDetectionEdgeCases:
    """Test edge cases and error conditions for platform detection."""

    def test_detect_platform_empty_string(self):
        """Test detection with empty string."""
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        result = detect_platform("")
        assert result is None or result == "unknown"

    def test_detect_platform_whitespace_only(self):
        """Test detection with whitespace-only string."""
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        result = detect_platform("   \t\n   ")
        assert result is None or result == "unknown"

    def test_detect_platform_none_input(self):
        """Test detection with None input."""
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        try:
            result = detect_platform(None)
            assert result is None or result == "unknown"
        except (TypeError, AttributeError):
            # It's acceptable to raise an exception for None input
            pass

    def test_detect_platform_non_string_input(self):
        """Test detection with non-string input."""
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        non_string_inputs = [123, [], {}, True, 3.14]
        
        for input_val in non_string_inputs:
            try:
                result = detect_platform(input_val)
                assert result is None or result == "unknown"
            except (TypeError, AttributeError):
                # It's acceptable to raise an exception for invalid types
                pass

    @pytest.mark.parametrize("malformed_url", [
        "https://youtube.com/watch",  # Missing video ID
        "https://youtube.com/watch?v=",  # Empty video ID
        "https://tiktok.com/@user",  # Missing video path
        "https://instagram.com/p/",  # Missing post ID
        "https://twitter.com/user/status/",  # Missing status ID
        "https://youtube",  # Incomplete URL
        "youtube.com/watch?v=123",  # Missing protocol
    ])
    def test_detect_platform_malformed_urls(self, malformed_url):
        """Test detection with malformed URLs that might partially match patterns."""
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        result = detect_platform(malformed_url)
        # Depending on implementation, these might be detected or return None/unknown
        # The key is that the function should not crash
        assert result is not None  # Should return something, not crash

class TestPlatformDetectionPerformance:
    """Performance tests for platform detection."""

    @pytest.mark.performance
    def test_detect_platform_performance(self):
        """Test that platform detection is fast enough for practical use."""
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        import time
        
        test_urls = [
            "https://www.youtube.com/watch?v=jNQXAC9IVRw",
            "https://www.tiktok.com/@user/video/1234567890123456789", 
            "https://www.instagram.com/p/ABC123DEF456/",
            "https://twitter.com/user/status/1234567890123456789",
            "https://example.com/invalid-url"
        ]
        
        # Warm up
        for url in test_urls[:2]:
            detect_platform(url)
        
        # Time the actual test
        start_time = time.time()
        iterations = 1000
        
        for _ in range(iterations):
            for url in test_urls:
                detect_platform(url)
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / (iterations * len(test_urls))
        
        # Should be very fast - less than 1ms per detection
        assert avg_time < 0.001, f"Platform detection too slow: {avg_time*1000:.2f}ms per detection"

    @pytest.mark.performance 
    def test_detect_platform_memory_usage(self):
        """Test that platform detection doesn't leak memory."""
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        import gc
        import sys
        
        # Force garbage collection
        gc.collect()
        initial_objects = len(gc.get_objects())
        
        # Run many detections
        test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        for _ in range(10000):
            detect_platform(test_url)
        
        # Force garbage collection again
        gc.collect()
        final_objects = len(gc.get_objects())
        
        # Should not have significantly more objects
        object_increase = final_objects - initial_objects
        assert object_increase < 100, f"Memory leak detected: {object_increase} new objects"

class TestPlatformDetectionIntegration:
    """Integration tests that verify platform detection works with the broader system."""

    def test_detect_platform_with_analyze_video_integration(self, youtube_url):
        """Test that detected platform can be used in the broader analyze_video workflow."""
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        platform = detect_platform(youtube_url)
        assert platform == "youtube"
        
        # Verify that this platform result would be usable in downstream functions
        assert isinstance(platform, str)
        assert platform.isalpha()  # Should be alphabetic characters only
        assert len(platform) > 2  # Should be a meaningful platform name

    @pytest.mark.slow
    def test_detect_platform_with_real_urls(self, sample_urls):
        """Test platform detection with a variety of real URLs."""
        if detect_platform is None:
            pytest.skip("detect_platform function not available")
        
        # This test uses the sample_urls fixture from conftest.py
        for platform, urls in sample_urls.items():
            if platform == "invalid":
                continue
                
            for url in urls[:3]:  # Test first 3 URLs for each platform
                result = detect_platform(url)
                assert result == platform, f"Failed to detect {platform} for URL: {url}"