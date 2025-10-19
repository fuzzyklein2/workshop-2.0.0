
# pytest Tutorial Conversation

This document captures a conversation about **pytest** — Python’s testing framework — and related tools and practices.

---

## 🧩 Writing Your First Test

```python
# test_math.py
def test_addition():
    assert 2 + 2 == 4
```

Run it with:
```bash
pytest
```

Pytest automatically finds tests whose names start with `test_`.

---

## 🧠 How `pytest` Finds and Runs Tests

- Files named `test_*.py` or `*_test.py`.
- Functions named `test_*`.
- Classes named `Test*`.

Pytest runs them automatically when you execute `pytest` in the project root.

---

## 🧩 Example: Testing a Config Reader

### `mypackage/config.py`

```python
import os
from pathlib import Path

def get_config_contents():
    config_path = os.environ.get("CONFIG_PATH")
    if not config_path:
        raise RuntimeError("CONFIG_PATH not set")
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text()
```

### `tests/test_config.py`

```python
from mypackage.config import get_config_contents

def test_get_config_contents(monkeypatch, tmp_path):
    config_file = tmp_path / "config.txt"
    config_file.write_text("DEBUG=True\nAPI_KEY=12345")

    monkeypatch.setenv("CONFIG_PATH", str(config_file))

    contents = get_config_contents()

    assert "DEBUG=True" in contents
    assert "API_KEY=12345" in contents
```

Run it with:
```bash
pytest -s tests/test_config.py
```

---

## 🧰 Built-in Fixtures: `tmp_path` and `monkeypatch`

| Fixture | What it does | Why it’s useful |
|----------|---------------|----------------|
| `tmp_path` | Gives a temporary directory | Keeps your real filesystem clean |
| `monkeypatch` | Temporarily modifies env vars, attributes, or imports | Avoids global side effects |

---

## 🧩 Reusable Fixtures with `conftest.py`

### `tests/conftest.py`

```python
import pytest

@pytest.fixture
def fake_config_env(tmp_path, monkeypatch):
    config_file = tmp_path / "config.txt"
    config_file.write_text("DEBUG=True\nAPI_KEY=xyz789")
    monkeypatch.setenv("CONFIG_PATH", str(config_file))
    yield config_file
```

### `tests/test_config.py`

```python
from mypackage.config import get_config_contents

def test_config_contents(fake_config_env):
    contents = get_config_contents()
    assert "DEBUG=True" in contents
    assert "API_KEY=xyz789" in contents

def test_config_file_exists(fake_config_env):
    assert fake_config_env.exists()
```

---

## 🧠 Key Takeaways

| Concept | Description |
|----------|-------------|
| Fixture | Reusable setup/teardown helper |
| `conftest.py` | Special file to share fixtures across tests |
| `yield` | Defines pre-test and post-test phases |
| `scope` | Controls how often a fixture runs (`function`, `module`, `session`) |

---

✅ With pytest, you can automate test runs before every commit or push, ensuring nothing breaks unexpectedly.

