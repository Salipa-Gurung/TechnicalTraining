# Pact Contract Testing — Live Demo Script

A ~5 minute demo: two fictional services, `OrderService` (consumer) and
`UserService` (provider). We prove they agree on an API contract — then
break the provider on purpose to show what a broken contract looks like.

## Setup (do this before the talk, not live)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Part 1 — "The consumer defines what it needs" (~1 min)

Open `tests/contract/test_consumer_pact.py` and talk through it:
- OrderService expects `GET /users/1` to return a 200 with `name` and `status`.
- No real UserService is running — Pact spins up a mock server.

Run it live:

```bash
pytest tests/contract/test_consumer_pact.py -v
```

**Note:** the test itself explicitly calls `pact.write_file(PACT_DIR, overwrite=True)`
at the end — the contract file isn't written automatically just because the
test passed, it's written when you ask Pact to serialize it. Worth calling
out live since it trips people up.

Show the generated contract — this is the artifact that gets shared with
the provider team:

```bash
cat tests/contract/pacts/OrderService-UserService.json
```

**Talking point:** this JSON file is the "contract." It's generated
automatically from the consumer's expectations — nobody hand-writes it.

## Part 2 — "The provider proves it honors that contract" (~1 min)

Start the real provider in one terminal:

```bash
python3 src/provider.py
```

In another terminal, verify it against the contract:

```bash
pytest tests/contract/test_provider_verify.py -v
```

**Talking point:** this is a real HTTP call to the real provider, replaying
the exact interaction the consumer recorded. It passes because both sides
agree on the shape of `/users/1`.

## Part 3 — "Now let's break it" (~2 min, the payoff)

Edit `src/provider.py` and rename the field:

```diff
- "status": "active",
+ "state": "active",
```

Restart the provider, re-run the verification:

```bash
pytest tests/contract/test_provider_verify.py -v
```

**It fails, with a specific and readable diff:**

```
has a matching body (FAILED)
  $ -> Actual map is missing the following keys: status
```

This is the moment to land the point: without Pact, this mismatch is only
caught when OrderService breaks in staging or production. With Pact, it's
caught in CI, on the provider's own build, before it ships — and the failure
message tells you exactly what field is wrong, not just "something broke."

Revert the change afterward so the repo is clean:

```bash
git checkout src/provider.py   # if you're using git, or just undo manually
```

## Closing talking points

- The consumer never talks to a real provider in its test suite — fast,
  no shared test environment needed.
- The provider's CI pipeline pulls contracts (often from a Pact Broker)
  and verifies against them on every build — so a breaking change is
  caught at the source, not downstream.
- This scales past two services: a Pact Broker tracks which consumer
  versions are compatible with which provider versions, so you always
  know if it's safe to deploy.
