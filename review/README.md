<!-- Generated with the assistance of an AI coding tool. -->

# Native Blender proof for the #9464 supplement

This branch preserves the native-method reproduction for supplement commit
`2fb98ff4d8a50986fa7cb7ac145e5de5f824d2f5`. Its exact parent is
franklincg's carrier commit `8e3d424f4a5c00a658cf311d33800bd68ea4fc8d`.
The supplement changes only these existing files:

- `src/bonsai/bonsai/tool/blender.py` (blob `82364a23a76a0b06f26a09bc866f3ee44a393f41`)
- `src/bonsai/test/tool/test_blender.py` (blob `c01629fc9659866906c2d95e312d0ad238c92be4`)

The supplement limits local-view exit to the viewport activating a camera,
while retaining the carrier's pinning of other scene-camera views. These
proof files are separate from the production candidate branch.

## Scope and provenance

`native_carrier_repro.py` was executed by the implementing agent as
`/workspace/ifc9464-supplement-20261111/native_carrier_repro.py` using
Blender 4.3.2. It extracts four exact methods from the source file and the
exact proposed regression-test body from the test file. It uses real Blender
RNA, camera objects, context overrides and local-view operators. Only
`ROOT = Path(__file__).parent.parent` differs from the executed script,
because this copy lives in `review/`.

The script deliberately skips Bonsai imports, add-on registration and the
`NewFile` fixture. It resets Blender with
`bpy.ops.wm.read_factory_settings(use_empty=True)` instead. This is isolated
native-method evidence, not a full Bonsai integration test.

## Reproduce the recorded red/green cases

Run these commands in a disposable checkout of this verification branch.
Each Blender invocation starts a fresh process. The test file stays at the
supplement version throughout; only the source file changes for the red
cases.

Original carrier source (red):

```sh
git show 8e3d424f4a5c00a658cf311d33800bd68ea4fc8d:src/bonsai/bonsai/tool/blender.py > src/bonsai/bonsai/tool/blender.py
blender --background --factory-startup --python-exit-code 1 --python review/native_carrier_repro.py -- false
blender --background --factory-startup --python-exit-code 1 --python review/native_carrier_repro.py -- true
```

Supplement source restored (green):

```sh
git show 2fb98ff4d8a50986fa7cb7ac145e5de5f824d2f5:src/bonsai/bonsai/tool/blender.py > src/bonsai/bonsai/tool/blender.py
blender --background --factory-startup --python-exit-code 1 --python review/native_carrier_repro.py -- false
blender --background --factory-startup --python-exit-code 1 --python review/native_carrier_repro.py -- true
git diff --exit-code -- src/bonsai/bonsai/tool/blender.py
```

These commands adjust the script path for its preserved location. The
original commands used the script path at the repository root. All four
reported original invocations used `--python-exit-code 1`.

## Recorded results

The implementing agent reported the following executed results before this
evidence branch was created; the preserving reviewer did not rerun them.

| Source | Other viewport local view | Result | Exit code |
| --- | --- | --- | --- |
| Original carrier `8e3d424` | false | Assertion failure at proposed regression test line 155: other local-view state changed | 1 |
| Original carrier `8e3d424` | true | Assertion failure at proposed regression test line 155: other local-view state changed | 1 |
| Supplement `2fb98ff` | false | `CARRIER_REPRO_PASS False` | 0 |
| Supplement `2fb98ff` | true | `CARRIER_REPRO_PASS True` | 0 |

The original carrier toggles the other view into local view when it was
previously outside local view, and exits its local view when it was already
inside. The supplement preserves both states, switches the scene camera,
and retains the previous camera in the other viewport as asserted by the
exact proposed test.

The implementing agent also reported passing Ruff lint and diff-whitespace
checks on the exact two-file supplement. Source-format checking reported an
unchanged carrier helper-signature formatting issue; the test file was
formatted.

A separate full Bonsai attempt on the exact carrier worktree called
`bonsai.register()`, then
`pytest.main(['-o', 'addopts=', 'src/bonsai/test/tool/test_blender.py', '-q'])`
with the existing local dependencies. It terminated with exit 137 before
producing test results. The cause was not established. This is not a passing
integration run and does not invalidate or broaden the isolated red/green
evidence above.
