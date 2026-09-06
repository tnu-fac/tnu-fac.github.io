from playwright.sync_api import sync_playwright
import pathlib

path = "سنة أولى/الفصل الأول/أساسيات علوم الحاسب"
file = "book"

HTML = str(pathlib.Path(f"{path}/{file}.html").resolve())

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file://{HTML}", wait_until="networkidle")
    page.pdf(
        path=f"{path}/{file}.pdf",
        format="A4",
        print_background=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
    )
    browser.close()