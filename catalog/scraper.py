from playwright.sync_api import sync_playwright

URL = "https://www.shl.com/products/product-catalog/"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(URL, wait_until="networkidle", timeout=60000)

    print("Title:", page.title())
    print("Current URL:", page.url)

    # Save the page HTML
    html = page.content()

    with open("catalog/page.html", "w", encoding="utf-8") as file:
        file.write(html)

    print("Saved HTML to catalog/page.html")

    input("Press ENTER to close the browser...")

    browser.close()