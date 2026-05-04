# Memories.ai V2 API Reference

The V2 API provides advanced AI-powered video analysis, transcription, and multi-platform support.

## Base Configuration

```bash
export MEMORIES_API_KEY="sk-mavi-mjLNMGVXHt52ZPvEIkx5QrsQEv6Z52GjvXa0MISOgAP5ckMGBzybxfMH9B-1tvUNFhbmDlI8juoFtJjoQJQMhwno9qDBidAblsfJMwL1NTiAqtSYgXnZKrD-uWxHFWkZ"
MEMORIES_V2_BASE_URL="https://mavi-backend.memories.ai/serve/api/v2"
```

**Important**: V2 uses different auth format - no "Bearer" prefix:
```bash
curl -H "Authorization: sk-mavi-..." "https://mavi-backend.memories.ai/serve/api/v2/status"
```

## Social Media Analysis

### YouTube Video Analysis

#### Metadata Only
```bash
memories v2 social metadata \\
  --platform youtube \\
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \\
  --channel rapid
```

**Response:**
```json
{
  "code": "0000",
  "data": {
    "title": "Rick Astley - Never Gonna Give You Up",
    "description": "The official video for Rick Astley...",
    "lengthSeconds": 213,
    "viewCount": 1500000000,
    "channel": {
      "name": "Rick Astley",
      "handle": "@RickAstley",
      "subscriber_count": 5000000
    },
    "upload_date": "2009-10-25",
    "tags": ["music", "80s", "pop"],
    "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
  }
}
```

#### Audio Transcript
```bash
memories v2 social transcript \\
  --platform youtube \\
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \\
  --channel rapid
```

**Response:**
```json
{
  "code": "0000", 
  "data": {
    "transcript": [
      {
        "text": "We're no strangers to love",
        "start": 0.5,
        "end": 2.8,
        "confidence": 0.98
      },
      {
        "text": "You know the rules and so do I",
        "start": 2.8,
        "end": 5.2,
        "confidence": 0.96
      }
    ],
    "language": "en",
    "duration": 213.0
  }
}
```

#### MAI Analysis (Visual + Audio)
```bash
memories v2 social mai-transcript \\
  --platform youtube \\
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \\
  --channel rapid
```

**Response (Async Task):**
```json
{
  "code": "0000",
  "data": {
    "task_id": "mai-yt-abc123def456",
    "status": "processing",
    "estimated_completion": "2026-05-04T02:10:00Z"
  }
}
```

**Webhook Callback:**
```json
{
  "task_id": "mai-yt-abc123def456",
  "status": "completed",
  "data": {
    "videoTranscript": {
      "data": [
        {
          "text": "A man in a suit dancing in a warehouse with vintage equipment and workers in the background",
          "startTime": 0.0,
          "endTime": 4.2,
          "confidence": 0.94
        }
      ]
    },
    "audioTranscript": {
      "data": [
        {
          "text": "We're no strangers to love",
          "startTime": 0.5,
          "endTime": 2.8,
          "confidence": 0.98
        }
      ]
    },
    "metadata": {
      "total_scenes": 45,
      "total_speech_segments": 28,
      "processing_time": 34.2
    }
  }
}
```

### TikTok Analysis

#### Metadata + MAI Analysis
```bash
memories v2 social mai-transcript \\
  --platform tiktok \\
  --video-url "https://www.tiktok.com/@username/video/7234567890123456789" \\
  --channel rapid
```

**Response:**
```json
{
  "code": "0000",
  "data": {
    "task_id": "mai-tiktok-xyz789",
    "metadata": {
      "title": "Amazing dance moves! 🔥",
      "creator": "@username",
      "likes": 150000,
      "comments": 5000,
      "shares": 2000,
      "duration": 15.5,
      "music": {
        "title": "Original sound - username",
        "id": "music-123456"
      },
      "hashtags": ["#dance", "#viral", "#fyp"],
      "upload_date": "2026-05-03"
    }
  }
}
```

### Instagram Analysis

#### Reels and Video Posts
```bash
memories v2 social mai-transcript \\
  --platform instagram \\
  --video-url "https://www.instagram.com/p/ABC123DEF456/" \\
  --channel quality
```

### Twitter/X Video Analysis

```bash
memories v2 social mai-transcript \\
  --platform twitter \\
  --video-url "https://twitter.com/user/status/1234567890123456789" \\
  --channel rapid
```

## Advanced Features

### Async Task Polling
```bash
# Check task status
memories v2 task status --task-id "mai-yt-abc123def456"

# Poll until completion
memories v2 task poll --task-id "mai-yt-abc123def456" --timeout 300
```

### Batch Processing
```bash
# Process multiple URLs
memories v2 social batch \\
  --platform youtube \\
  --urls-file "video_urls.txt" \\
  --channel rapid \\
  --webhook-url "https://your-server.com/batch-callback"
```

**URLs File Format:**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=abc123def456  
https://www.tiktok.com/@user/video/789
```

### Custom Analysis Parameters
```bash
memories v2 social mai-transcript \\
  --platform youtube \\
  --video-url "$URL" \\
  --channel quality \\
  --language-hint "en" \\
  --scene-detection-threshold 0.8 \\
  --max-scenes 100 \\
  --include-emotions \\
  --include-objects \\
  --include-text-ocr
```

## Webhook System

### Setup Webhook URL
```bash
export MEMORIES_WEBHOOK_URL="https://your-server.com/memories-callback"

# Or pass directly to commands
memories v2 social mai-transcript \\
  --video-url "$URL" \\
  --webhook-url "https://your-callback.com/webhook"
```

### Webhook Payload Structure
```json
{
  "webhook_id": "webhook-abc123",
  "task_id": "mai-yt-def456", 
  "platform": "youtube",
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "status": "completed|failed|processing",
  "timestamp": "2026-05-04T02:00:00Z",
  "data": {
    // Same as direct API response
  },
  "error": null, // Present if status=failed
  "metadata": {
    "processing_time_seconds": 34.2,
    "cost_usd": 0.11,
    "api_version": "v2.1"
  }
}
```

### Webhook Verification
```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

## Error Handling

### Error Response Format
```json
{
  "code": "4001",
  "message": "Invalid video URL or platform not supported",
  "details": {
    "url": "https://invalid-url.com",
    "platform": "youtube",
    "validation_errors": ["URL format invalid"]
  }
}
```

### Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 0000 | Success | - |
| 4001 | Invalid URL | Check URL format and accessibility |
| 4002 | Platform not supported | Use YouTube, TikTok, Instagram, or Twitter |
| 4003 | Video unavailable | Video may be private/deleted |
| 4291 | Rate limit exceeded | Wait 60 seconds, implement backoff |
| 5001 | Processing failed | Retry with different channel |
| 5002 | Webhook delivery failed | Check webhook URL accessibility |

### Retry Strategy
```python
import time
import random

async def retry_mai_analysis(video_url, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = await memories_v2_mai_transcript(video_url)
            if result.code == "0000":
                return result
        except RateLimitError:
            wait_time = min(60 * (2 ** attempt), 300) + random.uniform(0, 10)
            await asyncio.sleep(wait_time)
        except ProcessingError:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(30)  # Processing errors usually temporary
    
    raise Exception("Max retries exceeded")
```

## Rate Limits & Pricing

### Rate Limits (per API key)
- **Metadata**: 60 requests/minute
- **Simple Transcript**: 30 requests/minute  
- **MAI Analysis**: 10 requests/minute
- **Batch Processing**: 5 batches/hour

### Pricing Structure
- **Base Cost**: $0.10 per analysis
- **Token Usage**: 
  - Input tokens: $0.45 per 1M tokens
  - Output tokens: $3.75 per 1M tokens
- **Duration**: $0.0001 per second of video
- **Example**: 40-second video ≈ $0.11 total

### Cost Optimization
```bash
# Use rapid channel for cost-effective analysis
--channel rapid  # ~30% faster, ~20% cheaper

# Batch process for volume discounts
--batch-size 10  # 10% discount on batch >10 videos

# Skip expensive features if not needed
--no-ocr --no-emotions --no-objects  # Reduces cost ~25%
```

## Advanced Configuration

### Channel Options
| Channel | Speed | Quality | Cost | Use Case |
|---------|-------|---------|------|----------|
| rapid | Fast | Good | Lower | Real-time analysis |
| quality | Slower | Excellent | Higher | Production analysis |

### Custom Model Parameters
```bash
memories v2 social mai-transcript \\
  --model-version "2.1" \\
  --temperature 0.3 \\
  --max-tokens 4000 \\
  --scene-detection-model "enhanced" \\
  --audio-model "whisper-large-v3"
```

### Regional Endpoints
```bash
# US West (default)
MEMORIES_V2_REGION="us-west"

# Europe 
MEMORIES_V2_REGION="eu-central"

# Asia Pacific
MEMORIES_V2_REGION="ap-southeast"
```

## Integration Examples

### Node.js Integration
```javascript
const axios = require('axios');

async function analyzeVideo(videoUrl, platform = 'youtube') {
    const response = await axios.post(
        'https://mavi-backend.memories.ai/serve/api/v2/social/mai-transcript',
        {
            video_url: videoUrl,
            platform: platform,
            channel: 'rapid'
        },
        {
            headers: {
                'Authorization': process.env.MEMORIES_API_KEY,
                'Content-Type': 'application/json'
            }
        }
    );
    
    return response.data;
}
```

### Python Integration
```python
import requests
import os

def analyze_video(video_url, platform='youtube'):
    response = requests.post(
        'https://mavi-backend.memories.ai/serve/api/v2/social/mai-transcript',
        json={
            'video_url': video_url,
            'platform': platform,
            'channel': 'rapid'
        },
        headers={
            'Authorization': os.environ['MEMORIES_API_KEY']
        }
    )
    
    return response.json()
```

## Migration from V1

### Key Differences
| Feature | V1 | V2 |
|---------|----|----|
| Auth Header | `Authorization: Bearer sk-...` | `Authorization: sk-mavi-...` |
| Base URL | `api.memories.ai/serve/api/v1` | `mavi-backend.memories.ai/serve/api/v2` |
| Response Format | Various | Standardized `{code, data}` |
| AI Analysis | Basic | Advanced MAI with scenes |
| Platform Support | Limited | YouTube, TikTok, IG, Twitter |
| Async Processing | Limited | Full webhook support |

### Migration Checklist
- [ ] Update API keys (V2 keys start with `sk-mavi-`)
- [ ] Change base URL to V2 endpoint
- [ ] Update auth header format (remove "Bearer")
- [ ] Adapt to new response format
- [ ] Implement webhook handling for async tasks
- [ ] Update error handling for new error codes