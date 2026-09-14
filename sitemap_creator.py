"""
Human-Touch XML & Markdown Sitemap Creator
Crawls target domain, extracts clean metadata, assigns human-curated priority tiers,
and produces both search-engine XML and clean human-readable Markdown/HTML sitemaps.
"""

import sys
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[!] Installing missing dependencies...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"])
    import requests
    from bs4 import BeautifulSoup


class HumanTouchSitemap:
    def __init__(self, base_url: str, max_depth: int = 2):
        self.base_url = base_url.rstrip("/")
        self.domain = urlparse(base_url).netloc
        self.max_depth = max_depth
        self.visited = set()
        self.pages = []  # [{url, title, depth, priority, changefreq}]

    def _determine_human_priority(self, path: str) -> tuple:
        """Assigns sensible priorities based on real user interest, not just bots."""
        clean_path = path.strip("/").lower()
        if clean_path in ("", "home"):
            return (1.0, "daily", "Core Landing")
        elif any(k in clean_path for k in ["project", "portfolio", "service", "pricing"]):
            return (0.8, "weekly", "Commercial / Portfolio")
        elif any(k in clean_path for k in ["about", "contact", "team"]):
            return (0.6, "monthly", "Company Info")
        elif any(k in clean_path for k in ["blog", "news", "articles"]):
            return (0.7, "weekly", "Editorial & Content")
        return (0.5, "monthly", "General Page")

    def crawl(self, url: str = None, depth: int = 0):
        if url is None:
            url = self.base_url
        if depth > self.max_depth or url in self.visited:
            return

        self.visited.add(url)
        print(f"[+] Crawling ({depth}): {url}")

        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "HumanTouchSitemapBot/1.0"})
            if resp.status_code != 200 or "text/html" not in resp.headers.get("Content-Type", ""):
                return

            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else urlparse(url).path

            priority, changefreq, category = self._determine_human_priority(urlparse(url).path)
            self.pages.append({
                "url": url,
                "title": title,
                "category": category,
                "priority": priority,
                "changefreq": changefreq,
                "lastmod": datetime.now().strftime("%Y-%m-%d")
            })

            # Harvest internal links
            for a in soup.find_all("a", href=True):
                href = a["href"].split("#")[0].split("?")[0]
                full_url = urljoin(url, href).rstrip("/")
                if urlparse(full_url).netloc == self.domain and full_url not in self.visited:
                    self.crawl(full_url, depth + 1)

        except Exception as e:
            print(f"[-] Error crawling {url}: {e}")

    def export_xml(self, filename="sitemap.xml"):
        urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for p in self.pages:
            url_el = ET.SubElement(urlset, "url")
            ET.SubElement(url_el, "loc").text = p["url"]
            ET.SubElement(url_el, "lastmod").text = p["lastmod"]
            ET.SubElement(url_el, "changefreq").text = p["changefreq"]
            ET.SubElement(url_el, "priority").text = str(p["priority"])

        xml_str = minidom.parseString(ET.tostring(urlset)).toprettyxml(indent="  ")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(xml_str)
        print(f"[✓] XML Sitemap saved to: {filename}")

    def export_markdown(self, filename="SITEMAP.md"):
        content = ["# 🗺️ Human-Touch Visual Sitemap\n", f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} for **{self.base_url}**\n\n"]
        # Group by category
        categories = {}
        for p in self.pages:
            categories.setdefault(p["category"], []).append(p)

        for cat, items in categories.items():
            content.append(f"### {cat}\n")
            for item in items:
                content.append(f"- [{item['title']}]({item['url']}) `(Priority: {item['priority']})`\n")
            content.append("\n")

        with open(filename, "w", encoding="utf-8") as f:
            f.writelines(content)
        print(f"[✓] Human-Readable Markdown Sitemap saved to: {filename}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://shrinithiinfra.in"
    print(f"\n--- Starting Human Touch Sitemap Creator for {target} ---")
    bot = HumanTouchSitemap(target, max_depth=1)
    bot.crawl()
    bot.export_xml("sitemap.xml")
    bot.export_markdown("SITEMAP.md")
    print(f"\n[DONE] Crawled {len(bot.pages)} pages successfully!")