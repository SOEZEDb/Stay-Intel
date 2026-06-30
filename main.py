from playwright.sync_api import sync_playwright, Playwright
import random
import sqlite3

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.google.com/maps/search/hotel+in+ikeja/@6.5385121,3.2538571,12z/data=!3m1!4b1?entry=ttu&g_ep=EgoyMDI2MDYxNi4wIKXMDSoASAFQAw%3D%3D")

    conn  = sqlite3.connect("StayIntel.db")
    cursor = conn.cursor()
    cursor.execute ("""
        CREATE TABLE IF NOT EXISTS StayIntel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT,
            link  TEXT UNIQUE,
            provisions  TEXT,
            rating NUMERIC
        )
    """)


    try:
        accept_button = page.wait_for_selector("span.UywwFc-RLmnJb")
        accept_button.click()
        page.wait_for_timeout(random.randint(4000, 7000))
        page.wait_for_selector("div[role='article']")
    except:
        pass


    panel = page.wait_for_selector('div[role="feed"]')
    for _ in range(50):
        panel.evaluate("el => el.scrollBy(0, el.clientHeight * 0.8)")
        page.wait_for_timeout(random.randint(4000,7000))

    hotels = page.locator("div[role='article']").all()
    for hotel in hotels:
        name = hotel.locator("a[aria-label]").first.get_attribute("aria-label")
        link = hotel.locator("a[href]").first.get_attribute("href")
        provisions = (hotel.locator("div.qty3Ue").inner_text().strip())
        print(provisions)
        ratings_locator = hotel.locator("div.Lui3Od").inner_text().split()
        rating = None
        for item in ratings_locator:
            try:
                num = float(item)
                if 1.0 <= num <= 5.0:
                    rating = num
                    break
            except ValueError:
                pass

        cursor.execute("""
            INSERT OR IGNORE  INTO StayIntel (name, link, provisions, rating)
            VALUES (?, ?, ?, ?)
        """, (name, link, provisions, rating))
    conn.commit()
    conn.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)