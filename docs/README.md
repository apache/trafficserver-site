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

2. Run the generator:

```bash
cd source
python3 generate.py
```

3. Commit and push the changes.

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
