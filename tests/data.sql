INSERT INTO user (username, password, fullname, pct_pings_completed, amount_earned, completion_streak, activity_low_stress, activity_happiness)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',
    'Test User', 42.4242, 42.4242, 42, 'data analysis boop beep boop', 'cleaning circuitboards ouch ouch ouch'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79',
    'Other User', 21.2121, 21.2121, 21, 'other - data analysis boop beep boop', 'other - cleaning circuitboards ouch ouch ouch');
