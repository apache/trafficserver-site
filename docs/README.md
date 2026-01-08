# Apache Traffic Server Website

Modern, responsive website for Apache Traffic Server built with Tailwind CSS.

## Features

- Modern, responsive design using Tailwind CSS
- Mobile-first approach with hamburger menu
- Config-driven site generator for easy version updates
- Clean, contemporary tech aesthetic

## Directory Structure

```
source/
├── generate.py         # Site generator script
├── versions.json       # Version config & news items
└── templates/          # HTML templates with placeholders
    ├── index.template.html
    └── downloads.template.html

content/
├── index.html          # Generated homepage
├── downloads.html      # Generated downloads page
├── styles/             # Tailwind CSS
├── js/                 # Mobile menu JS
├── images/             # Site images
└── *.html              # Other static pages
```

## Building the Site

The site is automatically built by [Apache Buildbot](https://ci2.apache.org/#/builders?tags=trafficserver-site) when changes are pushed to the `asf-site` branch. Buildbot runs `source/generate.py` to generate the HTML files from templates.

To build manually (for local testing):

```bash
cd source
python3 generate.py
```

This generates `content/index.html` and `content/downloads.html` from templates.

## Releasing a New Version

1. Edit `source/versions.json`:

```json
{
  "versions": {
    "v10": {
      "version": "10.2.0",
      "date": "February 1, 2026",
      "branch": "10.2.x",
      "description": "Latest features and improvements"
    }
  },
  "news": [
    {
      "date": "February 1, 2026",
      "text": "We are releasing version <strong>v10.2.0</strong>!"
    }
  ]
}
```

2. Commit and push the changes to `asf-site`. Buildbot will automatically run the generator.

## URL Patterns

Download URLs are automatically generated from version info:
- Download: `https://www.apache.org/dyn/closer.cgi/trafficserver/trafficserver-{version}.tar.bz2`
- PGP: `https://www.apache.org/dist/trafficserver/trafficserver-{version}.tar.bz2.asc`
- SHA512: `https://www.apache.org/dist/trafficserver/trafficserver-{version}.tar.bz2.sha512`
- Changelog: `https://raw.githubusercontent.com/apache/trafficserver/{branch}/CHANGELOG-{version}`

## Testing Locally

```bash
cd content
python3 -m http.server 8080
# Open http://localhost:8080
```

## Design Specifications

### Colors
- **Primary Navy:** `#1e3a8a` - Headers and navigation
- **Accent Blue:** `#3b82f6` - CTAs and highlights
- **Secondary:** `#64748b` - Body text
- **Background:** White with `#f8fafc` gray sections

### Typography
- Modern system font stack: Inter, SF Pro, Segoe UI, Roboto

## Browser Support

- Chrome/Edge (Chromium)
- Firefox
- Safari (macOS/iOS)
- Mobile browsers

## Useful Links

- **Live Site:** https://trafficserver.apache.org/
- **Buildbot:** https://ci2.apache.org/#/builders?tags=trafficserver-site
- **ASF Website Checker:** https://whimsy.apache.org/site/project/trafficserver - Checks for required ASF content (privacy policy, events link, copyright, etc.)
- **W3C Link Checker:** https://validator.w3.org/checklink?uri=https%3A%2F%2Ftrafficserver.apache.org&recursive=on - Validates links and anchors in web pages
