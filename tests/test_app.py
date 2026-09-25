import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from app import create_app


RUN_A = "01M3B9TQ14F0Z0NV668DHSRX71"
RUN_B = "01M3B9TQ1D6MKEJ0Z96QXBRPAE"
TOKEN = "synthetic-cleanup-token-for-tests-only-12345"


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.path = str(Path(self.temporary.name) / "fixture.db")
        self.client = create_app(self.path, TOKEN).test_client()

    def tearDown(self):
        self.temporary.cleanup()

    def register(self, run_id):
        return self.client.post(
            "/api/auth/register",
            json={
                "email": f"luowang-{run_id.lower()}-user@example.test",
                "displayName": f"luowang-{run_id.lower()}-user",
                "password": "synthetic-password-12345",
            },
        )

    def test_register_hashes_password_and_delete_invalidates_session(self):
        self.assertEqual(self.register(RUN_A).status_code, 201)
        self.assertTrue(self.client.get("/api/auth/status").json["authenticated"])
        with closing(sqlite3.connect(self.path)) as db:
            stored = db.execute("SELECT password_hash FROM users").fetchone()[0]
        self.assertTrue(stored.startswith("$argon2id$"))
        self.assertNotIn("synthetic-password-12345", stored)
        self.assertEqual(self.client.delete("/api/me").status_code, 200)
        self.assertFalse(self.client.get("/api/auth/status").json["authenticated"])
        self.assertEqual(
            self.client.post(
                "/api/auth/login",
                json={
                    "email": f"luowang-{RUN_A.lower()}-user@example.test",
                    "password": "synthetic-password-12345",
                },
            ).status_code,
            401,
        )

    def test_cleanup_is_authenticated_and_scoped_to_one_run(self):
        self.assertEqual(self.register(RUN_A).status_code, 201)
        self.assertEqual(self.register(RUN_B).status_code, 201)
        base = f"/api/luowang/test-data/{RUN_A}"
        self.assertEqual(self.client.get(base + "/storage").status_code, 401)
        headers = {"Authorization": f"Bearer {TOKEN}"}
        self.assertEqual(
            self.client.get(base + "/storage", headers=headers).json,
            {"runId": RUN_A, "accounts": 1, "argon2id": 1, "other": 0},
        )
        self.assertEqual(self.client.delete(base, headers=headers).json["remaining"], 0)
        self.assertEqual(self.client.get(base, headers=headers).json["remaining"], 0)
        self.assertEqual(
            self.client.get(f"/api/luowang/test-data/{RUN_B}", headers=headers).json["remaining"],
            1,
        )

    def test_seeded_login_account_is_outside_run_cleanup(self):
        client = create_app(self.path, TOKEN, ("seed@example.test", "seed-password-12345")).test_client()
        login = client.post(
            "/api/auth/login",
            json={"email": "seed@example.test", "password": "seed-password-12345"},
        )
        self.assertEqual(login.status_code, 201)
        headers = {"Authorization": f"Bearer {TOKEN}"}
        self.assertEqual(
            client.delete(f"/api/luowang/test-data/{RUN_A}", headers=headers).json["remaining"], 0
        )
        self.assertTrue(client.get("/api/auth/status").json["authenticated"])


if __name__ == "__main__":
    unittest.main()
