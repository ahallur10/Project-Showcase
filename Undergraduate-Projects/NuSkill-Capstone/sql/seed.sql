INSERT INTO users (email, password_hash) VALUES ('demo@example.com', '$pbkdf2-sha256$29000$demo$L0b8QeNfFakeHashOnlyForLayout');
INSERT INTO tutorials (slug, title) VALUES ('intro-python', 'Intro to Python');
INSERT INTO deposits (user_id, amount_usd, refund_eligible, consumed) VALUES (1, 10.0, 0, 0);
