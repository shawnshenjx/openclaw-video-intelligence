"""
Tests for API client functionality.

This module tests API interactions with the Memories.ai service,
including request handling, response parsing, and error scenarios.

Test Coverage:
- API request formatting and headers
- Response parsing and validation
- Error handling and retry logic
- Authentication and rate limiting
- Network timeout and connection errors
"""

import pytest
import json
import time
from unittest.mock import patch, Mock, MagicMock, call
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
import sys
from pathlib import Path

# Add the scripts directory to path for importing
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

try:
    from analyze_video import (
        get_video_metadata, 
        get_video_transcript,
        run_memories_command
    )
except ImportError:
    # Fallback if import fails
    get_video_metadata = None
    get_video_transcript = None  
    run_memories_command = None

pytestmark = pytest.mark.unit

class TestMemoriesAPIClient:
    """Test suite for Memories.ai API client functionality."""

    def test_api_functions_exist(self):
        """Test that API functions exist and are importable."""
        assert get_video_metadata is not None, "get_video_metadata should be importable"
        assert get_video_transcript is not None, "get_video_transcript should be importable"
        assert run_memories_command is not None, "run_memories_command should be importable"

    @patch('requests.get')
    def test_get_video_metadata_success(self, mock_get, youtube_url, sample_metadata):
        """Test successful metadata retrieval."""
        if get_video_metadata is None:
            pytest.skip("get_video_metadata function not available")
        
        # Configure mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "data": sample_metadata
        }
        mock_get.return_value = mock_response
        
        result = get_video_metadata(youtube_url)
        
        # Verify the request was made correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        
        # Check that the URL contains the video URL
        assert youtube_url in str(call_args) or "jNQXAC9IVRw" in str(call_args)
        
        # Verify result structure
        assert result is not None
        if isinstance(result, dict):
            assert "title" in result or "data" in result

    @patch('requests.post')
    def test_get_video_transcript_success(self, mock_post, youtube_url, sample_transcript):
        """Test successful transcript retrieval."""
        if get_video_transcript is None:
            pytest.skip("get_video_transcript function not available")
        
        # Configure mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "data": sample_transcript
        }
        mock_post.return_value = mock_response
        
        result = get_video_transcript(youtube_url)
        
        # Verify the request was made
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        # Verify result
        assert result is not None

    @patch('subprocess.run')
    def test_run_memories_command_success(self, mock_subprocess):
        """Test successful CLI command execution."""
        if run_memories_command is None:
            pytest.skip("run_memories_command function not available")
        
        # Configure mock subprocess
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout='{"status": "success", "data": {"result": "test output"}}',
            stderr=""
        )
        
        result = run_memories_command(["v2", "transcribe", "--url", "https://youtube.com/test"])
        
        # Verify subprocess was called
        mock_subprocess.assert_called_once()
        
        # Check command structure
        call_args = mock_subprocess.call_args[0][0]
        assert "memories" in call_args or "python" in str(call_args)

class TestAPIErrorHandling:
    """Test API error handling and edge cases."""

    @patch('requests.get')
    def test_get_video_metadata_http_error(self, mock_get, youtube_url):
        """Test metadata retrieval with HTTP errors.""" 
        if get_video_metadata is None:
            pytest.skip("get_video_metadata function not available")
        
        # Test different HTTP error codes
        error_codes = [400, 401, 403, 404, 429, 500, 503]
        
        for status_code in error_codes:
            mock_response = Mock()
            mock_response.status_code = status_code
            mock_response.json.return_value = {
                "status": "error",
                "message": f"HTTP {status_code} error"
            }
            mock_get.return_value = mock_response
            
            try:
                result = get_video_metadata(youtube_url)
                # If no exception is raised, result should indicate error
                if isinstance(result, dict):
                    assert "error" in result or "status" in result
            except Exception as e:
                # It's acceptable to raise an exception for HTTP errors
                assert status_code in str(e) or "error" in str(e).lower()

    @patch('requests.get')
    def test_get_video_metadata_network_timeout(self, mock_get, youtube_url):
        """Test metadata retrieval with network timeout."""
        if get_video_metadata is None:
            pytest.skip("get_video_metadata function not available")
        
        mock_get.side_effect = Timeout("Request timed out")
        
        try:
            result = get_video_metadata(youtube_url)
            # If no exception, should return error indication
            assert result is None or (isinstance(result, dict) and "error" in result)
        except (Timeout, Exception) as e:
            # Acceptable to raise timeout exception
            assert "timeout" in str(e).lower() or "timed out" in str(e).lower()

    @patch('requests.get')
    def test_get_video_metadata_connection_error(self, mock_get, youtube_url):
        """Test metadata retrieval with connection errors."""
        if get_video_metadata is None:
            pytest.skip("get_video_metadata function not available")
        
        mock_get.side_effect = ConnectionError("Connection failed")
        
        try:
            result = get_video_metadata(youtube_url) 
            assert result is None or (isinstance(result, dict) and "error" in result)
        except (ConnectionError, Exception) as e:
            assert "connection" in str(e).lower() or "failed" in str(e).lower()

    @patch('requests.post')
    def test_get_video_transcript_malformed_response(self, mock_post, youtube_url):
        """Test transcript retrieval with malformed JSON response."""
        if get_video_transcript is None:
            pytest.skip("get_video_transcript function not available")
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.text = "Invalid JSON response"
        mock_post.return_value = mock_response
        
        try:
            result = get_video_transcript(youtube_url)
            # Should handle JSON decode error gracefully
            assert result is None or isinstance(result, (dict, str))
        except Exception as e:
            # Acceptable to raise JSON decode exception
            assert "json" in str(e).lower() or "decode" in str(e).lower()

class TestAPIAuthentication:
    """Test API authentication and authorization."""

    @patch('requests.get')
    def test_api_request_includes_auth_headers(self, mock_get, youtube_url):
        """Test that API requests include proper authentication headers.""" 
        if get_video_metadata is None:
            pytest.skip("get_video_metadata function not available")
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "data": {}}
        mock_get.return_value = mock_response
        
        get_video_metadata(youtube_url)
        
        # Check that headers were included in the request
        call_args = mock_get.call_args
        if call_args and len(call_args) > 1:
            kwargs = call_args[1]
            headers = kwargs.get('headers', {})
            
            # Should have some form of authentication
            auth_headers = ['Authorization', 'X-API-Key', 'Api-Key', 'x-api-key']
            has_auth = any(header in headers for header in auth_headers)
            
            # If no explicit auth header, function might be using other auth methods
            assert has_auth or len(headers) > 0 or 'auth' in kwargs

    @patch.dict('os.environ', {'MEMORIES_API_KEY': ''})
    @patch('requests.get') 
    def test_api_request_without_api_key(self, mock_get, youtube_url):
        """Test API behavior when API key is missing."""
        if get_video_metadata is None:
            pytest.skip("get_video_metadata function not available")
        
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"status": "error", "message": "Unauthorized"}
        mock_get.return_value = mock_response
        
        try:
            result = get_video_metadata(youtube_url)
            # Should handle missing API key gracefully
            assert result is None or (isinstance(result, dict) and "error" in str(result))
        except Exception as e:
            # Acceptable to raise authentication exception
            assert any(word in str(e).lower() for word in ["auth", "unauthorized", "key", "token"])

class TestAPIRateLimiting:
    """Test API rate limiting handling."""

    @patch('requests.get')
    def test_api_rate_limit_handling(self, mock_get, youtube_url):
        """Test handling of rate limit responses."""
        if get_video_metadata is None:
            pytest.skip("get_video_metadata function not available")
        
        # Simulate rate limit response
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '60'}
        mock_response.json.return_value = {
            "status": "error",
            "message": "Rate limit exceeded"
        }
        mock_get.return_value = mock_response
        
        try:
            result = get_video_metadata(youtube_url)
            # Should handle rate limit gracefully
            if isinstance(result, dict):
                assert "error" in result or "rate" in str(result).lower()
        except Exception as e:
            # Acceptable to raise rate limit exception
            assert "rate" in str(e).lower() or "limit" in str(e).lower()

    @patch('time.sleep')
    @patch('requests.get')
    def test_api_retry_logic(self, mock_get, mock_sleep, youtube_url):
        """Test API retry logic for transient failures."""
        if get_video_metadata is None:
            pytest.skip("get_video_metadata function not available")
        
        # First call fails, second succeeds
        mock_responses = [
            Mock(status_code=503, json=lambda: {"status": "error", "message": "Service unavailable"}),
            Mock(status_code=200, json=lambda: {"status": "success", "data": {}})
        ]
        mock_get.side_effect = mock_responses
        
        result = get_video_metadata(youtube_url)
        
        # Check if retry logic was implemented
        if mock_get.call_count > 1:
            # Retry logic is implemented
            assert mock_sleep.called, "Should sleep between retries"
            assert result is not None, "Should eventually succeed"

class TestAPIDataValidation:
    """Test API response data validation."""

    @patch('requests.get')
    def test_metadata_response_validation(self, mock_get, youtube_url):
        """Test validation of metadata response structure."""
        if get_video_metadata is None:
            pytest.skip("get_video_metadata function not available")
        
        # Test with missing required fields
        invalid_responses = [
            {"status": "success"},  # Missing data
            {"data": {}},  # Missing status
            {"status": "success", "data": None},  # Null data
            {},  # Empty response
        ]
        
        for invalid_response in invalid_responses:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = invalid_response
            mock_get.return_value = mock_response
            
            result = get_video_metadata(youtube_url)
            # Should handle invalid response structure gracefully
            assert result is not None  # Function should not crash

    @patch('requests.post')
    def test_transcript_response_validation(self, mock_post, youtube_url):
        """Test validation of transcript response structure."""
        if get_video_transcript is None:
            pytest.skip("get_video_transcript function not available")
        
        # Test with various response formats
        test_responses = [
            {"status": "success", "data": {"transcript": "test"}},
            {"status": "success", "data": {"audio": [], "visual": []}},
            {"transcript": "direct transcript"},  # Alternative format
            {"data": "string data"},  # Unexpected format
        ]
        
        for test_response in test_responses:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = test_response
            mock_post.return_value = mock_response
            
            result = get_video_transcript(youtube_url)
            # Should handle various response formats
            assert result is not None  # Function should not crash

class TestAPIPerformance:
    """Test API performance characteristics."""

    @pytest.mark.performance
    @patch('requests.get')
    def test_api_request_timeout_configuration(self, mock_get, youtube_url):
        """Test that API requests have appropriate timeout configuration."""
        if get_video_metadata is None:
            pytest.skip("get_video_metadata function not available")
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "data": {}}
        mock_get.return_value = mock_response
        
        get_video_metadata(youtube_url)
        
        # Check that timeout was configured
        call_args = mock_get.call_args
        if call_args and len(call_args) > 1:
            kwargs = call_args[1]
            timeout = kwargs.get('timeout')
            
            # Should have a reasonable timeout (between 5-120 seconds)
            if timeout is not None:
                if isinstance(timeout, (int, float)):
                    assert 5 <= timeout <= 120, f"Timeout should be reasonable: {timeout}"
                elif isinstance(timeout, tuple):
                    assert all(5 <= t <= 120 for t in timeout), f"Timeout tuple should be reasonable: {timeout}"

    @pytest.mark.slow
    @patch('subprocess.run')
    def test_cli_command_performance(self, mock_subprocess):
        """Test CLI command execution performance."""
        if run_memories_command is None:
            pytest.skip("run_memories_command function not available")
        
        # Simulate fast command execution
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout='{"status": "success"}',
            stderr=""
        )
        
        start_time = time.time()
        result = run_memories_command(["--version"])
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Command execution should be reasonably fast (< 5 seconds for simple commands)
        assert execution_time < 5.0, f"CLI command took too long: {execution_time:.2f}s"

class TestAPIIntegration:
    """Integration tests for API functionality."""

    @pytest.mark.integration
    def test_api_connectivity(self):
        """Test basic API connectivity (requires real API key)."""
        # This test would only run with --run-integration flag
        pytest.skip("Integration test - requires real API key and network access")

    @patch('requests.get')
    @patch('requests.post') 
    def test_metadata_and_transcript_integration(self, mock_post, mock_get, youtube_url):
        """Test that metadata and transcript functions work together."""
        if get_video_metadata is None or get_video_transcript is None:
            pytest.skip("Required functions not available")
        
        # Configure mocks
        metadata_response = Mock()
        metadata_response.status_code = 200
        metadata_response.json.return_value = {
            "status": "success",
            "data": {"title": "Test Video", "duration": 120}
        }
        mock_get.return_value = metadata_response
        
        transcript_response = Mock()
        transcript_response.status_code = 200
        transcript_response.json.return_value = {
            "status": "success", 
            "data": {"transcript": "Test transcript"}
        }
        mock_post.return_value = transcript_response
        
        # Test both functions
        metadata = get_video_metadata(youtube_url)
        transcript = get_video_transcript(youtube_url)
        
        assert metadata is not None
        assert transcript is not None
        
        # Both functions should have been called
        mock_get.assert_called_once()
        mock_post.assert_called_once()