# Theme Pack Contribution Checklist

## Required Files

Every theme pack PR must include:

### 1. Theme Directory
```
themes/<theme_name>/
├── index.html          # Main HTML template
├── style.css           # Stylesheet
├── config.yaml         # Theme metadata
└── screenshots/        # Screenshot directory
```

### 2. Screenshot Requirements
- **Minimum**: 3 screenshots per theme
- **Sizes**:
  - `homepage.png`: Full homepage view (1920x1080 minimum)
  - `post_view.png`: Blog post detail view (1920x1080 minimum)
  - `mobile.png`: Mobile responsive view (375x812 minimum)
- **Format**: PNG, transparent background not required
- **Content**: Must show actual rendered output, not mockups

### 3. config.yaml Fields
```yaml
name: "Theme Name"
version: "1.0.0"
author: "Your Name"
description: "Brief description"
screenshot: "screenshots/homepage.png"
tags:
  - minimal
  - dark
  - responsive
```

### 4. Acceptance Criteria

- [ ] All required files present in theme directory
- [ ] Screenshot dimensions meet minimum requirements
- [ ] config.yaml has all required fields
- [ ] Theme renders correctly with sample content
- [ ] Mobile responsive design works
- [ ] No hardcoded paths or credentials
- [ ] README updated with new theme link

## Example Structure

```
themes/portfolio_minimal/
├── index.html
├── style.css
├── config.yaml
└── screenshots/
    ├── homepage.png (1920x1080)
    ├── post_view.png (1920x1080)
    └── mobile.png (375x812)
```

## References

- Main README: [link to project README]
- Bounty policy: [link to BOUNTY.md]
- Example themes: `themes/` directory
