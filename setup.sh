#!/bin/sh
# Setup data base path
export DATABASE_URL=""
# Setup Auth0 credentials
export AUTH0_DOMAIN="gunnvantcoffee.us.auth0.com"
export API_AUDIENCE="casting"
export ALGORITHMS="RS256"
export CLIENT_ID = "8RZRHC0TgvGEUPIuQaaZz9jUcYwh0ZYr"
export CALLBACK_URL = "http://localhost:5000/api/token"