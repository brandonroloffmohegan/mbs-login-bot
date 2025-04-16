from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "MBS Login Bot is running"}

@app.get("/cookies")
async def get_cookies():
    async with async_playwright() as p:
        # You can optionally set headless=False during debugging to see the browser, 
        # but for production, headless=True is preferred.
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://app.mbslive.net/")
        # Wait until the network is idle to ensure resources have loaded
        await page.wait_for_load_state("networkidle")
        # Wait explicitly for the username input to appear (timeout set to 60000ms)
        await page.wait_for_selector('input[name="username"]', timeout=150000)

        # Now fill in the login details and click submit
        await page.fill('input[name="username"]', 'mmbilling@gomohegan.com')
        await page.fill('input[name="password"]', '$Zh@ifB6MGLLrsCR0GGf2Ktbz')
        await page.click('button[type="submit"]')
        # Wait for the dashboard URL to appear. Increase the timeout if necessary.
        await page.wait_for_url("**/dashboard", timeout=60000)

        cookies = await context.cookies()
        cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        await browser.close()
        return {"cookies": cookie_string}
