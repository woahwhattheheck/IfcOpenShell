<!-- This file was generated with the assistance of an AI coding tool. -->

# Native local-view review evidence for #6432

These are isolated native-Blender method proofs, not complete Bonsai/IFC integration results. The two Python files reconstruct the code actually executed on Blender 4.3.2; only disclosure/provenance comments have been added. They read production methods using Python AST and execute those methods against actual Blender objects, areas and local-view state.

## Source distinction

The failed cases used the **original retained #6432 patch**, not the later repaired candidate:

- Official upstream base checked out during review: `75390dab765afa87a88ae38e83880c0a8df17bba`.
- Retained bank: `woahwhattheheck/bug-bounty`, branch `claude/zen-cerf-rrfj52`, file `bounty-work/IfcOpenShell__IfcOpenShell__6432/fix.patch`.
- Exact retained patch Git blob: `e147b25279d1e191722ecab32b7fec9c0b2bfb72`. Its original preparation base was `f96911ce5cca7c31b963226108329ee43e57b4c8`; it applied cleanly at the later review base above.
- Local review checkout was `/workspace/ifc6432-verify-20261111`, with HEAD at the official base and the retained patch applied to the worktree. Both scripts intentionally retain that actually used path. Set up a fresh review checkout there before reproducing; do not overwrite a live caller's checkout.
- This verification branch is based on repaired candidate `b1de4db048def334c1100802671f5c29eb5cd787` solely to preserve the evidence beside it. **No result below is a full validation of that candidate.**

## Camera activation proof

The script selects the exact `Blender.activate_camera` method. Its only bound helper returns the actual target area A.

```sh
REVIEW_MODE=baseline blender --background --factory-startup --python-exit-code 1 --python review/native_local_view_repro.py
REVIEW_MODE=current blender --background --factory-startup --python-exit-code 1 --python review/native_local_view_repro.py
REVIEW_MODE=narrow blender --background --factory-startup --python-exit-code 1 --python review/native_local_view_repro.py
```

Recorded output:

| Mode | Source | Before B local view | After B local view | Result |
| --- | --- | --- | --- | --- |
| baseline | Original upstream method from review checkout HEAD | True | True | PRESERVED baseline |
| current | Original retained-patch method | True | False | AssertionError: Unrelated user local view was exited |
| narrow | Same retained method, with only `if a != area: continue` inserted in its screen-area loop | True | True | PRESERVED narrow |

The first current-mode invocation omitted `--python-exit-code 1`: Blender printed the assertion traceback but returned exit 0. Later baseline/current/narrow commands included the flag; their combined shell invocation returned 0 because its final narrow command passed. Do not interpret the initial exit 0 as a test pass.

The candidate's target-only implementation is semantically the narrowing checked here, but its exact final method has not been rerun by this reviewer.

## Final-unlock proof

```sh
blender --background --factory-startup --python-exit-code 1 --python review/native_final_unlock_repro.py
```

The script executes the exact retained methods `is_viewport_locked_to_drawing`, `is_drawing_local_view`, `unlock_viewport_from_drawing` and `exit_viewport_local_view`. Area enumeration and drawing-camera classification are supplied as fixture dependencies; actual cameras, objects and local views are Blender-native.

Recorded output:

```text
B_STILL_LOCAL True
B_RECOGNIZED_AS_DRAWING_LOCAL False
OLD_WALL_GLOBALLY_VISIBLE True
AssertionError: Transient local view survives final unlock
```

That standalone command exited 1. It demonstrates the retained patch's leftover temporary local view and union visibility after removing the final lock. The later candidate cleanup was not executed in this proof.

## Remaining checks

Full Bonsai registration/IFC/operator tests, exact repaired-candidate execution, model-mode unlock behavior, multiple scene-following camera viewports, and GUI acceptance remain separate. The runtime became unavailable during follow-up work; no new execution or pass is inferred from these preserved scripts.
