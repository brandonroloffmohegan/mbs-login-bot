from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "MBS Login Bot is running"}

@app.get("/cookies")
async def get_cookies():
    async with async_playwright() as p:
        # Launch browser; set headless=False for debugging if needed
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://app.mbslive.net/")
        # Wait for the page to fully load
        await page.wait_for_load_state("networkidle", timeout=60000)
        
        # Debug: capture screenshot (remove later)
        # await page.screenshot(path="debug.png")
        # Debug: print page HTML (for debugging; remove later)
        # print(await page.content())

        # Wait explicitly for the username input to appear
        await page.wait_for_selector('input[name="username"]', timeout=60000)
        
        await page.fill('input[name="username"]', 'mmbilling@gomohegan.com')
        await page.fill('input[name="password"]', '$Zh@ifB6MGLLrsCR0GGf2Ktbz')
        await page.click('button[type="submit"]')
        await page.wait_for_url("**/dashboard", timeout=60000)

        cookies = await context.cookies()
        cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

        await browser.close()
        return {"cookies": cookie_string}
