# Mutiny19 - Indiana Founders Charting What's Next

A cyber-pirate themed platform for Indiana founders. Automatically aggregates entrepreneur events from 100+ sources across Indiana, featuring an interactive map, captain-forged event highlighting, Discord community intel, and founder-friendly resources.

Live at: **https://mutiny19.github.io**

## Brand Identity

**Mutiny19** celebrates Indiana becoming the 19th state (December 11, 1816). The cyber-pirate theme represents founders charting their own course with full autonomy.

**Mascot:** XIX Captain Cardinal - Indiana's state bird, cyber-enhanced
**Core Values:**
- Captains Lead (founders hold the wheel)
- Transparent Maps (full visibility)
- Shipwrights Only (founders building for founders)
- Mutual Investment (collective rise)

## Features

### Event Discovery
- **100+ Sources**: Auto-scraped from TechPoint, Eventbrite, 1MC, SBDC, chambers, universities, makerspaces, and more
- **Interactive Map**: Leaflet-powered map of Indiana with event markers
- **List View**: Searchable, filterable event list with captain-forged highlighting
- **Captain-Forged Filter**: Dedicated system for founder-created events
  - ⚓ Visual badges and glowing cyan borders
  - Ghost hover effects ("CAPTAIN'S VOYAGE")
  - Quick toggle to show only captain-forged events
- **Smart Filtering**: Date range, free events, food, drinks, captain-forged
- **Daily Updates**: GitHub Actions runs scraper daily at 6 AM UTC

### Community Features
- **Discord Integration**: "Signal a New Port" form for community event submissions
- **Anonymous Intel**: Honeypot-protected submission form
- **Bilingual Support**: Full English/Spanish (i18n)

### Visual Design
- **Cyber-Pirate Theme**: CRT scanlines, neon cyan/crimson, glitch effects
- **Animated Hero**: MP4 video of XIX Captain Cardinal
- **Responsive**: Mobile-optimized with touch-friendly interactions

### Founder Resources
- **Founder-Friendly Docs**: SAFE, FAST, term sheet guides
- **Origin Story**: "The Tale of XIX Captain Cardinal" (collapsible narrative)

## Project Structure

```
.
├── index.html              # Main page
├── styles.css              # All styling (CRT effects, pirate theme)
├── app.js                  # JS logic + i18n translations (EN/ES)
├── events.json             # Event data (auto-generated daily)
├── hero-cardinal-xix.mp4   # Animated hero video
├── scraper/
│   ├── scrape_events.py   # Python scraper with Playwright support
│   ├── sources.json       # 100+ event sources + configuration
│   └── requirements.txt   # beautifulsoup4, requests, icalendar, python-dateutil, playwright
├── .github/
│   └── workflows/
│       └── scrape-events.yml  # Daily automation
└── .claude/
    ├── CLAUDE.md          # Project instructions for AI assistants
    └── settings.local.json # (gitignored)
```

## Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/mutiny19/mutiny19.git
cd mutiny19
```

### 2. Enable GitHub Pages
1. Repo Settings → Pages
2. Source: Deploy from branch `main`, root folder
3. Site live at: `https://mutiny19.github.io`

### 3. Enable GitHub Actions
1. Actions tab → Enable workflows
2. Scraper runs daily at 6 AM UTC (1 AM EST)
3. Manual trigger: Actions → "Scrape Events" → Run workflow

## Event Sources Configuration

### Adding New Sources

Edit `scraper/sources.json`:

```json
{
  "sources": [
    {
      "name": "Your Event Source",
      "type": "custom|eventbrite_search|ical|luma_event",
      "url": "https://example.com/events",
      "enabled": true,
      "description": "Brief description",
      "captainForged": false  // Set true for founder-created events
    }
  ]
}
```

### Supported Source Types

- **`custom`**: Custom websites (requires scraper logic)
- **`eventbrite_search`**: Eventbrite search results pages
- **`ical`**: iCalendar feeds (`.ics` files)
- **`luma_event`**: Single Luma.com events (with fallback for anti-bot detection)

### Manual Overrides for Difficult Sites

For sites with anti-bot protection (like Luma), add manual overrides:

```json
{
  "name": "Event Name",
  "type": "luma_event",
  "url": "https://luma.com/eventid",
  "enabled": true,
  "captainForged": true,
  "date": "2025-12-18T18:37:00",
  "location": "Venue Name, 123 Main St, Indianapolis, IN"
}
```

## Scraper Features

### Advanced Capabilities
- **Playwright Support**: Renders JavaScript-heavy sites
- **Anti-Bot Fallback**: Static HTML parsing when Playwright is blocked
- **Geocoding**: OpenStreetMap Nominatim API for precise coordinates
- **Rate Limiting**: 1 req/sec for geocoding, respects API limits
- **Caching**: Geocoding cache to reduce API calls
- **JSON-LD Parsing**: Structured data extraction for dates/locations
- **Date Parsing**: Multiple strategies (JSON-LD, time elements, text patterns)

### Captain-Forged Event Detection
Set `captainForged: true` in sources.json for founder-created events. The scraper:
1. Tags event with `captainForged` feature flag
2. Frontend applies special styling (glowing borders, badges, etc.)
3. Filterable via dedicated "Captain-Forged Only" button

### Running Scraper Locally

```bash
cd scraper
pip install -r requirements.txt
playwright install chromium  # For JavaScript rendering
python scrape_events.py
```

Output: `../events.json` (86+ events from 100+ sources)

## Local Development

### Frontend Testing
```bash
# Option 1: Direct file opening
open index.html

# Option 2: Local server (recommended)
python -m http.server 8000
# Visit http://localhost:8000
```

### Scraper Development
```bash
cd scraper
python scrape_events.py  # Run full scrape
```

## Technologies

**Frontend:**
- Vanilla HTML/CSS/JS (no framework)
- Leaflet.js for maps
- i18n translations in app.js

**Scraping:**
- Python 3.9+
- BeautifulSoup4 (HTML parsing)
- Playwright (JavaScript rendering)
- icalendar (iCal feed parsing)
- python-dateutil (date parsing)
- requests (HTTP)

**Hosting & Automation:**
- GitHub Pages (free static hosting)
- GitHub Actions (daily scraper runs)

**APIs:**
- OpenStreetMap Nominatim (geocoding)
- Discord Webhooks (community submissions)

## Key Files Reference

### `.claude/CLAUDE.md`
Project instructions for AI assistants. Contains:
- Privacy rules (no personal info, anonymous commits)
- Brand voice guidelines
- Tech stack overview
- SEO format

### `scraper/sources.json`
Master configuration for all event sources:
- 100+ sources across Indiana
- Keywords: entrepreneur, startup, tech, maker, food, art, defense, hardtech
- Excluded keywords: webinar only, virtual only, cancelled

### `app.js`
All JavaScript + translations:
- Event filtering logic
- Map/list view switching
- Captain-forged highlighting
- Discord form submission
- Bilingual support (EN/ES)

### `styles.css`
Complete styling:
- Cyber-pirate theme (neon cyan, crimson)
- CRT scanlines and glitch effects
- Captain-forged visual effects (glow, badges, hover animations)
- Responsive breakpoints

## Recent Updates (December 2025)

### Captain-Forged System
- Added `captainForged` feature flag to event schema
- Visual enhancements: cyan borders, glowing effects, corner ribbons
- Ghost hover animation ("CAPTAIN'S VOYAGE")
- Quick filter button for captain-forged-only view
- Luma event scraper with manual overrides

### Hero Section
- Animated MP4 video (hero-cardinal-xix.mp4)
- Title updated to "INDIANA FOUNDERS MUTINY19"
- Story title: "THE TALE OF XIX CAPTAIN CARDINAL"

### Messaging Updates
- Shifted from oppositional to ownership tone
- "Shipwrights Only" emphasizes mutual investment and collective rise
- Removed negative framing ("No gatekeepers" → "Full visibility")

### Scraper Enhancements
- Geocoding via Nominatim API for precise locations
- Playwright stealth mode for anti-bot bypass
- Static HTML fallback when Playwright blocked
- Manual date/location overrides in sources.json
- JSON-LD structured data parsing

## Future Tasks

### High Priority
- [ ] Fix geocoding for manual location overrides (currently defaults to city-level)
- [ ] Add more captain-forged events (currently: Indy Tech Founders Happy Hour)
- [ ] Improve Luma scraper reliability (currently using manual overrides)

### Feature Ideas
- [ ] Individual "Add to Calendar" buttons for events
- [ ] Event categories/tags beyond features
- [ ] Founder profiles/bios for captain-forged event hosts
- [ ] Event photos/images
- [ ] Search by keyword in title/description
- [ ] Save favorite events (localStorage)
- [ ] Email notifications for new captain-forged events

### Content
- [ ] Expand founder-friendly docs section
- [ ] Add FAQ or "What is Mutiny19?" explainer
- [ ] Community guidelines for Discord
- [ ] Success stories from Indiana founders

### Technical Debt
- [ ] Optimize video file size (currently 1.9MB)
- [ ] Add loading states for map/events
- [ ] Error handling for failed API calls
- [ ] Playwright cache management

## Contributing

### Adding Event Sources
1. Fork repository
2. Add source to `scraper/sources.json`
3. Test locally: `cd scraper && python scrape_events.py`
4. Verify events appear in `events.json`
5. Submit pull request

### Adding Custom Scrapers
Edit `scraper/scrape_events.py` and add logic:

```python
def scrape_custom(self, source: Dict[str, Any]):
    if source['name'] == 'Your Event Source':
        # Your scraping logic here
        # Use self.fetch_with_playwright() for JS sites
        # Use BeautifulSoup for static HTML
        pass
```

### Captain-Forged Events
To mark an event as captain-forged:
1. Add `"captainForged": true` to source in `sources.json`
2. Ensure it's genuinely created & hosted by a founder
3. Not corporate sponsors, accelerators, or third-party orgs

## Troubleshooting

### Events Not Updating
- Check Actions tab for workflow status
- Ensure GitHub Actions is enabled
- Verify workflow has write permissions

### Scraper Errors
- Review Actions logs for specific errors
- Test locally: `cd scraper && python scrape_events.py`
- Check if target website changed structure
- Some sites require Playwright: `playwright install chromium`

### Map Not Displaying
- Check browser console for errors
- Verify `events.json` is valid JSON
- Confirm lat/lng coordinates are correct

### Captain-Forged Events Not Highlighting
- Verify `captainForged: true` in events.json
- Check CSS is loaded (cyan borders, glow effects)
- Try hard refresh (Cmd+Shift+R / Ctrl+Shift+R)

## Privacy & Security

- **No personal data**: Anonymous git commits (Mutiny19 <crew@mutiny19.com>)
- **Discord webhook exposed**: Known limitation of static site, mitigated with honeypot
- **No tracking**: No analytics, cookies, or user tracking
- **Open source**: Fully transparent codebase

## Git Commit Rules

Per `.claude/CLAUDE.md`:
- Author: `Mutiny19 <crew@mutiny19.com>`
- No personal names, company names, or emails
- All commits anonymous

## License

MIT License - Build your own community!

## Credits

- **Mapping**: Leaflet.js + OpenStreetMap
- **Geocoding**: Nominatim (OpenStreetMap)
- **Hosting**: GitHub Pages
- **Automation**: GitHub Actions
- **Scraping**: BeautifulSoup, Playwright, icalendar

## Support

Questions or issues?
1. Check [existing issues](https://github.com/mutiny19/mutiny19/issues)
2. Create new issue with details
3. Include error messages and screenshots

---

**Built by captains, for captains.**
Shipwrights building for shipwrights. What we forge together strengthens our fleet.

🏴‍☠️ Join the crew: [mutiny19.github.io](https://mutiny19.github.io)
