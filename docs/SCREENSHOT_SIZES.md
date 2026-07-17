# Screenshot Sizes for Theme-Pack PR Evidence

## Overview

This document defines the recommended screenshot sizes for theme-pack bounty PRs. Following these guidelines ensures consistency and helps reviewers evaluate your work effectively.

## Required Screenshots

### Desktop Screenshots

| Type | Width | Height | Format | Description |
|------|-------|--------|--------|-------------|
| **Full Page** | 1280px | 720px (min) | PNG | Complete theme view |
| **Header** | 1280px | 400px | PNG | Top section with navigation |
| **Content Area** | 1280px | 800px | PNG | Main content section |
| **Footer** | 1280px | 300px | PNG | Bottom section |

### Mobile Screenshots

| Type | Width | Height | Format | Description |
|------|-------|--------|--------|-------------|
| **Full Page** | 390px | 844px (min) | PNG | Complete mobile view |
| **Header** | 390px | 200px | PNG | Mobile navigation |
| **Content** | 390px | 600px | PNG | Main content area |
| **Menu** | 390px | 400px | PNG | Mobile menu/hamburger |

## Screenshot Guidelines

### Desktop (1280px)

```
┌─────────────────────────────────────────────┐
│                 Header (400px)              │
├─────────────────────────────────────────────┤
│                                             │
│              Content Area                   │
│              (800px min)                    │
│                                             │
├─────────────────────────────────────────────┤
│                 Footer (300px)              │
└─────────────────────────────────────────────┘
Total: 1280 x 1500px minimum
```

### Mobile (390px)

```
┌───────────────┐
│  Header (200) │
├───────────────┤
│               │
│   Content     │
│   (600px)     │
│               │
├───────────────┤
│  Menu (400)   │
└───────────────┘
Total: 390 x 1200px minimum
```

## How to Take Screenshots

### Using Browser DevTools

1. **Open DevTools** (F12 or Cmd+Shift+I)
2. **Toggle Device Toolbar** (Cmd+Shift+M)
3. **Select device** or set custom size
4. **Set width**: 1280px (desktop) or 390px (mobile)
5. **Take screenshot**: Cmd+Shift+P → "Capture screenshot"

### Using Extensions

- **Desktop**: Full Page Screen Capture
- **Mobile**: Responsive Design Mode in Firefox

### Command Line (Puppeteer)

```javascript
// Desktop screenshot
await page.setViewport({ width: 1280, height: 800 });
await page.screenshot({ path: 'desktop.png', fullPage: true });

// Mobile screenshot
await page.setViewport({ width: 390, height: 844 });
await page.screenshot({ path: 'mobile.png', fullPage: true });
```

## PR Evidence Requirements

### Minimum Screenshots

For theme-pack PRs, include:

1. **Desktop Full Page** (required)
2. **Mobile Full Page** (required)
3. **Desktop Detail** (optional but recommended)
4. **Mobile Detail** (optional but recommended)

### Naming Convention

```
theme-name-desktop-full.png
theme-name-mobile-full.png
theme-name-desktop-detail.png
theme-name-mobile-detail.png
```

### File Size Limits

| Type | Max Size | Recommended |
|------|----------|-------------|
| PNG | 5MB | < 2MB |
| JPEG | 1MB | < 500KB |

## Quality Standards

### Desktop Screenshots

- ✅ **Resolution**: 1280px width minimum
- ✅ **Full page**: Complete scrollable content
- ✅ **No artifacts**: Clean, crisp rendering
- ✅ **Complete elements**: All UI elements visible
- ✅ **Consistent styling**: Theme applied correctly

### Mobile Screenshots

- ✅ **Resolution**: 390px width
- ✅ **Full page**: Complete mobile view
- ✅ **Touch targets**: Adequate button sizes
- ✅ **Responsive**: Proper mobile layout
- ✅ **No overflow**: No horizontal scrolling

## Common Mistakes

### ❌ Don't Do This

- Wrong width (e.g., 1920px instead of 1280px)
- Cropped screenshots (missing content)
- Low resolution (blurry images)
- Wrong aspect ratio (stretched/compressed)
- Missing mobile screenshots

### ✅ Do This

- Exact 1280px or 390px width
- Full page capture
- High resolution (Retina ready)
- Correct aspect ratio
- Both desktop and mobile

## Tools Recommendation

### Screenshot Tools

| Tool | Platform | Notes |
|------|----------|-------|
| **Snipping Tool** | Windows | Built-in, basic |
| **Screenshot** | Mac | Built-in, Cmd+Shift+4 |
| **FireShot** | Browser | Full page capture |
| **Puppeteer** | CLI | Automated screenshots |

### Image Optimization

| Tool | Purpose |
|------|---------|
| **TinyPNG** | Compress PNG |
| **ImageOptim** | Optimize images |
| **Squoosh** | Modern compression |

## References

- [Responsive Design Basics](https://web.dev/responsive-web-design-basics/)
- [Mobile-First Design](https://www.mobilemouse.com/)
- [Screenshot Best Practices](https://blog.hubspot.com/)
