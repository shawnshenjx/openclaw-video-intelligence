---
name: Video Intelligence Suite
slug: video-intelligence-suite
version: 1.0.0
description: Memories.ai CLI for video intelligence, transcription, and social media analysis. Supports YouTube, TikTok, Instagram, Twitter with V1 scraping and V2 AI analysis.
changelog: Initial release - Comprehensive video analysis skill supporting YouTube, TikTok, Instagram, Twitter with AI-powered transcription, metadata extraction, and performance testing suite
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["memories"]},"env":{"MEMORIES_API_KEY":"required"}}}
---

# Video Intelligence Suite

Comprehensive video analysis skill powered by Memories.ai for transcription, metadata extraction, and social media video processing.

## Requirements

**Required:**
- `memories` CLI — Memories.ai command-line tool
- `MEMORIES_API_KEY` — Valid API key from Memories.ai

**Installation:**
```bash
pip install memories-cli
export MEMORIES_API_KEY="your-api-key"
```

## Quick Reference

| Platform | Metadata | Transcript | MAI Analysis |
|----------|----------|------------|-------------|
| YouTube | ✅ | ✅ | ✅ |
| TikTok | ✅ | ❌ | ✅ |
| Instagram | ✅ | ❌ | ✅ |
| Twitter | ✅ | ❌ | ✅ |

## Core Capabilities

| Task | Command |
|------|---------|
| Video Metadata | `memories v2 social metadata --platform youtube --video-url URL` |
| Audio Transcript | `memories v2 social transcript --platform youtube --video-url URL` |
| MAI Analysis | `memories v2 social mai-transcript --platform youtube --video-url URL` |
| Full Analysis | `python scripts/analyze_video.py URL` |

## Features

🎥 **Multi-Platform Support**
- YouTube videos and shorts
- TikTok videos  
- Instagram Reels and videos
- Twitter/X videos

🧠 **AI-Powered Analysis**
- Video transcription (audio-to-text)
- MAI visual scene analysis
- Metadata extraction
- Content summarization

⚡ **Performance & Testing**
- Comprehensive pytest test suite
- Mock framework for development  
- Performance benchmarking
- Error handling and retries

## When to Use

✅ **USE this skill when:**
- "Analyze this YouTube video"
- "Get transcript for this video" 
- "Extract video metadata"
- "Summarize video content"
- "Social media video analysis"

❌ **DON'T use when:**
- Video editing or conversion → use `video` skill
- Live streaming analysis → use real-time tools
- Audio-only content → use `openai-whisper` skill

## Usage Examples

### Basic Video Analysis
```bash
python scripts/analyze_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Get Video Metadata Only
```bash
memories v2 social metadata \
  --platform youtube \
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --channel rapid
```

### Full MAI Analysis (Visual + Audio)
```bash
memories v2 social mai-transcript \
  --platform youtube \
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --channel rapid
```

### TikTok Analysis
```bash
python scripts/analyze_video.py "https://www.tiktok.com/@user/video/1234567890" --mai
```

## API Responses

### Metadata Response
```json
{
  "ok": true,
  "result": {
    "title": "Video Title",
    "description": "Video description...",
    "duration": "PT5M30S",
    "viewCount": 12345,
    "channel": {
      "name": "Channel Name",
      "handle": "@channel"
    }
  }
}
```

### MAI Transcript Response
```json
{
  "ok": true,
  "result": {
    "videoTranscript": {
      "data": [
        {
          "text": "Visual scene description",
          "startTime": 0.0,
          "endTime": 3.0
        }
      ]
    },
    "audioTranscript": {
      "data": [
        {
          "text": "Spoken words",
          "startTime": 0.5,
          "endTime": 2.5
        }
      ]
    }
  }
}
```

## Configuration

### Environment Variables
- `MEMORIES_API_KEY` - **Required** - Your Memories.ai API key

### Channel Options
- `rapid` - Fast processing (default)
- `quality` - Higher accuracy, slower processing

## Error Handling

The skill handles:
- Invalid URLs and formats
- Rate limiting (max 10 requests/minute)
- Network timeouts and connection issues
- Platform-specific errors
- API authentication failures

Common error responses:
```json
{
  "ok": false,
  "error": "Invalid URL or platform not supported"
}
```

## Testing

Run the comprehensive test suite:
```bash
pip install -r requirements-test.txt
python -m pytest tests/ -v --cov=scripts
```

Test coverage includes:
- **Unit tests** - Individual function testing
- **Integration tests** - Real API calls
- **Performance tests** - Response time benchmarks
- **Edge cases** - Error scenarios and edge conditions
- **Mock framework** - Development without API calls

## Best Practices

1. **API Key Management**
   - Store in environment variables
   - Never commit keys to version control
   - Rotate keys regularly

2. **Rate Limiting**
   - Respect 10 requests/minute limit  
   - Implement exponential backoff
   - Process videos sequentially

3. **Error Handling**
   - Always check response.ok status
   - Log errors for debugging
   - Implement retry logic

4. **Performance**
   - Use `rapid` channel for quick analysis
   - Cache metadata when possible
   - Process in batches for multiple videos

## Version History

- **1.0.0** - Initial release with full platform support, testing suite, and documentation

## Support

- **GitHub**: https://github.com/Memories-ai-labs/memories-cli  
- **API Docs**: https://api-tools.memories.ai/llms.txt
- **Issues**: Report bugs via GitHub issues
- **Community**: Join discussions on Discord

---

*Complete video intelligence solution for OpenClaw agents*