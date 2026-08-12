# Code Review: 02_buggy_data_processor.py

## Summary

This script processes customer orders from a JSON file and calculates
totals. While it works for simple, well-formed input, it has several
bugs and anti-patterns that will cause silent data loss, incorrect
calculations, and crashes on realistic input.

---

## 1. File Is Never Closed (`load_orders`)

**Issue:**
```python
f = open(filename)
data = json.load(f)
return data
```
The file handle is opened but never explicitly closed.

**Why it matters:**
This leaks a file descriptor every time the function runs, which can
exhaust the OS's file descriptor limit in long-running processes.

**Fix:**
```python
def load_orders(filename):
    with open(filename) as f:
        return json.load(f)
```

---

## 2. Mutable Default Argument (`calculate_total`)

**Issue:**
```python
def calculate_total(order, discounts=[]):
```

**Why it matters:**
Mutable default arguments are created once when the function is
defined, not each time it's called. If mutated in place, the change
persists across future calls, causing subtle bugs.

**Fix:**
```python
def calculate_total(order, discounts=None):
    if discounts is None:
        discounts = []
```

---

## 3. Silent Failure with Bare `except: pass` (`process_orders`)

**Issue:**
```python
except:
    pass
```

**Why it matters:**
This silently swallows every exception. Orders that fail to process
disappear from the results with no warning or log.

**Fix:**
```python
except (KeyError, TypeError) as e:
    logger.warning("Skipping order %s: %s", order.get("id", "unknown"), e)
```

---

## 4. No Validation of Order Structure

**Issue:** `calculate_total` assumes fields like `items`, `price`, and
`qty` always exist, with no checks.

**Fix:** Validate required fields exist and have the correct type
before use, raising a clear error otherwise.

---

## 5. Division by Zero Risk (`summarize`)

**Issue:**
```python
average = total_sum / len(results)
```

**Why it matters:** If `results` is empty, this crashes with
`ZeroDivisionError`.

**Fix:**
```python
average = total_sum / len(results) if results else 0
```

---

## 6. `apply_discount_code` Has Inconsistent Side Effects

**Issue:** The function both mutates `order` in place and returns a
value, making its behavior harder to predict and test.

**Fix:** Prefer one clear behavior only — mutation or return, not both.

---

## 7. Manual String Concatenation for Printing

**Issue:**
```python
print("Total: " + str(total_sum))
```

**Fix:**
```python
print(f"Total: {total_sum}")
```

---

## 8. No Type Hints or Docstrings

Functions don't document expected input/output types.

---

## Priority Summary

| Priority | Issue |
|----------|-------|
| High     | Silent `except: pass` hides real errors |
| High     | Mutable default argument |
| Medium   | File handle never closed |
| Medium   | No input validation on order structure |
| Medium   | Division by zero on empty results |
| Low      | Mixed mutation/return in `apply_discount_code` |
| Low      | Non-idiomatic string formatting |
| Low      | Missing docstrings/type hints |

See `fixed/02_buggy_data_processor.py` for the corrected version.
