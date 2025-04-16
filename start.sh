#!/bin/bash
npx playwright install --with-deps
uvicorn main:app --host 0.0.0.0 --port 10000
