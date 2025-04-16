from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "MBS Login Bot is running"}

@app.get("/cookies")
async def get_cookies():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://app.mbslive.net/")
        await page.fill('input[name="username"]', 'mmbilling@gomohegan.com')
        await page.fill('input[name="password"]', '$Zh@ifB6MGLLrsCR0GGf2Ktbz')
        await page.click('button[type="submit"]')
        await page.wait_for_url("**/dashboard")

        cookies = await context.cookies()
        cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

        await browser.close()
        return {"cookies": cookie_string}
