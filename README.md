# LuoWang Python fixture

An isolated, synthetic Python web app for LuoWang multi-project acceptance. It uses Flask, Argon2id, SQLite, and a project-specific Python execution image. It must only run in a non-production environment with synthetic Run-marked accounts.

Run locally with `pip install -r requirements.txt` and `python app.py`. Set `APP_DATA_DIR` to a disposable directory. The Run-scoped cleanup endpoints are disabled unless `CYNOS_TEST_DATA_CLEANUP_TOKEN` is set to a token of at least 32 characters; keep that token outside Git.

For an isolated login fixture, set `CYNOS_TEST_ACCOUNT_EMAIL` and `CYNOS_TEST_ACCOUNT_PASSWORD` together. The app seeds that non-production account once; Run-scoped cleanup never removes it.

The `scenario-testing` branch holds long-lived scenarios and formal LuoWang reports. The `main` branch holds product code. This fixture intentionally supports testing Issue, Pull Request, image rebuild, browser evidence, and cleanup paths; reports should describe actual behavior at their fixed commit.
