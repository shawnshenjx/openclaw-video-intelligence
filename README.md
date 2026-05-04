# Video Intelligence Suite

🧠 **Enterprise video intelligence platform for OpenClaw agents.** Professional-grade video analysis, transcription, and social media intelligence with multi-platform support and advanced AI capabilities.

[![GitHub release](https://img.shields.io/github/release/shawnshenjx/video-intelligence-platform.svg)](https://github.com/shawnshenjx/video-intelligence-platform/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills.sh](https://img.shields.io/badge/Skills.sh-Compatible-blue)](https://skills.sh)

## 🚀 Quick Start

### 1. Install Video Intelligence Suite

```bash
# Via pip (recommended)
pip install memories-cli

# Or download binary from GitHub releases
wget https://github.com/Memories-ai-labs/memories-cli/releases/latest/download/memories-linux-x64
chmod +x memories-linux-x64
mv memories-linux-x64 ~/.local/bin/memories
```

### 2. Set API Key

```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export MEMORIES_API_KEY="sk-your-api-key-here"

# Or set temporarily
export MEMORIES_API_KEY="sk-mavi-..."
```

### 3. Test Installation

```bash
memories --help
memories v2 --help
```

## Skill Structure

```
memories-cli/
├── SKILL.md              # Main skill documentation
├── README.md             # This file  
└── scripts/
    └── analyze_video.py   # Python wrapper script
```

## Usage Examples

### Via OpenClaw Assistant

```
"Analyze this YouTube video: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
"Get transcript for this TikTok video"
"Extract metadata from this Instagram reel"
```

### Direct CLI Usage

```bash
# Get video metadata
memories v2 social metadata \
  --platform youtube \
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --channel rapid

# Get simple transcript
memories v2 social transcript \
  --platform youtube \
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --channel rapid

# Get MAI transcript (visual + audio analysis)
memories v2 social mai-transcript \
  --platform youtube \
  --video-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --channel rapid
```

### Python Script Usage

```bash
cd ~/.openclaw/workspace/skills/memories-cli

# Basic analysis
python scripts/analyze_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# With MAI analysis
python scripts/analyze_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --mai

# Metadata only
python scripts/analyze_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --no-transcript
```

## Key Features

### ✅ What This Skill Provides

1. **Unified CLI Interface**: Single command for multiple platforms
2. **Structured Output**: JSON responses for easy parsing  
3. **Error Handling**: Proper error messages and debugging info
4. **Platform Detection**: Auto-detect video platform from URL
5. **Async Support**: Handle long-running MAI transcription tasks
6. **Rate Limiting**: Built-in respect for API limits

### 🎯 Use Cases

- **Video Summarization**: Extract key information from video content
- **Content Moderation**: Analyze video/audio for inappropriate content  
- **Research Analysis**: Process interview videos or conference talks
- **Social Media Monitoring**: Track mentions across video platforms
- **Accessibility**: Generate transcripts for deaf/hard-of-hearing users

### 📊 Supported Platforms

| Platform | Metadata | Audio Transcript | Visual Analysis |
|----------|----------|------------------|----------------|
| YouTube  | ✅        | ✅               | ✅             |
| TikTok   | ✅        | ❌               | ✅             |
| Instagram| ✅        | ❌               | ✅             |
| Twitter  | ✅        | ❌               | ✅             |

## 🏗️ Dual API Architecture

The Video Intelligence Platform is built on **Memories.ai's dual architecture** - two complementary API systems designed for different use cases:

### 🏢 V1 API - Video Data Hosting Platform
**Architecture**: Stateful platform with managed database infrastructure  
**Purpose**: Complete video hosting and management solution

- ✅ **Video Storage**: Upload and host video files with persistent storage
- ✅ **Built-in Search**: Managed database with full-text search capabilities
- ✅ **Video Library Management**: Organize, categorize, and manage video collections
- ✅ **Download & Streaming**: Direct access to hosted video files
- 🎯 **Use Case**: Building video platforms, content management systems, video hosting infrastructure

### ⚛️ V2 API - Atomic Intelligence Functions
**Architecture**: Stateless microservices providing pure AI analysis  
**Purpose**: Composable video intelligence capabilities

- ✅ **AI Transcription**: Advanced speech-to-text with speaker detection
- ✅ **Visual Scene Analysis**: MAI (Multimodal AI) visual understanding
- ✅ **External URL Analysis**: Process videos from any platform without storage
- ✅ **Webhook Integration**: Async processing for long-running analysis
- 🎯 **Use Case**: Adding AI analysis to existing systems, research, content intelligence

### 🎯 Architecture Decision Guide

| Need | Recommended API | Example Use Case |
|------|----------------|------------------|
| **Video Platform Infrastructure** | V1 | "Build an e-learning platform with video storage and search" |
| **AI Analysis of External Content** | V2 | "Analyze viral TikTok trends to understand engagement patterns" |
| **Complete Video Solution** | V1 + V2 | "Video platform with AI-powered content recommendations" |
| **Research & Analytics** | V2 | "Academic research on social media video content" |
| **Content Moderation** | V2 | "Automated safety analysis of user-generated video content" |

> **💡 Key Insight**: This is an **architectural choice**, not a version difference. V1 and V2 serve different purposes and can be used together or independently based on your specific requirements.

## Integration Patterns

### 1. As OpenClaw Skill

The assistant can automatically detect video URLs in conversations and suggest analysis:

```
User: "Can you help me understand this video? https://youtube.com/watch?v=..."
Assistant: *uses memories-cli skill to analyze video and provides summary*
```

### 2. In Automation Workflows

```bash
# Process a batch of videos
for url in $(cat video_urls.txt); do
    python scripts/analyze_video.py "$url" >> analysis_results.json
done
```

### 3. As API Service

Wrap the CLI in a web service for REST API access:

```python
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_video():
    url = request.json['url']
    # Run memories CLI and return results
    # ... implementation
```

## Configuration Options

### Environment Variables

- `MEMORIES_API_KEY`: Your Memories.ai API key (required)
- `MEMORIES_V1_BASE_URL`: Override V1 API base URL
- `MEMORIES_V2_BASE_URL`: Override V2 API base URL  
- `MEMORIES_TIMEOUT_MS`: Request timeout in milliseconds

### CLI Options

- `--channel rapid|quality`: Choose speed vs quality tradeoff
- `--timeout-ms N`: Set request timeout
- `--api-key KEY`: Override API key

## Best Practices

### 1. Error Handling
```python
result = run_memories_command(args)
if not result or not result.get('ok'):
    print(f"Command failed: {result.get('error', 'Unknown error')}")
    return None
```

### 2. Rate Limiting
```python
import time

for url in urls:
    analyze_video(url)
    time.sleep(6)  # Max 10 requests/minute
```

### 3. Async Processing
```python
# For long videos, use MAI with webhook callbacks
result = get_video_transcript(url, mai=True)
task_id = result.get('taskId')
# Poll or wait for webhook notification
```

## Troubleshooting

### Common Issues

1. **Missing API Key**
   ```
   ValueError: MEMORIES_API_KEY environment variable not set
   ```
   Solution: Set the environment variable with your API key

2. **Command Not Found**
   ```
   FileNotFoundError: [Errno 2] No such file or directory: 'memories'
   ```
   Solution: Install memories CLI and ensure it's in PATH

3. **Rate Limiting**
   ```
   HTTP 429: Too Many Requests
   ```
   Solution: Wait before retrying, respect rate limits

4. **Invalid URL**
   ```
   ValueError: Unsupported platform for URL
   ```
   Solution: Check that URL is from supported platform

### Debugging

```bash
# Enable verbose logging
export MEMORIES_DEBUG=1

# Test with simple command
memories v2 social metadata --platform youtube --video-url "..." --channel rapid

# Check API connectivity
curl -H "Authorization: $MEMORIES_API_KEY" https://mavi-backend.memories.ai/serve/api/v2/health
```

## Contributing

To extend this skill:

1. **Add New Platforms**: Update platform detection in `analyze_video.py`
2. **Add New Features**: Extend CLI wrapper functions
3. **Improve Error Handling**: Add more specific error cases
4. **Add Tests**: Create test cases for different video types

## Resources

- **Memories CLI**: https://github.com/Memories-ai-labs/memories-cli
- **API Documentation**: https://api-tools.memories.ai/
- **OpenClaw Skills**: https://docs.openclaw.ai/skills/
- **ClawHub**: https://clawhub.ai/