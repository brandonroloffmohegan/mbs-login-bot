import subprocess

# Install Playwright browsers in Python context
subprocess.run(["python", "-m", "playwright", "install", "--with-deps"], check=True)
