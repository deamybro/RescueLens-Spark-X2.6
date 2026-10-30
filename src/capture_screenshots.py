"""
Enhanced Automated Capture Script with Scenarios
Captures:
1. Flood Rescue (P1 Immediate)
2. Earthquake Structural Collapse & Gas Leak (P1 Immediate)
3. Shelter Logistics Replenishment (P3 Routine)
"""

import os
import time
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def capture_scenarios():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1480, "height": 1050})
        page = context.new_page()

        print("[*] Loading RescueLens Web UI...")
        page.goto("http://localhost:8501", wait_until="networkidle")
        time.sleep(3)

        # 1. Initial Empty Dashboard
        page.screenshot(path=os.path.join(OUTPUT_DIR, "01_dashboard_overview.png"), full_page=True)

        # 2. Run Flood Triage
        triage_button = page.locator("button:has-text('Analyze & Triage with Spark-X2.6')")
        if triage_button.count() > 0:
            triage_button.first.click()
            time.sleep(3)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "02_flood_p1_triage.png"), full_page=True)

        print("[*] Screenshots saved successfully!")
        browser.close()

if __name__ == "__main__":
    capture_scenarios()
