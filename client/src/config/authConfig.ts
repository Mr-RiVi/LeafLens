import { AUTH_CLIENT_ID, AUTH_ASGARDEO_BASE_URL, AUTH_SIGNINREDIRECTURL, AUTH_SIGNOUTREDIRECTURL } from "./base"

export const authConfig = {
    "clientID": AUTH_CLIENT_ID,
    "baseUrl": AUTH_ASGARDEO_BASE_URL,
    "signInRedirectURL": AUTH_SIGNINREDIRECTURL,
    "signOutRedirectURL": AUTH_SIGNOUTREDIRECTURL,
    "resourceServerURLs": [ "http://127.0.0.1:5000" ],
    "disableTrySignInSilently": false,
    "scope": [
        "openid",
        "profile"
    ]
}