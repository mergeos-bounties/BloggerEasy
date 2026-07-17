# Theme Pack Contribution Checklist

## Overview

This document describes the requirements for contributing theme packs to BloggerEasy.

## Required Files

Each theme pack must include:

| File | Description | Required |
|------|-------------|----------|
| `theme.json` | Theme configuration | ✅ |
| `index.html` | HTML template | ✅ |
| `preview.png` | Screenshot preview | ✅ |
| `README.md` | Theme documentation | ✅ |

## File Structure

```
theme-pack-name/
├── theme.json
├── index.html
├── preview.png
└── README.md
```

## theme.json Schema

```json
{
  "name": "Theme Name",
  "description": "Brief description of the theme",
  "author": "Your Name",
  "version": "1.0.0",
  "colors": {
    "primary": "#000000",
    "secondary": "#ffffff",
    "accent": "#00ff00",
    "background": "#ffffff",
    "text": "#000000"
  },
  "fonts": {
    "heading": "Arial",
    "body": "Arial"
  },
  "layout": {
    "max_width": "1200px",
    "spacing": "20px"
  }
}
```

## Screenshot Requirements

### Size

| Dimension | Minimum | Maximum | Recommended |
|-----------|---------|---------|-------------|
| Width | 800px | 1920px | 1200px |
| Height | 600px | 1080px | 800px |
| File Size | - | 2MB | 500KB |

### Format

- **Format**: PNG
- **Color Space**: sRGB
- **Compression**: Optimized for web

### Content

- Show the full page layout
- Include sample content (text, images)
- Demonstrate responsive design (optional)
- No browser UI elements

## index.html Requirements

### Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Theme Name</title>
  <style>
    /* Theme styles here */
  </style>
</head>
<body>
  <!-- Theme content here -->
</body>
</html>
```

### Best Practices

1. **Semantic HTML**: Use proper HTML5 semantic elements
2. **Responsive**: Include viewport meta tag
3. **Accessible**: Use proper heading hierarchy
4. **Clean Code**: Well-formatted, readable code
5. **No External Dependencies**: Keep styles inline or in `<style>` tag

## README.md Template

```markdown
# Theme Name

Brief description of the theme.

## Features

- Feature 1
- Feature 2
- Feature 3

## Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Primary | #000000 | Headers, buttons |
| Secondary | #ffffff | Background |
| Accent | #00ff00 | Links, highlights |

## Screenshots

![Preview](preview.png)

## Usage

1. Download theme files
2. Place in themes directory
3. Select in BloggerEasy settings

## License

MIT License
```

## Acceptance Criteria

### Must Have

- [ ] Valid `theme.json` with all required fields
- [ ] Working `index.html` that renders correctly
- [ ] Screenshot `preview.png` at correct size
- [ ] `README.md` with theme documentation
- [ ] No broken links or images
- [ ] Responsive design (optional but recommended)

### Nice to Have

- [ ] Multiple color variations
- [ ] Dark mode support
- [ ] Animation effects
- [ ] Custom fonts

## Common Mistakes

### Mistake 1: Missing theme.json
```json
// ❌ Wrong - Missing required file
theme-pack/
├── index.html
└── preview.png

// ✅ Correct - All files present
theme-pack/
├── theme.json
├── index.html
├── preview.png
└── README.md
```

### Mistake 2: Wrong screenshot size
```
// ❌ Wrong - Too small
preview.png: 400x300px

// ✅ Correct - Proper size
preview.png: 1200x800px
```

### Mistake 3: External dependencies
```html
<!-- ❌ Wrong - External CSS -->
<link rel="stylesheet" href="https://example.com/style.css">

<!-- ✅ Correct - Inline styles -->
<style>
  /* All styles here */
</style>
```

## PR Checklist

- [ ] All required files included
- [ ] `theme.json` is valid JSON
- [ ] `index.html` renders correctly
- [ ] `preview.png` is correct size
- [ ] `README.md` is complete
- [ ] No broken links or images
- [ ] PR description explains theme purpose

## Questions?

Open an issue or comment on the PR for clarification.
