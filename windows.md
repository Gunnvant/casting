## Setting up environment variables in powershell

Make sure you are in the root folder of the app.

```powershell
$env:AUTH0_DOMAIN="gunnvantcoffee.us.auth0.com"
$env:API_AUDIENCE="casting"
$env:ALGORITHMS="RS256"
$env:DATABASE_URL="postgresql://postgres:gun125@localhost:5432/capstone"
$env:CLIENT_ID = "8RZRHC0TgvGEUPIuQaaZz9jUcYwh0ZYr"
$env:CALLBACK_URL = "http://localhost:5000/api/token"
$env:FLASK_HOME="run_local.py"
$env:FLASK_ENV="development"
$env:FLASK_DEBUG=1
```