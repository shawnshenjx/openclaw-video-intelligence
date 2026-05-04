---
name: Video Intelligence Suite
slug: video-intelligence-suite
version: 1.0.0
description: Comprehensive video analysis with Memories.ai CLI. Multi-platform support for YouTube, TikTok, Instagram, Twitter with AI transcription, metadata extraction, and visual scene analysis.
---

# Video Intelligence with Memories.ai CLI

The memories command provides fast video analysis across multiple platforms. A unified CLI interface gives you transcription, metadata, and AI visual analysis in one tool.

## Understanding Memories.ai APIs

### 🏗️ V1 API (Legacy Scraping)
**Purpose**: Basic video scraping and metadata extraction
- **What it does**: Downloads video info, uploads files, basic search
- **Use when**: Simple metadata extraction, file uploads, legacy systems
- **Limitations**: No AI analysis, limited platform support
- **Cost**: Lower ($0.01/GB upload, $0.001/scrape)

### 🧠 V2 API (AI-Powered Analysis) 
**Purpose**: Advanced video intelligence with AI
- **What it does**: AI transcription, visual scene analysis, social media intelligence
- **Use when**: Content analysis, video understanding, social media monitoring
- **Features**: MAI (visual+audio), multi-platform support, webhooks
- **Cost**: Higher (~$0.11 per 40s video) but includes AI processing

### 🎯 When to Use Which?

| Task | API | Why |
|------|-----|-----|
| Get video title/duration | V1 | Simple, fast, cheap |
| Upload video files | V1 | File management focus |
| **Understand video content** | **V2** | **AI analysis needed** |
| **Transcribe speech** | **V2** | **Audio-to-text** |
| **Analyze TikTok/Instagram** | **V2** | **Only V2 supports these** |
| **Content moderation** | **V2** | **Needs AI understanding** |

**💡 Recommendation**: Use V2 for most analysis tasks. V1 is mainly for legacy support.

## ⚡ Quick Decision Guide

**"I want to understand what's in this video"** → **V2 MAI Analysis**
```bash
python scripts/memories.py "VIDEO_URL" --mai
```

**"I just need the video title and duration"** → **V2 Metadata**
```bash
memories v2 social metadata --platform youtube --video-url "URL" --channel rapid
```

**"I need to upload a video file to storage"** → **V1 Upload**
```bash
memories v1 upload --file "video.mp4"
```

**"I'm analyzing TikTok/Instagram content"** → **V2 Only**
```bash
# V1 doesn't support these platforms
python scripts/memories.py "TIKTOK_URL" --mai
```

## Prerequisites

```bash
pip install memories-cli
export MEMORIES_API_KEY="your-api-key-here"
```

For setup details, see [https://github.com/Memories-ai-labs/memories-cli](https://github.com/Memories-ai-labs/memories-cli)

## Core Workflow

### 🎯 Quick Start (Recommended)
```bash
# Full AI analysis (V2) - most common use case
python scripts/memories.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --mai
```

### 📋 Step-by-Step Analysis
1. **Basic Info** (V2): `memories v2 social metadata --platform youtube --video-url URL`
2. **Speech-to-Text** (V2): `memories v2 social transcript --platform youtube --video-url URL`  
3. **AI Visual+Audio** (V2): `memories v2 social mai-transcript --platform youtube --video-url URL`
4. **Verify**: Check JSON response and extract insights

### 🔄 V1 vs V2 Commands
```bash
# V1 (Legacy) - Basic scraping
memories v1 scrape --platform youtube --url URL
memories v1 upload --file video.mp4

# V2 (Modern) - AI-powered analysis  
memories v2 social metadata --platform youtube --video-url URL
memories v2 social mai-transcript --platform youtube --video-url URL
```

## Platform Support

### V2 API (Modern - Recommended)
| Platform | URL Format | Metadata | Transcript | MAI Analysis |
|----------|------------|----------|------------|-------------|
| YouTube | `youtube.com/watch?v=*` | ✅ | ✅ | ✅ |
| TikTok | `tiktok.com/@*/video/*` | ✅ | ❌ | ✅ |
| Instagram | `instagram.com/p/*` | ✅ | ❌ | ✅ |
| Twitter | `twitter.com/*/status/*` | ✅ | ❌ | ✅ |

### V1 API (Legacy)
| Platform | URL Format | Basic Scraping | Upload Support |
|----------|------------|----------------|----------------|
| YouTube | `youtube.com/watch?v=*` | ✅ | ❌ |
| General | Any platform | Limited | ✅ |

**💡 Key Difference**: V2 provides AI-powered analysis, V1 only does basic scraping.

## V1 vs V2 Detailed Comparison

### 🏗️ V1 API - Legacy Scraping
**Best for**: File uploads, basic metadata, legacy systems

**Capabilities**:
- ✅ Upload video files to Memories.ai storage
- ✅ Basic metadata extraction (title, duration, views)
- ✅ Simple video search and listing
- ✅ Download videos from storage
- ❌ No AI analysis or transcription
- ❌ Limited platform support
- ❌ No visual scene understanding

**Cost**: $0.01/GB upload + $0.001/scrape + storage fees

### 🧠 V2 API - AI-Powered Analysis  
**Best for**: Video understanding, content analysis, social media intelligence

**Capabilities**:
- ✅ **MAI Analysis**: Visual scene understanding + audio transcription
- ✅ **Multi-platform**: YouTube, TikTok, Instagram, Twitter
- ✅ **AI Transcription**: Speech-to-text with timestamps
- ✅ **Visual Intelligence**: Scene descriptions, objects, emotions
- ✅ **Webhook Support**: Async processing for large videos
- ✅ **Advanced Metadata**: Engagement metrics, hashtags, music
- ❌ No direct file uploads (URL-based analysis)

**Cost**: ~$0.11 per 40-second video (includes AI processing)

### 🎯 Which Should You Use?

**Use V1 when**:
- ✅ Uploading video files to storage
- ✅ Building file management systems
- ✅ Working with legacy integrations
- ✅ Need lowest possible cost

**Use V2 when** (🔥 **Recommended for most cases**):
- ✅ Analyzing social media content
- ✅ Understanding what's in videos
- ✅ Building content moderation systems
- ✅ Extracting insights from video content
- ✅ Transcribing video speech
- ✅ Analyzing competitor content

## Commands

### V2 Analysis (AI-Powered - Recommended)
```bash
# Full AI video analysis (V2)
python scripts/memories.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --mai

# Quick metadata only (V2)
python scripts/memories.py "https://www.tiktok.com/@user/video/123" --metadata-only

# Batch AI analysis (V2)
python scripts/memories.py --batch urls.txt --mai
```

### V1 Analysis (Legacy Scraping)
```bash
# Basic scraping (V1)
memories v1 scrape --platform youtube --url "VIDEO_URL"

# Upload file (V1)
memories v1 upload --file "video.mp4" --title "My Video"

# List uploaded videos (V1)
memories v1 list --limit 10
```

### V2 Metadata (AI Platform)
```bash
# YouTube video info (V2)
memories v2 social metadata \\
  --platform youtube \\
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \\
  --channel rapid

# TikTok video info (V2 - V1 doesn't support TikTok)
memories v2 social metadata \\
  --platform tiktok \\
  --video-url "https://www.tiktok.com/@user/video/123" \\
  --channel rapid
```

### V1 Metadata (Legacy)
```bash
# Basic video info (V1)
memories v1 info --video-no 12345

# Search videos (V1)
memories v1 search --query "tutorial" --limit 20
```

### V2 Transcription (AI-Powered)
```bash
# Audio transcript only (V2 - YouTube only)
memories v2 social transcript \\
  --platform youtube \\
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \\
  --channel rapid

# MAI transcript: Visual scenes + Audio (V2 - All platforms)
memories v2 social mai-transcript \\
  --platform youtube \\
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \\
  --channel rapid
```

**💡 Note**: V1 has NO transcription capabilities. Only V2 can convert speech to text and understand visual content.

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