import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        errors = []
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.on("console", lambda msg: errors.append(f"{msg.type}: {msg.text}") if msg.type == "error" else None)

        url = "http://localhost:3000"
        try:
            await page.goto(url, wait_until="networkidle")
        except Exception as e:
            errors.append(f"Goto error: {str(e)}")

        print("--- Errors ---")
        for err in errors:
            print(err)
        print("--------------")

        # Check if #hero is visible
        is_visible = await page.is_visible("#hero")
        print(f"Hero visible: {is_visible}")

        # Check main content
        content = await page.content()
        print(f"Content length: {len(content)}")

        await page.screenshot(path="debug_black_screen.png")
        await browser.close()

if __name__ == "__main__":
    import subprocess
    server = subprocess.Popen(["python3", "-m", "http.server", "3000", "--bind", "0.0.0.0"])
    try:
        asyncio.run(check())
    finally:
        server.terminate()
