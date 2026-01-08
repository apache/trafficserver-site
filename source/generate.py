#!/usr/bin/env python3
"""
Apache Traffic Server Website Generator

Generates the website HTML files from templates and versions.json config.

Usage:
    cd source/
    python3 generate.py

This reads versions.json and generates:
    - ../content/downloads.html (from templates/downloads.template.html)
    - ../content/index.html (from templates/index.template.html)

To release a new version:
    1. Edit versions.json (update version, date, branch)
    2. Add a news entry to the news array
    3. Run: python3 generate.py
"""

import json
import os
from pathlib import Path

# URLs are computed from version/branch
URL_PATTERNS = {
    'download': 'https://www.apache.org/dyn/closer.cgi/trafficserver/trafficserver-{version}.tar.bz2',
    'pgp': 'https://www.apache.org/dist/trafficserver/trafficserver-{version}.tar.bz2.asc',
    'sha512': 'https://www.apache.org/dist/trafficserver/trafficserver-{version}.tar.bz2.sha512',
    'changelog': 'https://raw.githubusercontent.com/apache/trafficserver/{branch}/CHANGELOG-{version}',
    'milestone': 'https://github.com/apache/trafficserver/pulls?q=is:closed+is:pr+milestone:{version}',
}

def load_config():
    """Load versions.json config file."""
    config_path = Path(__file__).parent / 'versions.json'
    with open(config_path) as f:
        return json.load(f)

def get_urls(version_info):
    """Generate all URLs from version info."""
    return {
        key: pattern.format(**version_info)
        for key, pattern in URL_PATTERNS.items()
    }

def generate_news_html(news_items, max_items=8):
    """Generate HTML for news items."""
    html_parts = []
    for item in news_items[:max_items]:
        html_parts.append(f'''                    <div class="border-l-4 border-accent pl-6 py-2">
                        <p class="text-sm text-secondary font-semibold mb-1">{item['date']}</p>
                        <p class="text-gray-700">{item['text']}</p>
                    </div>''')
    return '\n'.join(html_parts)

def generate_downloads_html(config):
    """Generate downloads.html from template."""
    template_path = Path(__file__).parent / 'templates' / 'downloads.template.html'
    output_path = Path(__file__).parent.parent / 'content' / 'downloads.html'
    
    with open(template_path) as f:
        template = f.read()
    
    v10 = config['versions']['v10']
    v9 = config['versions']['v9']
    
    v10_urls = get_urls(v10)
    v9_urls = get_urls(v9)
    
    # Replace placeholders
    html = template
    
    # V10 replacements
    html = html.replace('{{V10_VERSION}}', v10['version'])
    html = html.replace('{{V10_DATE}}', v10['date'])
    html = html.replace('{{V10_BRANCH}}', v10['branch'])
    html = html.replace('{{V10_DESCRIPTION}}', v10['description'])
    html = html.replace('{{V10_DOWNLOAD_URL}}', v10_urls['download'])
    html = html.replace('{{V10_PGP_URL}}', v10_urls['pgp'])
    html = html.replace('{{V10_SHA512_URL}}', v10_urls['sha512'])
    html = html.replace('{{V10_CHANGELOG_URL}}', v10_urls['changelog'])
    
    # V9 replacements
    html = html.replace('{{V9_VERSION}}', v9['version'])
    html = html.replace('{{V9_DATE}}', v9['date'])
    html = html.replace('{{V9_BRANCH}}', v9['branch'])
    html = html.replace('{{V9_DESCRIPTION}}', v9['description'])
    html = html.replace('{{V9_DOWNLOAD_URL}}', v9_urls['download'])
    html = html.replace('{{V9_PGP_URL}}', v9_urls['pgp'])
    html = html.replace('{{V9_SHA512_URL}}', v9_urls['sha512'])
    html = html.replace('{{V9_CHANGELOG_URL}}', v9_urls['changelog'])
    
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"Generated: {output_path}")

def generate_index_html(config):
    """Generate index.html from template."""
    template_path = Path(__file__).parent / 'templates' / 'index.template.html'
    output_path = Path(__file__).parent.parent / 'content' / 'index.html'
    
    with open(template_path) as f:
        template = f.read()
    
    # Generate news HTML
    news_html = generate_news_html(config['news'])
    
    # Replace placeholder
    html = template.replace('{{NEWS_ITEMS}}', news_html)
    
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"Generated: {output_path}")

def main():
    print("Apache Traffic Server Site Generator")
    print("=" * 40)
    
    config = load_config()
    
    v10 = config['versions']['v10']
    v9 = config['versions']['v9']
    
    print(f"\nCurrent versions:")
    print(f"  v10.x: {v10['version']} ({v10['date']})")
    print(f"  v9.x:  {v9['version']} ({v9['date']})")
    print(f"  News items: {len(config['news'])}")
    print()
    
    generate_downloads_html(config)
    generate_index_html(config)
    
    print("\nDone!")

if __name__ == '__main__':
    main()
