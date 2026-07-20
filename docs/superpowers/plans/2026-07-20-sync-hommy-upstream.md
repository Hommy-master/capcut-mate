# Sync Hommy Upstream Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Merge `Hommy-master/capcut-mate` `main` into the latest `WQfans/capcut-mate` `main` while preserving the fork's Ken Burns image animation support and adopting upstream's transition-duration behavior.

**Architecture:** Work on `codex/sync-upstream`, created from `origin/main`, so the currently running checkout is unchanged during integration. Resolve the single `src/service/add_images.py` conflict by composing the independent behaviors from both sides: retain Ken Burns parsing and keyframe generation, and treat a missing or empty transition duration as `None` so the transition type supplies its default duration.

**Tech Stack:** Python 3.11, standard-library `unittest`, pytest project suite, Git merge workflow.

## Global Constraints

- Preserve `ken_burns` request parsing and scale/X/Y keyframe generation from the WQfans fork.
- Adopt upstream behavior where omitted or empty `transition_duration` becomes `None` and is passed to `add_transition` as the transition type's default duration.
- Preserve an explicitly supplied numeric `transition_duration` as an integer.
- Do not rewrite published history; use a merge commit.
- Do not alter or stop the currently running CapCut Mate process until the merged branch has passed verification.

---

### Task 1: Lock the Conflict Resolution Contract with Tests

**Files:**
- Create: `tests/test_add_images_upstream_merge.py`

**Interfaces:**
- Consumes: `src.service.add_images.parse_image_data(json_str: str) -> List[Dict[str, Any]]`
- Produces: Regression coverage for Ken Burns preservation and transition-duration normalization.

- [ ] **Step 1: Write the failing tests**

```python
import json
import unittest

from src.service.add_images import parse_image_data


class AddImagesUpstreamMergeTests(unittest.TestCase):
    def _image(self, **overrides):
        image = {
            "image_url": "https://example.com/image.png",
            "start": 0,
            "end": 2_000_000,
            "transition": "叠化",
            "ken_burns": {
                "start_scale": 1.0,
                "end_scale": 1.06,
                "start_x": 0,
                "end_x": 0.03,
            },
        }
        image.update(overrides)
        return image

    def test_missing_transition_duration_uses_default_and_keeps_ken_burns(self):
        parsed = parse_image_data(json.dumps([self._image()]))[0]

        self.assertIsNone(parsed["transition_duration"])
        self.assertEqual(1.06, parsed["ken_burns"]["end_scale"])

    def test_empty_transition_duration_uses_default(self):
        parsed = parse_image_data(
            json.dumps([self._image(transition_duration="")])
        )[0]

        self.assertIsNone(parsed["transition_duration"])

    def test_explicit_transition_duration_is_preserved(self):
        parsed = parse_image_data(
            json.dumps([self._image(transition_duration=750_000)])
        )[0]

        self.assertEqual(750_000, parsed["transition_duration"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify the intended red state**

Run: `../capcut-mate/.venv/bin/python -m unittest tests.test_add_images_upstream_merge -v`

Expected: the missing-duration assertion reports `500000 is not None`, and the empty-string case fails because the fork has not yet adopted upstream normalization.

- [ ] **Step 3: Commit the failing regression tests**

Run: `git add tests/test_add_images_upstream_merge.py && git commit -m "test: cover upstream image merge behavior"`

Expected: one test-only commit is created before the upstream merge.

### Task 2: Merge Upstream and Resolve the Single Conflict

**Files:**
- Modify: `src/service/add_images.py`
- Modify automatically through merge: files changed by `upstream/main`

**Interfaces:**
- Consumes: `image_infos` JSON objects with optional `ken_burns` and `transition_duration` fields.
- Produces: Parsed image dictionaries that retain `ken_burns`; `add_image_to_draft` applies Ken Burns keyframes and passes either an explicit integer duration or `None` to `video_segment.add_transition`.

- [ ] **Step 1: Merge upstream without committing**

Run: `git merge --no-commit --no-ff upstream/main`

Expected: Git reports one content conflict in `src/service/add_images.py`; all other upstream changes merge automatically.

- [ ] **Step 2: Resolve `src/service/add_images.py`**

Keep the WQfans `KeyframeProperty` import, `ken_burns` documentation, keyframe generation block, and parsed `ken_burns` field. Adopt upstream's transition behavior:

```python
transition_duration = image.get('transition_duration')
if transition_duration is not None and transition_duration != "":
    transition_duration = int(transition_duration)
else:
    transition_duration = None
video_segment.add_transition(transition_enum, duration=transition_duration)
```

Set the parser default to:

```python
"transition_duration": item.get("transition_duration", None),
"ken_burns": item.get("ken_burns", None),
```

Remove the old hard-coded `[100000, 2500000]` fallback-to-`500000` validation so omitted durations can reach the transition implementation as `None`.

- [ ] **Step 3: Run the targeted tests and verify green**

Run: `../capcut-mate/.venv/bin/python -m unittest tests.test_add_images_upstream_merge -v`

Expected: `Ran 3 tests` and `OK`.

- [ ] **Step 4: Commit the merge**

Run: `git add src/service/add_images.py docs/superpowers/plans/2026-07-20-sync-hommy-upstream.md && git commit`

Expected: one merge commit with both parents, containing the manual conflict resolution; the preceding parent commit contains the regression tests.

### Task 3: Verify, Publish, and Activate

**Files:**
- No additional source files expected.

**Interfaces:**
- Consumes: completed merge branch.
- Produces: tested `origin/main` and matching local running checkout source.

- [ ] **Step 1: Run syntax and test verification**

Run: `../capcut-mate/.venv/bin/python -m compileall -q src tests`

Expected: exit code 0.

Run: `pytest -q` using an environment with the project dev dependencies installed.

Expected: all collected automated tests pass; environment-specific/manual tests are reported separately if they require external services.

- [ ] **Step 2: Review the final branch diff and merge topology**

Run: `git diff --check && git status --short && git log --oneline --graph -n 8`

Expected: no whitespace errors, no uncommitted files, and the new commit has `origin/main` and `upstream/main` as parents.

- [ ] **Step 3: Push the tested merge to the fork**

Run: `git push origin HEAD:main`

Expected: `origin/main` advances to the merge commit without force-push.

- [ ] **Step 4: Fast-forward the local runtime checkout**

Run in `.cache/capcut-mate`: `git merge --ff-only origin/main`

Expected: local `main` matches `origin/main`; the untracked `src/capcut_mate.egg-info/` remains untouched.
