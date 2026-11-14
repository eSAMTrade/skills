---
applyTo: '**/*.py'
---

# Copilot Instructions – Test Writing (Python)

Generate stable, low-maintenance Python tests that test specific functionalities without being fragile to minor code changes.

# Critical Rules:
- Never patch our own code. When in need to patch external dependencies, refactor our code to accept DI instead. Only patch truly external code that cannot accept DI. This is a hard rule.

## Don’t Hard-Code Constructors Everywhere - Use Factory Helpers for Non-Trivial Objects
When object creation is non-trivial or reused, centralize it in a _make_* factory. Constructor changes → update only the factory.
- No unused default params: a parameter always called with its default is dead API — remove it.
- No speculative params: only add a parameter if it is used with ≥2 distinct values in the same file.
- Hardcode the single variant if the factory only ever creates one, and reuse it across tests.

### Factory Placement
Default: same test file, never a new file just for factories.

Example (preferred) - where it's used in the same class/file::
```python
from mypkg.entsoe import Request
class TestX(TestCase):
    @staticmethod
    def _make_request(country: str) -> Request:
        return Request(country)

    def test_nominal(self) -> None:
        req = self._make_request("RO")
        
        self.assertEqual(req.country, "RO")
```
- Move to a shared module only if: it already exists and the factory is used by multiple test files. Never create a new shared module preemptively.

In that case, move the helper from the test files into the shared module and update imports. Do **not** create a new shared module preemptively for a helper
used in just one file.

## General Test Style
- Follow the project-declared test framework and its fixture conventions; default to unittest and TestCase when no convention is declared.
- Prefer calling main() directly for entrypoint tests; avoid runpy.run_module unless module-execution is the contract.
- Arrange – Act – Assert with blank lines between phases.
- Use domain-specific names: imbalance_df, request_ro, etc.
- Prefer a small real factory object over a mock when cheap.
- Unit tests never wait for the clock. Do not use `time.sleep`, `asyncio.sleep` to pass time, retry loops with a delay, or any fixed or repeated delay that only lets time pass.
  - To check that an action happens, wait for its completion signal: `Event.wait(timeout)`, `Future.result(timeout)`, or `Queue.get(timeout=...)`. The wait ends as soon as
    the signal arrives. The timeout value only stops a hung test.
  - To check that an action does not happen, do not wait and hope. Call the function that makes the decision and assert its result. If a worker thread would run the
    action, first wait until that thread has ended (`Thread.join(timeout)`), then assert.
  - To test code that reads the time, pass a fake clock or sleep function into the code and advance the fake clock in the test. Do not patch `time` in our own code.
  - In `tearDown`, stop every thread the test started and wait until it has ended (`Thread.join(timeout)`). No thread may keep running into the next test.

## Test Typing Rules
- Test helpers, fake classes, callbacks, factories, `setUp`, and `tearDown` must be clearly annotated.
- Do not use `Any` or `object` annotations in tests when a concrete fake class, callback signature, domain type, union/type alias, or small test-only value class can express the expected contract.
- Keep test doubles as narrow as the tested behavior requires. Avoid mirroring an entire production API when the test only needs one typed method or callback.

## Test Readability Rules
- Treat tests as executable explanations. A reader should quickly understand what is being tested, why the input values were chosen, and how the expected
  result follows.
- Name tests after the public contract and the distinguishing condition, not incidental implementation details. If the risk is "local timestamp must not
  affect ordering", say that directly in the name.
- Keep one behavioral axis per test (for example, do not vary time range, entity key, row order, bucket size, and value changes in the same test unless each
  variation is essential to the one behavior under test).
- Split tests when they prove separate behaviors. If several assertions must stay together, group them by concept with blank lines and local variable names
  (for example `in_ohlc` and `out_ohlc`).
- For time bucket, ordering, or stateful aggregation tests, make the scenario explicit in Arrange: use named timestamps/buckets or a compact comment table
  such as `update -> expected bucket -> expected state`.
- Prefer obvious data over clever data. Choose timestamps and values that make bucket membership, ordering, and state transitions easy to see; when
  non-obvious values are required, explain the reason in a short comment.
- Keep fixtures minimal. Avoid extra entities, contracts, columns, or rows that are not needed for the behavior being tested.
- Prefer named result rows or expected tuples over dense positional `iloc` assertions. If row position is itself the behavior, assert the ordered keys first
  so the positional assertions are justified.
- Do not use `ai_blackbox` on tests. Tests must remain readable, reviewable executable specs; use the project's draft/provenance tag only when required by
  the active project rules.

Example:
```python
class TestStore(TestCase):
    def setUp(self):
        self.req = make_req()
        self._td = tempfile.TemporaryDirectory()
        self.store = Store(self._td.name)

    def tearDown(self):
        self._td.cleanup()

    def test_blabla(self):
        df = self.store.fetch(self.req)

        self.assertEqual(list(df.columns), ["t1"])
        self.assertTrue(df["t1"].notna().all())
```
If there is **no shared factories module**, define the helpers locally in this file instead of creating a new one.

## When a Constructor Changes
Do not update tests directly. Update or introduce a _make_* factory. Keep it local unless multiple files use it and a shared module exists.
Constructor changes → update factories, not tests.

## General Anti-Patterns to Avoid
- Unused parameters with defaults that are never overridden at call sites
- Helper functions that are more general than the test suite requires
- Parameters whose only purpose is to mirror the signature of the production code being tested
- Opaque scenario setup where the reviewer must mentally simulate bucketing, sorting, or state updates to understand the expected value
- Large assertion blocks that mix unrelated concepts without splitting the test or visually grouping the assertions

## Non-Negotiable Rules (repeat)
- Never `patch` our own code.
- Factories stay in the same test file by default.
- Constructor changes → update factories, not tests.
- Use keyword args in factories to override only the values that matter.
- Type fake dependencies and callback parameters explicitly; do not hide unclear test contracts behind `Any` or `object`.
- Make non-obvious test data self-explanatory through names, grouping, or short comments.
- Keep tests small, focused, and use clear Arrange–Act–Assert structure.
