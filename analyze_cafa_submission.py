#!/usr/bin/env python3
"""
Quick script to download and analyze CAFA submission from Google Drive
"""

import sys
from download_from_gdrive import download_file, analyze_submission_file

# Example usage:
# python analyze_cafa_submission.py "YOUR_GOOGLE_DRIVE_LINK_OR_FILE_ID"

if len(sys.argv) < 2:
    print("Usage: python analyze_cafa_submission.py <google_drive_url_or_file_id>")
    print("\nExample:")
    print("  python analyze_cafa_submission.py 1ABC123XYZ")
    print("  python analyze_cafa_submission.py 'https://drive.google.com/file/d/1ABC123XYZ/view'")
    sys.exit(1)

gdrive_input = sys.argv[1]
output_path = "submission.txt"

print("Downloading file from Google Drive...")
try:
    download_file(gdrive_input, output_path)
    print("\nAnalyzing submission file...")
    analyze_submission_file(output_path)
except Exception as e:
    print(f"Error: {e}")
    print("\nMake sure:")
    print("1. The file is shared with 'Anyone with link can view'")
    print("2. You copied the correct file ID or URL")
