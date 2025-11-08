#!/usr/bin/env python3
"""MoodKeeper entrypoint"""
from uvicorn import run

if __name__ == '__main__':
    print('Starting MoodKeeper...')
    run('app.server:app', host='127.0.0.1', port=8001, reload=True)
