# Modernize Apache Traffic Server Website

## Overview
Create a completely new, modern version of the trafficserver.apache.org website in `newsite/` directory using Tailwind CSS for responsive mobile and desktop support. The existing site remains untouched until you're ready to deploy.

## Design Specifications

### Visual Style: Tech/Modern
- Gradients and depth effects for visual interest
- Subtle animations and transitions on hover
- Contemporary tech-focused aesthetic
- Clean, professional appearance similar to GitHub/Stripe

### Color Palette
- **Primary Navy:** `#1e3a8a` (dark blue for headers/nav)
- **Accent Blue:** `#3b82f6` (bright blue for CTAs and highlights)
- **Secondary Text:** `#64748b` (slate gray)
- **Background:** White with subtle gray sections `#f8fafc`
- **Gradients:** Blue to cyan for hero and prominent buttons

### Typography
- **Modern system fonts:** Inter, -apple-system, SF Pro, Segoe UI fallback
- **Weight hierarchy:** Light (300), Regular (400), Semibold (600), Bold (700)
- **Improved line-height and spacing** for better readability on all devices

### Key Components
- **Download Button:** Large, prominent gradient button with hover effects
- **Feature Cards:** Clean cards with subtle shadows and smooth hover animations
- **Responsive Navigation:** Sticky header that collapses to hamburger menu on mobile
- **Modern Footer:** Multi-column layout that stacks on mobile

## Implementation Steps

### 1. Create New Site Structure
- Create `newsite/` directory with subdirectories: `source/`, `content/`, `content/styles/`, `content/js/`, `content/images/`
- Copy necessary assets (images, logos) from existing site
- Set up basic file structure for the new site

### 2. Build Modern HTML Template
- Create `newsite/source/template.html` with HTML5 and Tailwind CSS CDN
- Implement responsive navigation with mobile hamburger menu
- Create modern header with sticky positioning
- Build clean footer with proper link organization
- Add mobile menu toggle JavaScript

### 3. Create Homepage
- Build `newsite/content/index.html` with modern hero section
- Design prominent download CTA with gradient styling
- Create responsive feature cards (Caching, Proxying, Fast, Extensible, Proven)
- Style "Learn More" section with clean card grid
- Add "News" section with improved typography
- Implement "Miscellaneous" section

### 4. Create Additional Pages
- Build modern versions of: downloads.html, users.html, press.html, assistance.html, acknowledgements.html
- Apply consistent styling and navigation across all pages
- Ensure all internal links work within newsite structure

### 5. Add Styles and Scripts
- Create `newsite/content/styles/custom.css` for any brand-specific overrides
- Add mobile menu JavaScript to `newsite/content/js/menu.js`
- Implement smooth scroll and transition effects
- Ensure accessibility with proper ARIA labels and focus states

### 6. Copy/Update Python Build Script
- Copy `generate.py` to `newsite/source/generate.py`
- Update paths to work within newsite directory structure
- Create markdown source files if needed
- Test that build script works correctly

### 7. Testing
- Test all pages on mobile (320px, 375px, 768px)
- Test on tablet and desktop viewports (1024px, 1440px+)
- Verify all navigation links work
- Check that download buttons and external links function
- Ensure Apache license headers are preserved

## Directory Structure
```
newsite/
├── source/
│   ├── template.html (modern Tailwind template)
│   ├── generate.py (build script)
│   └── markdown/ (markdown source files)
├── content/ (generated HTML output)
│   ├── index.html
│   ├── downloads.html
│   ├── users.html
│   ├── press.html
│   ├── assistance.html
│   ├── acknowledgements.html
│   ├── styles/
│   │   └── custom.css
│   ├── js/
│   │   └── menu.js
│   └── images/ (copied from existing site)
```

## Key Benefits
- Existing site remains completely untouched
- Can test thoroughly before deployment
- Easy to compare old vs new
- Simple to deploy when ready (just replace old content with newsite/content)

## Implementation Todos
1. Create newsite directory structure and copy assets
2. Create modern HTML5 template with Tailwind and responsive nav
3. Build modern homepage with hero, features, and CTAs
4. Create remaining pages with consistent styling
5. Add custom CSS, JavaScript for mobile menu and effects
6. Set up Python build script in newsite directory
7. Test on mobile, tablet, and desktop viewports




