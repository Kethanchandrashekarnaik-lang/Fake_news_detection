import pytest
from scraper.scraper import NewsScraper

def test_scraper_initialization():
    scraper = NewsScraper()
    assert scraper.ua is not None

def test_scraper_invalid_url():
    scraper = NewsScraper()
    result = scraper.scrape_article("http://invalid-url-that-does-not-exist.com")
    assert result['error'] is not None
    assert result['text'] == ""
