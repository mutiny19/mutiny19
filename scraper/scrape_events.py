#!/usr/bin/env python3
"""
Indiana Entrepreneur Events Scraper
Scrapes events from various sources and outputs to events.json
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
import re

class EventScraper:
    def __init__(self, sources_file='sources.json'):
        """Initialize the scraper with sources configuration"""
        with open(sources_file, 'r') as f:
            config = json.load(f)
            self.sources = config['sources']
            self.keywords = config['keywords']
            self.excluded_keywords = config['excluded_keywords']

        self.events = []
        self.seen_events = set()  # To avoid duplicates

    def scrape_all(self) -> List[Dict[str, Any]]:
        """Scrape all enabled sources"""
        print("Starting scraper...")

        for source in self.sources:
            if not source.get('enabled', True):
                continue

            print(f"Scraping: {source['name']}")
            try:
                if source['type'] == 'eventbrite_search':
                    self.scrape_eventbrite(source)
                elif source['type'] == 'meetup_group':
                    self.scrape_meetup(source)
                elif source['type'] == 'custom':
                    self.scrape_custom(source)
            except Exception as e:
                print(f"Error scraping {source['name']}: {e}")

        print(f"Total events scraped: {len(self.events)}")
        return self.events

    def scrape_eventbrite(self, source: Dict[str, Any]):
        """Scrape Eventbrite search results"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(source['url'], headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Note: Eventbrite structure changes frequently
            # This is a basic example - may need updates
            events = soup.find_all('div', class_='discover-search-desktop-card')

            for event_elem in events[:10]:  # Limit to 10 events per source
                try:
                    title_elem = event_elem.find('h3') or event_elem.find('h2')
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)

                    # Check if event matches keywords
                    if not self._matches_keywords(title):
                        continue

                    # Extract event details
                    link_elem = event_elem.find('a', href=True)
                    url = link_elem['href'] if link_elem else source['url']

                    # Try to extract date
                    date_elem = event_elem.find('time') or event_elem.find('p', class_=re.compile('date'))
                    event_date = self._parse_date(date_elem.get_text(strip=True) if date_elem else '')

                    if not event_date or event_date < datetime.now():
                        continue

                    event_data = {
                        'title': title,
                        'url': url,
                        'date': event_date.isoformat(),
                        'source': source['name']
                    }

                    self._add_event(event_data)

                except Exception as e:
                    print(f"Error parsing Eventbrite event: {e}")
                    continue

        except Exception as e:
            print(f"Error fetching Eventbrite: {e}")

    def scrape_meetup(self, source: Dict[str, Any]):
        """Scrape Meetup.com events"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(source['url'], headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Note: Meetup requires authentication for API
            # This is basic scraping - consider using Meetup API with key
            event_elements = soup.find_all('div', {'data-event-label': True})

            for event_elem in event_elements[:10]:
                try:
                    title_elem = event_elem.find('h3') or event_elem.find('span', class_=re.compile('eventTitle'))
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)

                    if not self._matches_keywords(title):
                        continue

                    link_elem = event_elem.find('a', href=True)
                    url = link_elem['href'] if link_elem else source['url']
                    if url.startswith('/'):
                        url = 'https://www.meetup.com' + url

                    event_data = {
                        'title': title,
                        'url': url,
                        'source': source['name']
                    }

                    self._add_event(event_data)

                except Exception as e:
                    print(f"Error parsing Meetup event: {e}")
                    continue

        except Exception as e:
            print(f"Error fetching Meetup: {e}")

    def scrape_custom(self, source: Dict[str, Any]):
        """Scrape custom sources (specific implementations)"""
        name = source.get('name', '')

        if 'TechPoint' in name:
            self.scrape_techpoint(source)
        elif '1 Million Cups' in name or '1MC' in name:
            self.scrape_1mc(source)
        else:
            print(f"No custom scraper implemented for {name}")

    def scrape_techpoint(self, source: Dict[str, Any]):
        """Scrape TechPoint events"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(source['url'], headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # TechPoint uses Elementor/Jet Listing Grid
            event_items = soup.find_all('div', class_='jet-listing-grid__item')

            print(f"Found {len(event_items)} potential events on TechPoint")

            for item in event_items[:15]:  # Limit to 15 events
                try:
                    # Extract title
                    title_elem = item.find(class_='event-title') or item.find('h3') or item.find('h2')
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)

                    # Extract link
                    link = item.find('a', href=True)
                    url = link['href'] if link else source['url']
                    if url.startswith('/'):
                        url = 'https://techpoint.org' + url

                    # Extract date
                    date_str = ''
                    month_elem = item.find(class_='month')
                    day_elem = item.find(class_='day')

                    if month_elem and day_elem:
                        month = month_elem.get_text(strip=True)
                        day = day_elem.get_text(strip=True)
                        date_str = f"{month} {day}, 2025"  # Assume current/next year

                    event_date = self._parse_date(date_str) if date_str else None

                    # Skip past events
                    if event_date and event_date < datetime.now():
                        continue

                    # Extract description
                    desc_elem = item.find(class_='jet-listing-dynamic-field__content')
                    description = desc_elem.get_text(strip=True) if desc_elem else title

                    event_data = {
                        'title': title,
                        'description': description,
                        'url': url,
                        'date': event_date.isoformat() if event_date else datetime.now().isoformat(),
                        'source': source['name']
                    }

                    self._add_event(event_data)
                    print(f"  Added: {title}")

                except Exception as e:
                    print(f"Error parsing TechPoint event: {e}")
                    continue

        except Exception as e:
            print(f"Error fetching TechPoint: {e}")

    def scrape_1mc(self, source: Dict[str, Any]):
        """Scrape 1 Million Cups events"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(source['url'], headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 1MC typically has recurring events
            # Try to find event schedule or calendar
            event_items = soup.find_all(['div', 'article'], class_=re.compile('event|meeting|schedule'))

            if not event_items:
                # Generate recurring event for 1MC (they meet regularly)
                # Indianapolis meets Wednesdays, South Bend meets 2nd Wednesday
                city = 'Indianapolis' if 'indy' in source['url'].lower() else 'South Bend'

                event_data = {
                    'title': f'1 Million Cups {city}',
                    'description': 'Join entrepreneurs every month for coffee, conversation, and connections. Two startup presentations followed by community feedback and networking.',
                    'url': source['url'],
                    'date': self._get_next_1mc_date(city).isoformat(),
                    'source': source['name']
                }

                self._add_event(event_data)
                print(f"  Added recurring: 1 Million Cups {city}")

        except Exception as e:
            print(f"Error fetching 1MC: {e}")

    def _get_next_1mc_date(self, city: str) -> datetime:
        """Get next 1 Million Cups meeting date"""
        from datetime import timedelta

        today = datetime.now()

        if 'South Bend' in city:
            # 2nd Wednesday of month at 8 AM
            day = 1
            while day <= 31:
                try:
                    candidate = datetime(today.year, today.month, day, 8, 0)
                    if candidate.weekday() == 2:  # Wednesday
                        week_num = (day - 1) // 7 + 1
                        if week_num == 2 and candidate > today:
                            return candidate
                except ValueError:
                    break
                day += 1

            # Try next month
            next_month = today.month + 1 if today.month < 12 else 1
            next_year = today.year if today.month < 12 else today.year + 1
            day = 1
            while day <= 31:
                try:
                    candidate = datetime(next_year, next_month, day, 8, 0)
                    if candidate.weekday() == 2:
                        week_num = (day - 1) // 7 + 1
                        if week_num == 2:
                            return candidate
                except ValueError:
                    break
                day += 1

        else:  # Indianapolis - typically weekly Wednesdays
            days_ahead = 2 - today.weekday()  # Wednesday = 2
            if days_ahead <= 0:
                days_ahead += 7
            next_wed = today + timedelta(days=days_ahead)
            return next_wed.replace(hour=9, minute=0, second=0, microsecond=0)

        return today + timedelta(days=7)

    def _matches_keywords(self, text: str) -> bool:
        """Check if text matches any keywords and doesn't match excluded keywords"""
        text_lower = text.lower()

        # Check excluded keywords first
        for excluded in self.excluded_keywords:
            if excluded.lower() in text_lower:
                return False

        # Check if matches any keyword
        for keyword in self.keywords:
            if keyword.lower() in text_lower:
                return True

        return False

    def _parse_date(self, date_string: str) -> datetime:
        """Parse date string into datetime object"""
        try:
            return date_parser.parse(date_string)
        except:
            return None

    def _add_event(self, event_data: Dict[str, Any]):
        """Add event to list if not duplicate"""
        # Create unique identifier
        identifier = f"{event_data.get('title', '')}_{event_data.get('date', '')}"

        if identifier not in self.seen_events:
            self.seen_events.add(identifier)
            self.events.append(event_data)

    def enrich_events(self):
        """Enrich events with additional data and geocoding"""
        print("Enriching events with geocoding...")

        # Default Indiana locations for events without specific addresses
        indiana_cities = {
            'indianapolis': {'lat': 39.7684, 'lng': -86.1581},
            'fort wayne': {'lat': 41.0793, 'lng': -85.1394},
            'evansville': {'lat': 37.9747, 'lng': -87.5558},
            'south bend': {'lat': 41.6764, 'lng': -86.2520},
            'carmel': {'lat': 39.9784, 'lng': -86.1180},
            'bloomington': {'lat': 39.1653, 'lng': -86.5264}
        }

        for event in self.events:
            # Try to determine location from title or URL
            location_found = False
            title_lower = event.get('title', '').lower()

            for city, coords in indiana_cities.items():
                if city in title_lower:
                    event['location'] = {
                        'name': city.title(),
                        'address': f'{city.title()}, Indiana',
                        'lat': coords['lat'],
                        'lng': coords['lng']
                    }
                    location_found = True
                    break

            if not location_found:
                # Default to Indianapolis
                event['location'] = {
                    'name': 'Indianapolis',
                    'address': 'Indianapolis, IN',
                    'lat': 39.7684,
                    'lng': -86.1581
                }

            # Set default features (would need actual detection from event description)
            event['features'] = {
                'free': 'free' in event.get('title', '').lower(),
                'food': 'food' in event.get('title', '').lower() or 'lunch' in event.get('title', '').lower(),
                'appetizers': 'appetizer' in event.get('title', '').lower(),
                'nonAlcoholDrinks': True,  # Assume most have non-alcoholic options
                'alcoholDrinks': 'happy hour' in event.get('title', '').lower() or 'beer' in event.get('title', '').lower()
            }

            # Add missing fields
            if 'organizer' not in event:
                event['organizer'] = event.get('source', 'Unknown')

            if 'description' not in event:
                event['description'] = f"Entrepreneur event: {event.get('title', '')}"

            if 'id' not in event:
                event['id'] = str(abs(hash(event.get('title', '') + event.get('date', ''))))

    def save_to_json(self, output_file='../events.json'):
        """Save scraped events to JSON file"""
        output = {
            'lastUpdated': datetime.now().isoformat(),
            'events': self.events
        }

        output_path = os.path.join(os.path.dirname(__file__), output_file)

        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"Saved {len(self.events)} events to {output_path}")

def main():
    """Main function"""
    try:
        scraper = EventScraper()
        scraper.scrape_all()
        scraper.enrich_events()
        scraper.save_to_json()
        print("Scraping completed successfully!")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
