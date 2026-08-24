# Wispbyte keep-alive

Orphan branch. Keeps a free Wispbyte server from being archived; not part of
the site. The workflow lives on the default branch as
`.github/workflows/Auto-login.yml` and checks this branch out to run
`keepalive.py`, which documents the rest.

## The one part that needs a human

Turnstile means the session has to be created by hand, once per account:

1. Log in at wispbyte.com.
2. DevTools -> Network -> click the `dashboard` document request.
3. Request Headers -> copy the `connect.sid=...` pair out of `Cookie`.
4. Add it to the `LOGIN_ACCOUNTS` secret.

Then **do not log out** - that destroys the session server-side and the stored
cookie with it. Close the tab instead. For several accounts, capture each from
a separate browser profile so they are signed in at the same time.
