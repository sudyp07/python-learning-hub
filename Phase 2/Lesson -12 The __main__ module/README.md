# Understanding `if __name__ == "__main__"` in Python

This small project demonstrates one of the most confusing Python concepts for beginners.

## Files

- `script1.py` → Contains a `main()` function and an `if __name__ == "__main__"` block.
- `script2.py` → Imports `script1.py` to demonstrate what happens during an import.

## Run Directly

```bash
python script1.py
```

When executed directly:

- `__name__` becomes `"__main__"`
- `main()` is called automatically.

## Run Through Import

```bash
python script2.py
```

When imported:

- `__name__` becomes `"script1"`
- The condition

```python
if __name__ == "__main__":
```

evaluates to `False`.

Therefore:

- `main()` is **not** called automatically.
- You can still call it manually:

```python
script1.main()
```

## Simple Rule

```python
if __name__ == "__main__":
```

means:

> **Run this block only when this file is executed directly. Do not run it automatically when another file imports it.**