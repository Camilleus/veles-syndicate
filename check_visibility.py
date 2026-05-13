import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        url = "http://localhost:3000"
        await page.goto(url)
        await page.wait_for_timeout(2000)

        hero_id = await page.evaluate("document.getElementById('hero') ? 'exists' : 'missing'")
        active_sections = await page.evaluate("Array.from(document.querySelectorAll('section.active')).map(s => s.id)")
        display = await page.evaluate("document.getElementById('hero') ? window.getComputedStyle(document.getElementById('hero')).display : 'n/a'")
        opacity = await page.evaluate("document.getElementById('hero') ? window.getComputedStyle(document.getElementById('hero')).opacity : 'n/a'")

        print(f"Hero ID: {hero_id}")
        print(f"Active Sections: {active_sections}")
        print(f"Hero Display: {display}")
        print(f"Hero Opacity: {opacity}")

        await browser.close()

if __name__ == "__main__":
    import subprocess
    server = subprocess.Popen(["python3", "-m", "http.server", "3000", "--bind", "0.0.0.0"])
    try:
        asyncio.run(check())
    finally:
        server.terminate()
