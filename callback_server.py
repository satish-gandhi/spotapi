'''Callback server for storing spotify code'''

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
import os
from datetime import datetime, timedelta, timezone
import json
import uvicorn

app = FastAPI()

STATE_FILE = ".spotify_state"
TOKEN_FILE = 'creds.json'

@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/callback", response_class=HTMLResponse)
def callback(request: Request):
    # 1) Parse query params safely
    code = request.query_params.get("code")
    incoming_state = request.query_params.get("state")
    error = request.query_params.get("error")

    # 2) Handle user denial / OAuth errors explicitly
    if error:
        raise HTTPException(status_code=400, detail=f"Spotify OAuth error: {error}")

    # 3) Server must have expected state available
    if not os.path.exists(STATE_FILE):
        raise HTTPException(status_code=500, detail=f"Missing {STATE_FILE}. Start auth flow first.")

    with open(STATE_FILE, "r") as f:
        expected_state = f.read().strip()

    if not expected_state:
        raise HTTPException(status_code=500, detail=f"{STATE_FILE} is empty.")

    # 4) Validate state (CSRF protection)
    if not incoming_state:
        raise HTTPException(status_code=400, detail="Missing state in callback.")
    if incoming_state != expected_state:
        raise HTTPException(status_code=400, detail="State mismatch.")

    # 5) Require code (needed for token exchange)
    if not code:
        raise HTTPException(status_code=400, detail="Missing code in callback.")

    # 6) Persist code for the separate auth process
    with open(TOKEN_FILE, "w") as json_file:
        now_time = datetime.now(timezone.utc) + timedelta(seconds=3600)

        dic= {'code': code, 'expire': now_time.isoformat()}

        json.dump(dic, json_file, indent=4)


    # 7) Cleanup to avoid stale state causing future confusion
    try:
        os.remove(STATE_FILE)
    except FileNotFoundError:
        pass

    # 8) Friendly browser response
    return "<h3>Approved ✅</h3><p>You can close this tab now.</p>"

if '__name__' == '__main__':
    uvicorn.run('callback_server',host="127.0.0.1", port='8888', reload=False)
