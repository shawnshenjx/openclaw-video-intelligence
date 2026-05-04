"""
pytest configuration and shared fixtures for Memories.ai CLI tests.

This module provides:
- Test configuration settings
- Common fixtures for mocking
- Sample data for testing
- Helper utilities for test setup/teardown
"""

import pytest
import json
import os
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Test configuration
pytest_plugins = []

@pytest.fixture(scope="session")
def test_data_dir():
    """Get the fixtures directory path."""
    return Path(__file__).parent / "fixtures"

@pytest.fixture(scope="session") 
def sample_urls(test_data_dir):
    """Load sample URLs for testing."""
    with open(test_data_dir / "test_urls.json", "r") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def sample_responses(test_data_dir):
    """Load sample API responses for testing."""
    with open(test_data_dir / "sample_responses.json", "r") as f:
        return json.load(f)

@pytest.fixture
def mock_subprocess():
    """Mock subprocess.run for CLI command testing."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Mock command output",
            stderr=""
        )
        yield mock_run

@pytest.fixture
def mock_requests():
    """Mock requests for API testing."""
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post:
        
        # Configure mock responses
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "data": {}}
        mock_response.text = '{"status": "success", "data": {}}'
        
        mock_get.return_value = mock_response
        mock_post.return_value = mock_response
        
        yield {
            'get': mock_get,
            'post': mock_post,
            'response': mock_response
        }

@pytest.fixture
def youtube_url():
    """Sample YouTube URL for testing."""
    return "https://www.youtube.com/watch?v=jNQXAC9IVRw"

@pytest.fixture  
def tiktok_url():
    """Sample TikTok URL for testing."""
    return "https://www.tiktok.com/@user/video/1234567890123456789"

@pytest.fixture
def instagram_url():
    """Sample Instagram URL for testing.""" 
    return "https://www.instagram.com/p/ABC123DEF456/"

@pytest.fixture
def twitter_url():
    """Sample Twitter URL for testing."""
    return "https://twitter.com/user/status/1234567890123456789"

@pytest.fixture
def invalid_url():
    """Invalid URL for error testing."""
    return "https://example.com/not-a-video"

@pytest.fixture
def sample_metadata():
    """Sample video metadata for testing."""
    return {
        "title": "Test Video",
        "description": "A test video for unit testing",
        "duration": "00:02:30",
        "view_count": 1000,
        "channel": "Test Channel",
        "upload_date": "2023-01-15"
    }

@pytest.fixture
def sample_transcript():
    """Sample transcript data for testing."""
    return {
        "audio": [
            {"start": 0.0, "end": 2.5, "text": "Hello and welcome to this test video"},
            {"start": 2.5, "end": 5.0, "text": "This is a sample transcript for testing"},
            {"start": 5.0, "end": 7.5, "text": "Thank you for watching"}
        ],
        "visual": [
            {"timestamp": 0.0, "description": "Person speaking to camera"},
            {"timestamp": 2.5, "description": "Text overlay appears on screen"}, 
            {"timestamp": 5.0, "description": "Video transitions to end screen"}
        ]
    }

@pytest.fixture
def mock_memories_api():
    """Mock Memories.ai API responses."""
    api_responses = {
        "transcript": {
            "status_code": 200,
            "json": {
                "status": "success",
                "data": {
                    "transcript": "This is a test transcript",
                    "duration": 150,
                    "language": "en"
                }
            }
        },
        "metadata": {
            "status_code": 200,
            "json": {
                "status": "success", 
                "data": {
                    "title": "Test Video",
                    "description": "Test description",
                    "duration": 150
                }
            }
        },
        "analysis": {
            "status_code": 200,
            "json": {
                "status": "success",
                "data": {
                    "summary": "Test video analysis",
                    "key_points": ["Point 1", "Point 2"],
                    "sentiment": "positive"
                }
            }
        }
    }
    
    def mock_response(endpoint):
        """Return mock response for given endpoint."""
        mock_resp = Mock()
        if 'transcript' in endpoint:
            response_data = api_responses['transcript']
        elif 'metadata' in endpoint:
            response_data = api_responses['metadata'] 
        else:
            response_data = api_responses['analysis']
            
        mock_resp.status_code = response_data['status_code']
        mock_resp.json.return_value = response_data['json']
        return mock_resp
    
    return mock_response

@pytest.fixture
def temp_output_file(tmp_path):
    """Temporary file for testing output."""
    output_file = tmp_path / "test_output.json"
    yield str(output_file)
    # Cleanup is automatic with tmp_path

@pytest.fixture
def set_test_env_vars():
    """Set test environment variables."""
    original_env = os.environ.copy()
    
    # Set test environment
    os.environ.update({
        'MEMORIES_API_KEY': 'test_api_key_12345',
        'MEMORIES_API_BASE': 'https://api.test.memories.ai',
        'PYTHONPATH': str(Path(__file__).parent.parent)
    })
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture(autouse=True)
def setup_test_environment(set_test_env_vars):
    """Automatically set up test environment for each test."""
    pass

# Test markers
def pytest_configure(config):
    """Configure custom test markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests requiring API access"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance benchmarks"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as fast unit tests"
    )

# Pytest configuration options
def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-slow", action="store_true", default=False, 
        help="run slow tests"
    )
    parser.addoption(
        "--run-integration", action="store_true", default=False,
        help="run integration tests (requires API key)"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection based on command line options."""
    if not config.getoption("--run-slow"):
        skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
    
    if not config.getoption("--run-integration"):
        skip_integration = pytest.mark.skip(reason="need --run-integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)