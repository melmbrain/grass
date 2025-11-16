#!/usr/bin/env python3
"""
Download files from Google Drive and analyze CAFA submission files
"""

import gdown
import os

def download_file(gdrive_url_or_id, output_path):
    """
    Download a file from Google Drive

    Args:
        gdrive_url_or_id: Either full Google Drive URL or just the file ID
        output_path: Where to save the file
    """
    # Extract file ID if full URL is provided
    if 'drive.google.com' in gdrive_url_or_id:
        # Handle different URL formats
        if '/file/d/' in gdrive_url_or_id:
            file_id = gdrive_url_or_id.split('/file/d/')[1].split('/')[0]
        elif 'id=' in gdrive_url_or_id:
            file_id = gdrive_url_or_id.split('id=')[1].split('&')[0]
        else:
            file_id = gdrive_url_or_id
    else:
        file_id = gdrive_url_or_id

    # Download the file
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url, output_path, quiet=False)
    print(f"Downloaded to: {output_path}")
    return output_path

def analyze_submission_file(file_path):
    """
    Analyze a CAFA submission file to identify potential issues
    """
    print(f"\n{'='*60}")
    print(f"Analyzing: {file_path}")
    print(f"{'='*60}\n")

    # Get file size
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    print(f"File size: {file_size_mb:.2f} MB ({file_size_bytes:,} bytes)")

    # Count lines and analyze content
    unique_proteins = set()
    total_predictions = 0
    go_terms_per_protein = {}
    sample_lines = []

    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue

            total_predictions += 1

            # Save first 10 lines as sample
            if i < 10:
                sample_lines.append(line)

            # Parse the line
            parts = line.split('\t') if '\t' in line else line.split(',')
            if len(parts) >= 2:
                protein_id = parts[0]
                unique_proteins.add(protein_id)
                go_terms_per_protein[protein_id] = go_terms_per_protein.get(protein_id, 0) + 1

    print(f"Total predictions (lines): {total_predictions:,}")
    print(f"Unique proteins: {len(unique_proteins):,}")
    print(f"Average GO terms per protein: {total_predictions / len(unique_proteins):.1f}")

    # Show distribution of GO terms per protein
    if go_terms_per_protein:
        max_go_terms = max(go_terms_per_protein.values())
        min_go_terms = min(go_terms_per_protein.values())
        print(f"Min GO terms for a protein: {min_go_terms}")
        print(f"Max GO terms for a protein: {max_go_terms}")

    print(f"\nFirst 10 lines:")
    print("-" * 60)
    for line in sample_lines:
        print(line)

    # Estimate expected size
    avg_bytes_per_line = file_size_bytes / total_predictions if total_predictions > 0 else 0
    print(f"\n{'='*60}")
    print("DIAGNOSIS:")
    print(f"{'='*60}")
    print(f"Average bytes per prediction: {avg_bytes_per_line:.1f}")

    # Provide recommendations
    if file_size_mb > 100:
        print("\n⚠️  WARNING: File is very large (>100 MB)")
        print("\nPossible issues:")
        if total_predictions / len(unique_proteins) > 100:
            print(f"  • Too many GO terms per protein ({total_predictions / len(unique_proteins):.0f} avg)")
            print("    → Recommended: Filter to top 10-50 predictions per protein")
        if len(unique_proteins) > 200000:
            print(f"  • Too many proteins ({len(unique_proteins):,})")
            print("    → Make sure you're only predicting on TEST set proteins")
        if avg_bytes_per_line > 100:
            print(f"  • Lines are too long ({avg_bytes_per_line:.0f} bytes)")
            print("    → Check if you're including extra data/features")
    else:
        print(f"\n✓ File size looks reasonable ({file_size_mb:.2f} MB)")

    return {
        'file_size_mb': file_size_mb,
        'total_predictions': total_predictions,
        'unique_proteins': len(unique_proteins),
        'avg_go_terms_per_protein': total_predictions / len(unique_proteins) if unique_proteins else 0
    }

if __name__ == "__main__":
    print("Google Drive File Downloader for CAFA Submissions")
    print("="*60)
    print("\nTo use this script:")
    print("1. Share your Google Drive file (Anyone with link can view)")
    print("2. Copy the file ID or full URL")
    print("3. Run this script with the file ID/URL")
    print("\nExample file ID from URL:")
    print("  https://drive.google.com/file/d/1ABC123XYZ/view")
    print("  File ID: 1ABC123XYZ")
    print("\n" + "="*60)
