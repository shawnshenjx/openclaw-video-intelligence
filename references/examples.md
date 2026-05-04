# Video Intelligence Suite - Usage Examples

Complete examples for common video analysis workflows using the Video Intelligence Suite.

## Basic Analysis Examples

### 1. YouTube Video Analysis
```bash
# Simple metadata extraction
python scripts/memories.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Full analysis with transcript and visuals
python scripts/memories.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --mai

# Extract specific fields only
python scripts/memories.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \\
  --extract title,duration,viewCount,transcript
```

**Expected Output:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "platform": "youtube",
  "metadata": {
    "title": "Rick Astley - Never Gonna Give You Up",
    "duration": 213,
    "viewCount": 1500000000,
    "channel": {
      "name": "Rick Astley",
      "handle": "@RickAstley"
    }
  },
  "transcript": {
    "segments": [
      {
        "text": "We're no strangers to love",
        "start": 0.5,
        "end": 2.8
      }
    ]
  }
}
```

### 2. TikTok Content Analysis
```bash
# TikTok video with MAI analysis
python scripts/memories.py "https://www.tiktok.com/@username/video/7234567890" --mai

# Batch analyze TikTok creator's recent videos
python scripts/memories.py --batch tiktok_urls.txt --output tiktok_analysis.json
```

**TikTok URLs file (tiktok_urls.txt):**
```
https://www.tiktok.com/@creator1/video/7234567890
https://www.tiktok.com/@creator1/video/7234567891
https://www.tiktok.com/@creator2/video/7234567892
```

### 3. Instagram Reels Analysis
```bash
# Instagram Reel analysis
python scripts/memories.py "https://www.instagram.com/p/ABC123DEF456/" --mai

# Extract hashtags and engagement metrics
python scripts/memories.py "https://www.instagram.com/p/ABC123DEF456/" \\
  --extract hashtags,likes,comments,shares
```

## Advanced Workflows

### 4. Content Creator Analysis Pipeline
```bash
#!/bin/bash
# analyze_creator.sh - Complete creator analysis workflow

CREATOR_URLS="creator_videos.txt"
OUTPUT_DIR="analysis_results"
CREATOR_NAME="example_creator"

mkdir -p "$OUTPUT_DIR"

echo "🔍 Starting creator analysis for $CREATOR_NAME..."

# 1. Batch analyze all videos
python scripts/memories.py --batch "$CREATOR_URLS" \\
  --mai \\
  --output "$OUTPUT_DIR/${CREATOR_NAME}_raw_data.json"

# 2. Generate summary report
python scripts/analyze_creator_performance.py \\
  --input "$OUTPUT_DIR/${CREATOR_NAME}_raw_data.json" \\
  --output "$OUTPUT_DIR/${CREATOR_NAME}_report.json"

# 3. Extract top-performing content
python scripts/extract_top_content.py \\
  --input "$OUTPUT_DIR/${CREATOR_NAME}_raw_data.json" \\
  --metric engagement_rate \\
  --top 10 \\
  --output "$OUTPUT_DIR/${CREATOR_NAME}_top_content.json"

echo "✅ Analysis complete! Results in $OUTPUT_DIR/"
```

### 5. Social Media Monitoring
```python
# monitor_trending.py - Monitor trending content
import json
import time
from datetime import datetime
import subprocess

def analyze_trending_videos():
    """Monitor and analyze trending videos across platforms"""
    
    trending_urls = [
        "https://www.youtube.com/watch?v=trending1",
        "https://www.tiktok.com/@viral/video/trending2", 
        "https://www.instagram.com/p/trending3/"
    ]
    
    results = []
    
    for url in trending_urls:
        print(f"Analyzing: {url}")
        
        try:
            # Run analysis
            result = subprocess.run([
                'python', 'scripts/memories.py',
                url,
                '--mai',
                '--extract', 'title,engagement,themes,sentiment',
                '--output', 'temp_result.json'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                with open('temp_result.json', 'r') as f:
                    analysis = json.load(f)
                
                # Add analysis timestamp
                analysis['analyzed_at'] = datetime.now().isoformat()
                results.append(analysis)
                
            time.sleep(6)  # Rate limiting (10 requests/minute)
            
        except Exception as e:
            print(f"Error analyzing {url}: {e}")
    
    # Save consolidated results
    with open(f'trending_analysis_{datetime.now().strftime("%Y%m%d_%H%M")}.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    analyze_trending_videos()
```

### 6. Competitive Analysis
```bash
# competitive_analysis.sh - Analyze competitor content

COMPETITOR_CHANNELS=(
    "https://www.youtube.com/@competitor1"
    "https://www.youtube.com/@competitor2"
    "https://www.tiktok.com/@competitor3"
)

OUTPUT_FILE="competitive_analysis_$(date +%Y%m%d).json"

echo "🏢 Starting competitive analysis..."

# Create analysis file
echo '{"competitors": []}' > "$OUTPUT_FILE"

for channel in "${COMPETITOR_CHANNELS[@]}"; do
    echo "Analyzing channel: $channel"
    
    # Extract channel videos (you'd implement channel scraping)
    # For demo, using placeholder URLs
    python scripts/memories.py \\
        --batch "${channel}_recent_videos.txt" \\
        --mai \\
        --extract "engagement,themes,posting_frequency,content_style" \\
        --competitor-mode \\
        --output "temp_competitor.json"
    
    # Append to main analysis file
    python scripts/merge_analysis.py \\
        --main "$OUTPUT_FILE" \\
        --append "temp_competitor.json" \\
        --channel "$channel"
done

echo "✅ Competitive analysis complete: $OUTPUT_FILE"
```

## Platform-Specific Examples

### 7. YouTube Channel Analysis
```python
# youtube_channel_analysis.py
import json
import requests
from datetime import datetime, timedelta

def analyze_youtube_channel(channel_handle, days_back=30):
    """Analyze recent videos from a YouTube channel"""
    
    # Get recent video URLs (implement your preferred method)
    recent_videos = get_recent_channel_videos(channel_handle, days_back)
    
    analysis_results = {
        'channel': channel_handle,
        'analysis_date': datetime.now().isoformat(),
        'video_count': len(recent_videos),
        'videos': []
    }
    
    for video_url in recent_videos:
        print(f"Analyzing: {video_url}")
        
        # Analyze video
        result = analyze_single_video(video_url)
        
        if result:
            analysis_results['videos'].append(result)
            
        time.sleep(6)  # Rate limiting
    
    # Generate insights
    insights = generate_channel_insights(analysis_results)
    analysis_results['insights'] = insights
    
    return analysis_results

def generate_channel_insights(analysis_data):
    """Generate actionable insights from channel analysis"""
    videos = analysis_data['videos']
    
    if not videos:
        return {}
    
    # Calculate averages
    avg_duration = sum(v['metadata']['duration'] for v in videos) / len(videos)
    avg_engagement = sum(v['metadata']['viewCount'] for v in videos) / len(videos)
    
    # Identify patterns
    common_themes = extract_common_themes([v['transcript'] for v in videos if 'transcript' in v])
    posting_pattern = analyze_posting_pattern(videos)
    
    return {
        'average_duration_seconds': avg_duration,
        'average_views': avg_engagement,
        'common_themes': common_themes[:10],  # Top 10 themes
        'posting_pattern': posting_pattern,
        'content_recommendations': generate_content_recommendations(videos)
    }
```

### 8. TikTok Trend Analysis
```bash
# tiktok_trends.sh - Analyze TikTok trending hashtags

HASHTAGS=(
    "#viral"
    "#fyp"
    "#trending" 
    "#funny"
    "#dance"
)

for hashtag in "${HASHTAGS[@]}"; do
    echo "Analyzing hashtag: $hashtag"
    
    # Get trending videos for hashtag (implement scraping)
    python scripts/scrape_tiktok_hashtag.py "$hashtag" --limit 50 > "${hashtag}_urls.txt"
    
    # Analyze videos
    python scripts/memories.py \\
        --batch "${hashtag}_urls.txt" \\
        --mai \\
        --extract "engagement,music,effects,duration,themes" \\
        --output "analysis_${hashtag}.json"
    
    # Generate hashtag insights
    python scripts/hashtag_insights.py \\
        --input "analysis_${hashtag}.json" \\
        --hashtag "$hashtag" \\
        --output "insights_${hashtag}.json"
done

# Consolidate all hashtag analyses
python scripts/consolidate_trends.py \\
    --input-pattern "insights_*.json" \\
    --output "tiktok_trend_report_$(date +%Y%m%d).json"
```

## Integration Examples

### 9. Webhook Integration
```python
# webhook_server.py - Handle Memories.ai webhooks
from flask import Flask, request, jsonify
import json
import hmac
import hashlib

app = Flask(__name__)

@app.route('/memories-webhook', methods=['POST'])
def handle_memories_webhook():
    """Handle incoming webhook from Memories.ai V2 API"""
    
    # Verify webhook signature
    signature = request.headers.get('X-Memories-Signature')
    if not verify_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    webhook_data = request.json
    
    # Process based on status
    if webhook_data['status'] == 'completed':
        handle_analysis_complete(webhook_data)
    elif webhook_data['status'] == 'failed':
        handle_analysis_failed(webhook_data)
    
    return jsonify({'status': 'received'}), 200

def handle_analysis_complete(data):
    """Process completed video analysis"""
    task_id = data['task_id']
    video_url = data['video_url']
    analysis_result = data['data']
    
    print(f"✅ Analysis complete for {video_url}")
    
    # Store results
    with open(f'results/{task_id}.json', 'w') as f:
        json.dump(analysis_result, f, indent=2)
    
    # Trigger downstream processing
    process_video_insights(analysis_result)
    
    # Send notification
    send_completion_notification(video_url, analysis_result)

def verify_signature(payload, signature):
    """Verify webhook signature"""
    secret = os.environ.get('MEMORIES_WEBHOOK_SECRET')
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

### 10. Automated Content Moderation
```python
# content_moderator.py - Automated video content moderation
import json
import subprocess
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ModerationResult:
    video_url: str
    is_safe: bool
    risk_score: float
    flagged_content: List[str]
    recommendations: List[str]

class ContentModerator:
    def __init__(self):
        self.safety_keywords = [
            'violence', 'hate speech', 'harassment',
            'inappropriate', 'explicit', 'dangerous'
        ]
        self.risk_thresholds = {
            'low': 0.3,
            'medium': 0.6, 
            'high': 0.8
        }
    
    def moderate_video(self, video_url: str) -> ModerationResult:
        """Perform content moderation on a video"""
        
        # Analyze video with MAI
        analysis = self.analyze_video_content(video_url)
        
        # Extract safety signals
        safety_signals = self.extract_safety_signals(analysis)
        
        # Calculate risk score
        risk_score = self.calculate_risk_score(safety_signals)
        
        # Determine if content is safe
        is_safe = risk_score < self.risk_thresholds['medium']
        
        # Generate recommendations
        recommendations = self.generate_recommendations(safety_signals, risk_score)
        
        return ModerationResult(
            video_url=video_url,
            is_safe=is_safe,
            risk_score=risk_score,
            flagged_content=safety_signals,
            recommendations=recommendations
        )
    
    def analyze_video_content(self, video_url: str) -> Dict:
        """Analyze video using Memories.ai"""
        result = subprocess.run([
            'python', 'scripts/memories.py',
            video_url,
            '--mai',
            '--extract', 'transcript,visual_scenes,objects,text_ocr',
            '--safety-mode'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            with open('temp_moderation.json', 'r') as f:
                return json.load(f)
        
        raise Exception(f"Analysis failed: {result.stderr}")
    
    def extract_safety_signals(self, analysis: Dict) -> List[str]:
        """Extract potential safety concerns from analysis"""
        flags = []
        
        # Check transcript for problematic content
        if 'transcript' in analysis:
            for segment in analysis['transcript'].get('segments', []):
                text = segment['text'].lower()
                for keyword in self.safety_keywords:
                    if keyword in text:
                        flags.append(f"Transcript contains: {keyword}")
        
        # Check visual scenes
        if 'visual_scenes' in analysis:
            for scene in analysis['visual_scenes'].get('scenes', []):
                description = scene['text'].lower()
                for keyword in self.safety_keywords:
                    if keyword in description:
                        flags.append(f"Visual scene: {keyword}")
        
        return list(set(flags))  # Remove duplicates
    
    def calculate_risk_score(self, safety_signals: List[str]) -> float:
        """Calculate overall risk score based on safety signals"""
        base_score = min(len(safety_signals) * 0.2, 1.0)
        
        # Weight certain signals higher
        high_risk_keywords = ['violence', 'hate speech', 'explicit']
        for signal in safety_signals:
            for high_risk in high_risk_keywords:
                if high_risk in signal.lower():
                    base_score += 0.3
        
        return min(base_score, 1.0)
    
    def generate_recommendations(self, signals: List[str], risk_score: float) -> List[str]:
        """Generate moderation recommendations"""
        recommendations = []
        
        if risk_score < self.risk_thresholds['low']:
            recommendations.append("✅ Content appears safe for publication")
        elif risk_score < self.risk_thresholds['medium']:
            recommendations.append("⚠️ Review flagged content before publication")
            recommendations.append("Consider adding content warnings")
        else:
            recommendations.append("🚨 High-risk content - manual review required")
            recommendations.append("Consider blocking or restricting access")
        
        if signals:
            recommendations.append(f"Address flagged issues: {', '.join(signals)}")
        
        return recommendations

# Usage example
if __name__ == "__main__":
    moderator = ContentModerator()
    
    test_videos = [
        "https://www.youtube.com/watch?v=test1",
        "https://www.tiktok.com/@user/video/test2"
    ]
    
    for video_url in test_videos:
        result = moderator.moderate_video(video_url)
        
        print(f"\n📹 Video: {result.video_url}")
        print(f"✅ Safe: {result.is_safe}")
        print(f"🎯 Risk Score: {result.risk_score:.2f}")
        
        if result.flagged_content:
            print(f"🚩 Flags: {', '.join(result.flagged_content)}")
        
        print("💡 Recommendations:")
        for rec in result.recommendations:
            print(f"  - {rec}")
```

## Error Handling Examples

### 11. Robust Error Handling
```python
# robust_analyzer.py - Production-ready video analysis
import time
import random
import logging
from typing import Optional, Dict, List
from dataclasses import dataclass

@dataclass
class AnalysisConfig:
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    rate_limit_delay: float = 65.0
    timeout_seconds: int = 300

class RobustVideoAnalyzer:
    def __init__(self, config: AnalysisConfig = None):
        self.config = config or AnalysisConfig()
        self.logger = logging.getLogger(__name__)
        
    def analyze_video(self, video_url: str, **kwargs) -> Optional[Dict]:
        """Analyze video with robust error handling and retries"""
        
        for attempt in range(self.config.max_retries):
            try:
                self.logger.info(f"Analyzing video (attempt {attempt + 1}): {video_url}")
                
                # Attempt analysis
                result = self._perform_analysis(video_url, **kwargs)
                
                if self._is_valid_result(result):
                    self.logger.info(f"✅ Analysis successful: {video_url}")
                    return result
                else:
                    self.logger.warning(f"⚠️ Invalid result format: {video_url}")
                    
            except RateLimitError as e:
                self.logger.warning(f"Rate limited: {e}. Waiting {self.config.rate_limit_delay}s")
                time.sleep(self.config.rate_limit_delay)
                
            except TimeoutError as e:
                self.logger.warning(f"Timeout: {e}")
                if attempt < self.config.max_retries - 1:
                    self._exponential_backoff(attempt)
                    
            except NetworkError as e:
                self.logger.warning(f"Network error: {e}")
                if attempt < self.config.max_retries - 1:
                    self._exponential_backoff(attempt)
                    
            except ValidationError as e:
                self.logger.error(f"❌ Validation error (no retry): {e}")
                return None
                
            except Exception as e:
                self.logger.error(f"❌ Unexpected error: {e}")
                if attempt < self.config.max_retries - 1:
                    self._exponential_backoff(attempt)
        
        self.logger.error(f"❌ Analysis failed after {self.config.max_retries} attempts: {video_url}")
        return None
    
    def _perform_analysis(self, video_url: str, **kwargs) -> Dict:
        """Perform the actual video analysis"""
        # Implementation depends on your analysis method
        # This could call the memories CLI or API directly
        pass
    
    def _is_valid_result(self, result: Dict) -> bool:
        """Validate analysis result structure"""
        required_fields = ['url', 'metadata']
        return all(field in result for field in required_fields)
    
    def _exponential_backoff(self, attempt: int):
        """Implement exponential backoff with jitter"""
        delay = min(
            self.config.base_delay * (2 ** attempt) + random.uniform(0, 1),
            self.config.max_delay
        )
        self.logger.info(f"Backing off for {delay:.2f} seconds")
        time.sleep(delay)
    
    def batch_analyze(self, video_urls: List[str], **kwargs) -> Dict[str, Optional[Dict]]:
        """Analyze multiple videos with error tracking"""
        results = {}
        failed_count = 0
        
        for i, url in enumerate(video_urls):
            self.logger.info(f"Processing video {i+1}/{len(video_urls)}: {url}")
            
            try:
                result = self.analyze_video(url, **kwargs)
                results[url] = result
                
                if result is None:
                    failed_count += 1
                
                # Progress reporting
                if (i + 1) % 10 == 0:
                    success_rate = ((i + 1 - failed_count) / (i + 1)) * 100
                    self.logger.info(f"Progress: {i+1}/{len(video_urls)} ({success_rate:.1f}% success)")
                
                # Rate limiting between requests
                time.sleep(6.5)  # Slightly over 6s for 10 requests/minute limit
                
            except KeyboardInterrupt:
                self.logger.info("Analysis interrupted by user")
                break
            
            except Exception as e:
                self.logger.error(f"Unexpected error processing {url}: {e}")
                results[url] = None
                failed_count += 1
        
        # Final summary
        success_rate = ((len(results) - failed_count) / len(results)) * 100
        self.logger.info(f"Batch analysis complete: {len(results)} videos, {success_rate:.1f}% success")
        
        return results

# Custom exception classes
class RateLimitError(Exception): pass
class TimeoutError(Exception): pass  
class NetworkError(Exception): pass
class ValidationError(Exception): pass

# Usage example
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    analyzer = RobustVideoAnalyzer()
    
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.tiktok.com/@user/video/123",
        "https://invalid-url.com/video"  # This will fail
    ]
    
    results = analyzer.batch_analyze(test_urls, mai=True)
    
    # Process results
    for url, result in results.items():
        if result:
            print(f"✅ {url}: {result['metadata']['title']}")
        else:
            print(f"❌ {url}: Analysis failed")
```

These examples demonstrate the full range of capabilities of the Video Intelligence Suite, from basic single-video analysis to complex production workflows with error handling, batch processing, and integration patterns.