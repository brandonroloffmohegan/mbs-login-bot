import subprocess

print("Installing Playwright browsers for Python...")
subprocess.run(["python", "-m", "playwright", "install", "--with-deps"], check=True)
