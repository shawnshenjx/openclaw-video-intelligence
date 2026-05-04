#!/usr/bin/env python3
"""
Test runner script for Memories CLI skill tests
Provides different test execution modes and reporting
"""

import os
import sys
import subprocess
import argparse
import json
import time
from pathlib import Path

# Test categories with their markers
TEST_CATEGORIES = {
    'unit': 'unit',
    'integration': 'integration',
    'performance': 'performance', 
    'all': None,  # Run all tests
    'fast': 'unit',  # Alias for unit tests
    'slow': 'slow',
    'network': 'network',
    'api': 'requires_api_key'
}

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['pytest', 'pytest-cov', 'pytest-mock', 'psutil']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing required packages:")
        for package in missing:
            print(f"   - {package}")
        print("\n💡 Install with: pip install " + " ".join(missing))
        return False
    
    return True

def check_api_key():
    """Check if API key is available for integration tests"""
    api_key = os.environ.get('MEMORIES_API_KEY')
    if not api_key:
        print("⚠️  MEMORIES_API_KEY not set - integration tests will be skipped")
        return False
    
    print("✅ API key found - integration tests enabled")
    return True

def run_pytest(category='all', verbose=False, coverage=True, output_format='term'):
    """Run pytest with specified options"""
    cmd = ['python', '-m', 'pytest']
    
    # Add category marker if specified
    if category != 'all' and TEST_CATEGORIES.get(category):
        cmd.extend(['-m', TEST_CATEGORIES[category]])
    
    # Add verbosity
    if verbose:
        cmd.append('-v')
    else:
        cmd.append('-q')
    
    # Add coverage options
    if coverage:
        cmd.extend([
            '--cov=scripts',
            '--cov-report=term-missing'
        ])
        
        if output_format == 'html':
            cmd.append('--cov-report=html:tests/coverage')
        elif output_format == 'xml':
            cmd.append('--cov-report=xml')
    
    # Output formatting
    if output_format == 'junit':
        cmd.extend(['--junit-xml=tests/results/junit.xml'])
    
    # Add test directory
    cmd.append('tests/')
    
    print(f"🧪 Running tests: {' '.join(cmd)}")
    print("─" * 60)
    
    start_time = time.time()
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    end_time = time.time()
    
    duration = end_time - start_time
    print("─" * 60)
    print(f"⏱️  Tests completed in {duration:.2f}s")
    
    return result.returncode

def generate_test_report():
    """Generate a comprehensive test report"""
    report_data = {
        'timestamp': time.time(),
        'environment': {
            'python_version': sys.version,
            'platform': sys.platform,
            'working_directory': str(Path.cwd()),
            'api_key_available': bool(os.environ.get('MEMORIES_API_KEY'))
        },
        'test_categories': list(TEST_CATEGORIES.keys())
    }
    
    # Run tests for each category and collect results
    results = {}
    
    for category in ['unit', 'integration', 'performance']:
        print(f"\n📊 Running {category} tests...")
        
        cmd = [
            'python', '-m', 'pytest', 
            '-m', TEST_CATEGORIES[category],
            '--tb=no', '-q',
            f'--json-report', '--json-report-file=/tmp/pytest_report_{category}.json'
        ]
        
        if category in ['integration', 'performance'] and not os.environ.get('MEMORIES_API_KEY'):
            print(f"⏭️  Skipping {category} tests (no API key)")
            continue
        
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        
        # Try to read JSON report
        try:
            with open(f'/tmp/pytest_report_{category}.json', 'r') as f:
                test_data = json.load(f)
                results[category] = {
                    'passed': test_data.get('summary', {}).get('passed', 0),
                    'failed': test_data.get('summary', {}).get('failed', 0),
                    'skipped': test_data.get('summary', {}).get('skipped', 0),
                    'duration': test_data.get('duration', 0),
                    'exit_code': result.returncode
                }
        except (FileNotFoundError, json.JSONDecodeError):
            results[category] = {
                'exit_code': result.returncode,
                'error': 'Could not parse test results'
            }
    
    report_data['results'] = results
    
    # Save report
    os.makedirs('tests/results', exist_ok=True)
    report_path = 'tests/results/test_report.json'
    with open(report_path, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📋 Test report saved to {report_path}")
    return report_data

def print_test_summary(report_data):
    """Print a formatted test summary"""
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    total_passed = 0
    total_failed = 0
    total_skipped = 0
    
    for category, results in report_data.get('results', {}).items():
        if 'error' in results:
            print(f"{category.upper():12}: ❌ {results['error']}")
            continue
        
        passed = results.get('passed', 0)
        failed = results.get('failed', 0)
        skipped = results.get('skipped', 0)
        duration = results.get('duration', 0)
        
        total_passed += passed
        total_failed += failed
        total_skipped += skipped
        
        status = "✅" if failed == 0 else "❌"
        print(f"{category.upper():12}: {status} {passed}✓ {failed}✗ {skipped}⏭ ({duration:.1f}s)")
    
    print("─" * 60)
    print(f"{'TOTAL':12}: {total_passed}✓ {total_failed}✗ {total_skipped}⏭")
    
    if total_failed == 0:
        print("🎉 All tests passed!")
    else:
        print(f"💥 {total_failed} tests failed")
    
    print("=" * 60)

def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(description='Run Memories CLI skill tests')
    parser.add_argument(
        'category', 
        nargs='?', 
        default='all',
        choices=list(TEST_CATEGORIES.keys()),
        help='Test category to run'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--no-coverage',
        action='store_true',
        help='Disable coverage reporting'
    )
    parser.add_argument(
        '--format',
        choices=['term', 'html', 'xml', 'junit'],
        default='term',
        help='Output format'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate comprehensive test report'
    )
    parser.add_argument(
        '--check-deps',
        action='store_true',
        help='Check dependencies only'
    )
    
    args = parser.parse_args()
    
    print("🧠 Memories CLI Test Runner")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    if args.check_deps:
        print("✅ All dependencies available")
        return 0
    
    # Check API key for integration tests
    check_api_key()
    
    # Create results directory
    os.makedirs('tests/results', exist_ok=True)
    
    # Run tests or generate report
    if args.report:
        report_data = generate_test_report()
        print_test_summary(report_data)
        return 0
    else:
        return run_pytest(
            category=args.category,
            verbose=args.verbose,
            coverage=not args.no_coverage,
            output_format=args.format
        )

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)