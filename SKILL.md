---
name: Video Intelligence Suite
slug: video-intelligence-suite
version: 1.0.0
description: Comprehensive video analysis with Memories.ai CLI. Multi-platform support for YouTube, TikTok, Instagram, Twitter with AI transcription, metadata extraction, and visual scene analysis.
---

# Video Intelligence with Memories.ai CLI

The memories command provides fast video analysis across multiple platforms. A unified CLI interface gives you transcription, metadata, and AI visual analysis in one tool.

## Prerequisites

```bash
pip install memories-cli
export MEMORIES_API_KEY="your-api-key-here"
```

For setup details, see [https://github.com/Memories-ai-labs/memories-cli](https://github.com/Memories-ai-labs/memories-cli)

## Core Workflow

- **Analyze**: `python scripts/memories.py <video-url>` — full analysis with metadata + transcript
- **Metadata**: `memories v2 social metadata --platform youtube --video-url URL` — video info only
- **Transcript**: `memories v2 social transcript --platform youtube --video-url URL` — audio transcription  
- **MAI Analysis**: `memories v2 social mai-transcript --platform youtube --video-url URL` — visual + audio AI
- **Verify**: Check JSON response and extract insights

## Platform Support

| Platform | URL Format | Metadata | Transcript | MAI Analysis |
|----------|------------|----------|------------|-------------|
| YouTube | `youtube.com/watch?v=*` | ✅ | ✅ | ✅ |
| TikTok | `tiktok.com/@*/video/*` | ✅ | ❌ | ✅ |
| Instagram | `instagram.com/p/*` | ✅ | ❌ | ✅ |
| Twitter | `twitter.com/*/status/*` | ✅ | ❌ | ✅ |

## Commands

### Analysis
```bash
# Full video analysis (recommended)
python scripts/memories.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Analysis with MAI visual understanding
python scripts/memories.py "https://www.tiktok.com/@user/video/123" --mai

# Batch analysis
python scripts/memories.py --batch urls.txt
```

### Metadata Only
```bash
# YouTube video info
memories v2 social metadata \\
  --platform youtube \\
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \\
  --channel rapid

# TikTok video info  
memories v2 social metadata \\
  --platform tiktok \\
  --video-url "https://www.tiktok.com/@user/video/123" \\
  --channel rapid
```

### Transcription
```bash
# Audio transcript only (YouTube)
memories v2 social transcript \\
  --platform youtube \\
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \\
  --channel rapid

# MAI transcript (visual + audio)
memories v2 social mai-transcript \\
  --platform youtube \\
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \\
  --channel rapid
```

### Channels & Speed
```bash
# Fast processing
--channel rapid

# Higher quality (slower)
--channel quality
```

## Response Formats

### Metadata Response
```json
{
  "ok": true,
  "result": {
    "title": "Video Title",
    "description": "Video description text...",
    "lengthSeconds": 300,
    "viewCount": 12345,
    "channel": {
      "name": "Channel Name", 
      "handle": "@channelhandle"
    }
  }
}
```

### Transcript Response
```json
{
  "ok": true,
  "result": {
    "transcript": [
      {
        "text": "Hello world",
        "offset": 1000,
        "duration": 2000,
        "lang": "en"
      }
    ]
  }
}
```

### MAI Analysis Response
```json
{
  "ok": true,
  "result": {
    "videoTranscript": {
      "data": [
        {
          "text": "A person walking on a beach at sunset",
          "startTime": 0.0,
          "endTime": 3.0
        }
      ]
    },
    "audioTranscript": {
      "data": [
        {
          "text": "The waves are crashing gently",
          "startTime": 0.5,
          "endTime": 2.5
        }
      ]
    }
  }
}
```

## Error Handling

```json
{
  "ok": false,
  "error": "Invalid URL or platform not supported"
}
```

Common issues:
- **Invalid URL**: Check platform and URL format
- **Rate limiting**: Wait before retrying (10 requests/minute)
- **API key missing**: Set `MEMORIES_API_KEY` environment variable  
- **Network errors**: Retry with exponential backoff
- **Platform not supported**: Check supported platforms table

## Command Chaining

Commands can be chained for complex workflows:

```bash
# Get metadata, then transcript if video is short
python scripts/memories.py "$URL" --metadata-first && \\
  python scripts/memories.py "$URL" --transcript

# Batch process with error handling
for url in $(cat urls.txt); do
  python scripts/memories.py "$url" --mai || echo "Failed: $url"
done
```

## Advanced Usage

### Webhook Integration
```bash
# Async processing with webhooks
memories v2 social mai-transcript \\
  --platform youtube \\
  --video-url "$URL" \\
  --webhook-url "https://your-server.com/callback"
```

### Custom Processing
```bash
# Extract specific data
python scripts/memories.py "$URL" --extract title,duration,transcript

# Save results
python scripts/memories.py "$URL" --output results.json

# Filter by language
python scripts/memories.py "$URL" --lang en --transcript-only
```

## Testing

```bash
# Run test suite
python -m pytest tests/ -v --cov=scripts

# Test specific platform
python tests/test_platform_detection.py

# Performance benchmarks
python tests/test_performance.py
```

## Configuration

Environment variables:
- `MEMORIES_API_KEY` — Required API key
- `MEMORIES_CHANNEL` — Default channel (rapid/quality)
- `MEMORIES_WEBHOOK_URL` — Default webhook endpoint

Config file `~/.memories/config.json`:
```json
{
  "api_key": "your-key",
  "default_channel": "rapid",
  "webhook_url": "https://your-callback.com",
  "rate_limit": 10
}
```

## Global Options

| Option | Description |
|--------|-------------|
| `--mai` | Enable visual scene analysis |
| `--channel rapid/quality` | Processing speed/quality |
| `--output FILE` | Save results to file |
| `--webhook URL` | Async callback URL |
| `--extract FIELDS` | Extract specific fields only |
| `--batch FILE` | Process multiple URLs |
| `--retry N` | Max retry attempts |
| `--timeout N` | Request timeout seconds |

## Tips

- Always check response `"ok": true` before parsing results
- Use `rapid` channel for quick analysis, `quality` for accuracy  
- MAI analysis provides visual understanding but costs more
- Rate limit is 10 requests/minute per API key
- Batch processing: process sequentially to avoid rate limits
- YouTube supports both transcript and MAI, others only MAI

## Troubleshooting

- **API key invalid**: Check key format and permissions
- **Rate limited**: Wait 60 seconds, implement exponential backoff
- **Platform detection failed**: Verify URL format and supported platforms
- **Network timeout**: Increase timeout or retry with exponential backoff
- **MAI analysis failed**: Try with `--channel quality` or retry later

Run diagnostics:
```bash
python scripts/memories.py --doctor
```

## Use Cases

### Content Analysis
```bash
# Analyze TikTok for content themes
python scripts/memories.py "https://tiktok.com/@creator/video/123" --mai --extract themes,sentiment

# YouTube video summarization  
python scripts/memories.py "https://youtube.com/watch?v=abc" --extract title,transcript,summary
```

### Social Media Monitoring
```bash
# Monitor competitor content
python scripts/memories.py --batch competitor_urls.txt --extract engagement,topics

# Content moderation
python scripts/memories.py "$URL" --mai --extract safety,content_flags
```

### Research & Data Mining
```bash
# Extract educational content
python scripts/memories.py "$URL" --transcript --extract keywords,concepts,entities

# Trend analysis
python scripts/memories.py --batch trending_videos.txt --extract hashtags,metrics,themes
```

---

For detailed API reference and advanced features, see `references/` folder.