# New Modern Apache Traffic Server Website

This directory contains a modernized, responsive version of the Apache Traffic Server website built with Tailwind CSS.

## Overview

This is a complete redesign of the trafficserver.apache.org website featuring:
- Modern, responsive design using Tailwind CSS
- Mobile-first approach with hamburger menu for small screens
- Clean, contemporary tech aesthetic with gradients and smooth animations
- Improved typography and spacing for better readability
- Sticky navigation header
- Modern footer with organized links

## Design Specifications

### Visual Style
- Tech/Modern aesthetic similar to GitHub/Stripe
- Gradients and subtle animations
- Contemporary color palette

### Colors
- **Primary Navy:** `#1e3a8a` - Used for headers and navigation
- **Accent Blue:** `#3b82f6` - Used for CTAs and highlights
- **Secondary Text:** `#64748b` - Used for body text
- **Background:** White with gray sections (`#f8fafc`)

### Typography
- Modern system font stack: Inter, SF Pro, Segoe UI, Roboto
- Improved hierarchy and spacing for readability

## Directory Structure

```
newsite/
├── source/
│   ├── template.html          # Modern HTML5 template with Tailwind
│   ├── generate.py            # Python script to build HTML from markdown
│   └── markdown/              # Markdown source files
├── content/                   # Generated HTML output
│   ├── index.html            # Homepage (manually created)
│   ├── downloads.html        # Generated from markdown
│   ├── users.html            # Generated from markdown
│   ├── press.html            # Generated from markdown
│   ├── assistance.html       # Generated from markdown
│   ├── acknowledgements.html # Generated from markdown
│   ├── styles/
│   │   └── custom.css        # Custom CSS for brand-specific styles
│   ├── js/
│   │   └── menu.js           # Mobile menu toggle functionality
│   └── images/               # Copied from existing site
```

## Building the Site

To regenerate pages from markdown:

```bash
cd source
python3 generate.py
```

## Testing

The site has been designed to work on:
- Mobile devices (320px - 768px)
- Tablets (768px - 1024px)
- Desktop (1024px+)

To test locally:
1. Navigate to the `content/` directory
2. Open `index.html` in a browser
3. Use browser dev tools to test responsive layouts

## Features

### Homepage (content/index.html)
- Eye-catching gradient hero section
- Prominent download CTA button with hover effects
- Responsive feature cards with icons
- Timeline-style news section
- Modern footer with organized links

### Other Pages
- Generated from markdown using the template
- Consistent navigation and footer
- Responsive content layout

### Responsive Navigation
- Desktop: Horizontal navigation with all links visible
- Mobile: Hamburger menu that slides down smoothly
- Sticky header that stays visible on scroll

### Custom Styling
- Gradient buttons with hover effects
- Card hover animations
- Smooth transitions
- Accessibility features (focus states, ARIA labels)

## Deployment

When ready to deploy:

1. Test thoroughly in multiple browsers and devices
2. Verify all links work correctly
3. Replace the current `content/` directory with `newsite/content/`
4. Update any deployment scripts to use the new structure

## Notes

- The homepage (`index.html`) is a static HTML file and not generated from markdown
- All other pages are generated from markdown files in `source/markdown/`
- Tailwind CSS is loaded via CDN for simplicity
- Custom styles are in `content/styles/custom.css`
- Mobile menu JavaScript is in `content/js/menu.js`




