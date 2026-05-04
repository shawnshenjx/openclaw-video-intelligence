# Memories.ai V1 API Reference

The V1 API provides basic video scraping and metadata extraction capabilities.

## Base Configuration

```bash
export MEMORIES_API_KEY="sk-652f3f23d99ad68c96b019ffb3376e74"
MEMORIES_V1_BASE_URL="https://api.memories.ai/serve/api/v1"
```

## Upload Operations

### Upload by URL
```bash
memories v1 upload-url \\
  --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \\
  --callback "https://your-webhook.com/callback" \\
  --unique-id "video-001"
```

**Response:**
```json
{
  "status": "success",
  "video_no": 12345,
  "task_id": "upload-abc123",
  "callback_url": "https://your-webhook.com/callback"
}
```

### Upload Local File
```bash
memories v1 upload \\
  --file "/path/to/video.mp4" \\
  --title "My Video" \\
  --description "Video description"
```

## Download Operations

### Download Video
```bash
memories v1 download \\
  --video-no 12345 \\
  --output "./downloaded_video.mp4"
```

### Get Download URL
```bash
memories v1 download-url --video-no 12345
```

**Response:**
```json
{
  "download_url": "https://cdn.memories.ai/videos/12345.mp4",
  "expires_at": "2026-05-04T12:00:00Z"
}
```

## Metadata Operations

### Video Information
```bash
memories v1 info --video-no 12345
```

**Response:**
```json
{
  "video_no": 12345,
  "title": "Video Title",
  "description": "Video description",
  "duration": 180,
  "file_size": 50331648,
  "format": "mp4",
  "resolution": "1920x1080",
  "uploaded_at": "2026-05-04T01:00:00Z",
  "status": "processed"
}
```

### List Videos
```bash
memories v1 list --limit 10 --offset 0
```

**Response:**
```json
{
  "videos": [
    {
      "video_no": 12345,
      "title": "Video Title",
      "uploaded_at": "2026-05-04T01:00:00Z",
      "status": "processed"
    }
  ],
  "total": 100,
  "limit": 10,
  "offset": 0
}
```

## Search Operations

### Search Videos
```bash
memories v1 search \\
  --query "tutorial" \\
  --limit 20 \\
  --sort "relevance"
```

**Response:**
```json
{
  "results": [
    {
      "video_no": 12345,
      "title": "Python Tutorial",
      "description": "Learn Python basics",
      "score": 0.95,
      "thumbnail": "https://cdn.memories.ai/thumbs/12345.jpg"
    }
  ],
  "total_results": 50,
  "query_time": 0.045
}
```

## Platform-Specific Scraping

### YouTube Scraping
```bash
memories v1 scrape \\
  --platform youtube \\
  --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \\
  --extract metadata,comments,captions
```

### TikTok Scraping
```bash
memories v1 scrape \\
  --platform tiktok \\
  --url "https://www.tiktok.com/@user/video/123" \\
  --extract metadata,hashtags,music
```

## Webhook Integration

### Setup Webhook
```bash
memories v1 webhook \\
  --url "https://your-server.com/webhook" \\
  --events "upload_complete,processing_done,error" \\
  --secret "your-webhook-secret"
```

### Webhook Payload Examples

**Upload Complete:**
```json
{
  "event": "upload_complete",
  "video_no": 12345,
  "status": "uploaded",
  "timestamp": "2026-05-04T01:00:00Z",
  "metadata": {
    "duration": 180,
    "file_size": 50331648
  }
}
```

**Processing Done:**
```json
{
  "event": "processing_done",
  "video_no": 12345,
  "status": "processed",
  "timestamp": "2026-05-04T01:05:00Z",
  "results": {
    "thumbnail": "https://cdn.memories.ai/thumbs/12345.jpg",
    "preview": "https://cdn.memories.ai/previews/12345.gif"
  }
}
```

## Error Handling

### Common Error Responses
```json
{
  "error": "invalid_url",
  "message": "The provided URL is not valid or accessible",
  "code": 400
}
```

```json
{
  "error": "rate_limit_exceeded",
  "message": "Rate limit of 10 requests per minute exceeded",
  "code": 429,
  "retry_after": 60
}
```

```json
{
  "error": "video_not_found",
  "message": "Video with video_no 12345 not found",
  "code": 404
}
```

### Rate Limits

- **Upload**: 5 uploads per minute
- **Download**: 20 downloads per minute  
- **API calls**: 100 requests per minute
- **Scraping**: 10 scrapes per minute

### Retry Logic
```bash
# Python example with exponential backoff
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

## Authentication

### API Key Format
```
sk-[32-character-hex-string]
```

### Headers
```bash
curl -H "Authorization: sk-652f3f23d99ad68c96b019ffb3376e74" \\
     "https://api.memories.ai/serve/api/v1/info?video_no=12345"
```

## Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid API key |
| 404 | Not Found - Resource doesn't exist |
| 429 | Rate Limited - Too many requests |
| 500 | Internal Error - Server issue |

## Pricing (V1)

- **Upload**: $0.01 per GB
- **Storage**: $0.001 per GB per month
- **Download**: $0.005 per GB transferred
- **API calls**: Free up to 10,000/month
- **Scraping**: $0.001 per page scraped

## Migration to V2

V1 is legacy. New projects should use V2 for:
- Better AI analysis capabilities
- Improved error handling  
- More platform support
- Enhanced webhook system
- Better rate limits

See `v2-api.md` for V2 documentation.