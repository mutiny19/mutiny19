# Mutiny19 Project Instructions

## Privacy & Security Rules

**CRITICAL: Never include personal information in any code, commits, or files:**
- No real names (first, last, or full names)
- No company names associated with the maintainer
- No email addresses (except crew@mutiny19.com)
- No usernames or account references

**Git commits must use:**
- Author: Mutiny19 <crew@mutiny19.com>
- All commits should be anonymous

**If you need to reset history:**
```bash
rm -rf .git && git init && git add -A && git commit -m "Initial commit"
git remote add origin https://github.com/mutiny19/mutiny19.git
git push --force origin main
```

## Project Overview

Mutiny19 is a cyber-pirate themed website for Indiana entrepreneurs featuring:
- Event calendar with filterable events
- Community Intel form (anonymous reporting)
- Discord integration
- Captain Cardinal mascot (XIX)

## Tech Stack

- Static HTML/CSS/JS (no framework)
- Leaflet.js for maps
- Python scraper for events
- GitHub Pages hosting

## Key Files

- `index.html` - Main page
- `styles.css` - All styling
- `app.js` - All JavaScript
- `events.json` - Event data
- `scraper/` - Python event scraper
