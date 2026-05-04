---
name: Video Intelligence Platform
slug: video-intelligence-platform
version: 1.5.1
description: Enterprise video intelligence platform for AI agents. Multi-platform analysis (YouTube, TikTok, Instagram, Twitter) with advanced AI transcription, visual scene understanding, and comprehensive API integration. Compatible with OpenClaw, Claude Code, Cursor, and 50+ agent platforms.
---

# Video Intelligence Platform

**Professional video analysis platform for AI agents.** The Video Intelligence Platform provides enterprise-grade video understanding capabilities through a unified CLI interface, delivering transcription, metadata extraction, and advanced AI visual analysis across multiple social media platforms. Compatible with all major AI agent ecosystems including OpenClaw, Claude Code, Cursor, and Skills.sh standard.

## Understanding Memories.ai APIs

### 🗄️ V1 API (Video Data Hosting)
**Purpose**: Managed video storage and search platform
- **What it does**: Video hosting, persistent storage, search database, file management
- **Use when**: Building video platforms, need persistent storage, video libraries
- **Benefits**: No need to setup your own database, built-in search, file hosting
- **Cost**: $0.01/GB upload + storage fees, includes database and hosting

### ⚛️ V2 API (Atomic Intelligence Capabilities) 
**Purpose**: Stateless, atomic video analysis functions
- **What it does**: Pure analysis functions - transcription, visual understanding, metadata extraction
- **Use when**: Need specific AI capabilities, integrate with existing systems
- **Benefits**: Stateless design, composable functions, no storage overhead
- **Cost**: ~$0.11 per 40s video, pay-per-analysis, no storage costs

### 🎯 When to Use Which?

| Use Case | API | Why |
|----------|-----|-----|
| **Build video platform** | **V1** | **Need persistent storage + search** |
| **Video library management** | **V1** | **Database included, no setup needed** |
| Upload and store videos | V1 | Managed hosting service |
| Search across video collection | V1 | Built-in search database |
| **Analyze external videos** | **V2** | **Stateless analysis functions** |
| **Transcribe speech** | **V2** | **Atomic AI capability** |
| **Understand video content** | **V2** | **Pure analysis, no storage** |
| **Integrate AI into existing system** | **V2** | **Composable functions** |

**💡 Architecture Choice**: 
- **V1** = Video hosting platform (like YouTube backend)
- **V2** = Analysis microservices (like transcription API)

## ⚡ Quick Decision Guide

**"I want to understand what's in this video"** → **V2 Analysis Functions**
```bash
python scripts/memories.py "VIDEO_URL" --mai
```

**"I'm building a video platform and need storage"** → **V1 Hosting Platform**
```bash
memories v1 upload --file "video.mp4" --title "My Video"
```

**"I need to search through my video library"** → **V1 Database**
```bash
memories v1 search --query "tutorial" --limit 20
```

**"I'm analyzing external social media content"** → **V2 Atomic Functions**
```bash
# V2 is designed for analyzing external URLs
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
# V1 - Video hosting platform
memories v1 scrape --platform youtube --url URL
memories v1 upload --file video.mp4

# V2 - Atomic intelligence functions
memories v2 social metadata --platform youtube --video-url URL
memories v2 social mai-transcript --platform youtube --video-url URL
```

## Platform Support

### V2 API (Modern - Recommended)
| Platform | URL Format | Metadata | Transcript | MAI Analysis |
|----------|------------|----------|------------|-------------|
| YouTube | `youtube.com/watch?v=*` | ✅ | ✅ | ✅ |
| TikTok | `tiktok.com/@*/video/*` | ✅ | ✅ | ✅ |
| Instagram | `instagram.com/p/*` | ✅ | ✅ | ✅ |
| Twitter | `twitter.com/*/status/*` | ✅ | ✅ | ✅ |

### V1 API (Video Hosting Platform)
| Function | Support | Description |
|----------|---------|-------------|
| File Upload | ✅ | Store videos in Memories.ai hosting |
| Database Search | ✅ | Search through your video library |
| Download/Stream | ✅ | Serve videos from storage |
| External URL Analysis | ❌ | Use V2 for analyzing external videos |

**💡 Key Difference**: 
- **V1** = Your video hosting platform (like building your own YouTube)
- **V2** = Analysis tools for any video URL (like AI microservices)

## V1 vs V2 Detailed Comparison

### 🗄️ V1 API - Video Data Hosting
**Best for**: Building video platforms, managing video libraries, persistent storage

**Architecture**: Stateful platform with managed database
**Capabilities**:
- ✅ **Video Hosting**: Upload, store, and serve video files
- ✅ **Search Database**: Built-in video search without setting up your own DB
- ✅ **Metadata Management**: Persistent video information storage
- ✅ **File Operations**: Download, list, organize video collections
- ✅ **Platform Features**: User management, playlists, video libraries
- ❌ No AI analysis capabilities (pure hosting/storage)

**Cost**: $0.01/GB upload + storage fees (includes database hosting)

### ⚛️ V2 API - Atomic Intelligence Functions  
**Best for**: Adding AI analysis to existing systems, stateless operations

**Architecture**: Stateless microservices, pure functions
**Capabilities**:
- ✅ **Atomic AI Functions**: Transcription, visual analysis, metadata extraction
- ✅ **Multi-platform Analysis**: YouTube, TikTok, Instagram, Twitter
- ✅ **Composable**: Use only the analysis functions you need
- ✅ **Stateless**: No storage, no database, pure input→output
- ✅ **Integration-friendly**: Works with any existing video storage system
- ❌ No file storage or hosting capabilities

**Cost**: ~$0.11 per 40-second analysis (pay-per-use, no storage costs)

### 🎯 Architectural Decision Guide

**Use V1 (Data Hosting) when**:
- ✅ Building a video platform (like YouTube, Vimeo)
- ✅ Need persistent video storage and database
- ✅ Want search functionality without setting up databases
- ✅ Managing large video libraries
- ✅ Need video hosting infrastructure

**Use V2 (Atomic Functions) when**:
- ✅ Adding AI analysis to existing systems
- ✅ Need specific analysis capabilities (transcription, visual understanding)
- ✅ Analyzing external videos (social media, competitor content)
- ✅ Building microservices architecture
- ✅ Want stateless, composable functions
- ✅ Already have video storage, just need analysis

**🏢 Real-world examples**:
- **V1**: "I'm building a video learning platform and need to store student videos"
- **V2**: "I want to analyze TikTok trends and understand what makes videos viral"

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

### V1 Platform Operations (Data Hosting)
```bash
# Upload to hosting platform (V1)
memories v1 upload --file "video.mp4" --title "My Video"

# Search video database (V1)
memories v1 search --query "tutorial" --limit 20

# List stored videos (V1)
memories v1 list --limit 10

# Download from storage (V1)
memories v1 download --video-no 12345 --output "video.mp4"
```

### V2 Analysis Functions (Stateless)
```bash
# Extract metadata from external URL (V2)
memories v2 social metadata \\
  --platform youtube \\
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \\
  --channel rapid

# Analyze social media content (V2)
memories v2 social metadata \\
  --platform tiktok \\
  --video-url "https://www.tiktok.com/@user/video/123" \\
  --channel rapid
```

### V1 Database Operations (Stateful)
```bash
# Get info from hosted video (V1)
memories v1 info --video-no 12345

# Search hosted video database (V1)
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

**💡 Key Difference**: 
- **V1**: Manages your video database and hosting infrastructure
- **V2**: Provides atomic AI analysis functions for any video URL

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