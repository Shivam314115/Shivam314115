import json
import requests
from bs4 import BeautifulSoup
import os

USERNAME = "Shivam314115"
URL = f"https://github.com/users/{USERNAME}/contributions"

def fetch_contributions():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    print(f"Fetching {URL}...")
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch contributions: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    days = soup.find_all("td", class_="ContributionCalendar-day")
    
    contributions = []
    
    for day in days:
        date_str = day.get("data-date")
        if not date_str:
            continue
            
        level = day.get("data-level", "0")
        
        contributions.append({
            "date": date_str,
            "level": int(level)
        })
            
    total = 0
    total_h2 = soup.find("h2", class_="f4 text-normal mb-2")
    if total_h2:
        try:
            total_text = total_h2.text.strip().replace(",", "").split(" ")[0]
            total = int(total_text)
        except:
            pass

    data = {
        "total": total,
        "days": contributions
    }
    
    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(contributions)} days of contributions to data/contributions.json")

if __name__ == "__main__":
    fetch_contributions()
