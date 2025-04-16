from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "MBS Login Bot is running"}

@app.get("/cookies")
async def get_cookies():
    async with async_playwright() as p:
        # Launch browser in headless mode (set headless=False for debugging if needed)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to the login page
        await page.goto("https://app.mbslive.net/")
        # Wait until network activity is idle to ensure the page has loaded completely
        await page.wait_for_load_state("networkidle", timeout=60000)

        # Wait for the login input fields to be visible
        await page.wait_for_selector('input[name="UserName"]', timeout=60000)
        await page.wait_for_selector('input[name="Password"]', timeout=60000)

        # Fill in the login form using the correct field names
        await page.fill('input[name="UserName"]', 'mmbilling@gomohegan.com')
        await page.fill('input[name="Password"]', '$Zh@ifB6MGLLrsCR0GGf2Ktbz')

        # Click the submit button (adjust the selector if necessary)
        await page.click('button[type="submit"]')

        # Wait for the dashboard page to load (adjust the URL pattern if needed)
        await page.wait_for_url("**/dashboard", timeout=60000)

        # Retrieve the cookies from the current context
        cookies = await context.cookies()
        cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

        await browser.close()
        return {"cookies": cookie_string}
