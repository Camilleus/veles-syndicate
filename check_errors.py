import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        errors = []
        page.on("pageerror", lambda exc: errors.append(exc))
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

        url = "http://localhost:3000"
        await page.goto(url)
        await page.wait_for_timeout(2000)

        print("Errors found:", errors)
        await page.screenshot(path="debug_screen.png")
        await browser.close()

if __name__ == "__main__":
    import subprocess
    server = subprocess.Popen(["python3", "-m", "http.server", "3000", "--bind", "0.0.0.0"])
    try:
        asyncio.run(check())
    finally:
        server.terminate()
