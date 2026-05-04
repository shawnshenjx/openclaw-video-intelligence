#!/usr/bin/env python3
"""
Memories CLI Video Analysis Script
Demonstrates how to wrap CLI commands in a Python script for better integration
"""

import subprocess
import json
import sys
import os
from urllib.parse import urlparse

def run_memories_command(args):
    """Run memories CLI command and return parsed JSON result"""
    try:
        # Ensure API key is set
        if not os.environ.get('MEMORIES_API_KEY'):
            raise ValueError("MEMORIES_API_KEY environment variable not set")
        
        # Run the command
        cmd = ['memories'] + args
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Parse JSON response
        return json.loads(result.stdout)
    
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        print(f"Raw output: {result.stdout}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def detect_platform(url):
    """Detect video platform from URL"""
    domain = urlparse(url).netloc.lower()
    
    if 'youtube.com' in domain or 'youtu.be' in domain:
        return 'youtube'
    elif 'tiktok.com' in domain:
        return 'tiktok' 
    elif 'instagram.com' in domain:
        return 'instagram'
    elif 'twitter.com' in domain or 'x.com' in domain:
        return 'twitter'
    else:
        raise ValueError(f"Unsupported platform for URL: {url}")

def get_video_metadata(url, channel='rapid'):
    """Get video metadata"""
    platform = detect_platform(url)
    args = ['v2', 'social', 'metadata', 
            '--platform', platform,
            '--video-url', url,
            '--channel', channel]
    
    return run_memories_command(args)

def get_video_transcript(url, channel='rapid', mai=False):
    """Get video transcript (audio only or MAI visual+audio)"""
    platform = detect_platform(url)
    
    if mai:
        endpoint = 'mai-transcript'
    else:
        endpoint = 'transcript'
    
    args = ['v2', 'social', endpoint,
            '--platform', platform, 
            '--video-url', url,
            '--channel', channel]
    
    return run_memories_command(args)

def analyze_video(url, include_transcript=True, use_mai=False):
    """Complete video analysis workflow"""
    print(f"🔍 Analyzing video: {url}")
    
    # Get metadata
    print("📊 Getting metadata...")
    metadata = get_video_metadata(url)
    if not metadata or not metadata.get('ok'):
        print("❌ Failed to get metadata")
        return None
    
    result = {
        'url': url,
        'metadata': metadata['result'],
        'transcript': None
    }
    
    # Get transcript if requested
    if include_transcript:
        print(f"📝 Getting {'MAI ' if use_mai else ''}transcript...")
        transcript = get_video_transcript(url, mai=use_mai)
        if transcript and transcript.get('ok'):
            result['transcript'] = transcript['result']
        else:
            print("⚠️ Failed to get transcript")
    
    return result

def print_summary(analysis):
    """Print analysis summary"""
    if not analysis:
        return
    
    metadata = analysis['metadata']
    print("\n" + "="*60)
    print("📺 VIDEO ANALYSIS SUMMARY")
    print("="*60)
    print(f"🎬 Title: {metadata.get('title', 'Unknown')}")
    print(f"📺 Channel: {metadata.get('channel', {}).get('name', 'Unknown')}")
    print(f"⏱️ Duration: {metadata.get('lengthSeconds', 0)} seconds") 
    print(f"👁️ Views: {metadata.get('viewCount', 0):,}")
    
    if analysis['transcript']:
        transcript_data = analysis['transcript']
        
        # Handle different transcript formats
        if 'transcript' in transcript_data:
            # Simple transcript
            text_segments = transcript_data['transcript']
            if isinstance(text_segments, list):
                total_text = ' '.join([seg.get('text', '') for seg in text_segments])
                print(f"📝 Transcript length: {len(total_text)} characters")
                print(f"📝 First 200 chars: {total_text[:200]}...")
        elif 'audioTranscript' in transcript_data:
            # MAI transcript
            audio_segments = transcript_data['audioTranscript'].get('data', [])
            video_segments = transcript_data['videoTranscript'].get('data', [])
            print(f"🎵 Audio segments: {len(audio_segments)}")
            print(f"👁️ Visual segments: {len(video_segments)}")
    
    print("="*60)

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_video.py <video_url> [--mai] [--no-transcript]")
        print("Example: python analyze_video.py 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'")
        sys.exit(1)
    
    url = sys.argv[1]
    use_mai = '--mai' in sys.argv
    include_transcript = '--no-transcript' not in sys.argv
    
    try:
        analysis = analyze_video(url, include_transcript, use_mai)
        print_summary(analysis)
        
        # Save detailed results
        if analysis:
            output_file = 'video_analysis.json'
            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            print(f"💾 Detailed results saved to {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()