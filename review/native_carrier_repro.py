# Generated with the assistance of an AI coding tool.
"""Execute exact carrier methods and the proposed test with real Blender RNA.

This deliberately skips the Bonsai add-on import/bootstrap. It is isolated
native-method evidence, not full Bonsai integration coverage.
"""

import ast
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).parent.parent
source = ast.parse((ROOT / "src/bonsai/bonsai/tool/blender.py").read_text())
original_class = next(node for node in source.body if isinstance(node, ast.ClassDef) and node.name == "Blender")
method_names = {
    "activate_camera",
    "get_view3d_area",
    "get_view3d_spaces",
    "pin_scene_camera_to_other_viewports",
}
methods = [node for node in original_class.body if isinstance(node, ast.FunctionDef) and node.name in method_names]
assert len(methods) == len(method_names)
isolated_class = ast.ClassDef(name="Blender", bases=[], keywords=[], body=methods, decorator_list=[])
module = ast.Module(body=[ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0), isolated_class], type_ignores=[])
namespace = {"bpy": bpy}
exec(compile(ast.fix_missing_locations(module), "exact-carrier-methods", "exec"), namespace)

tests = ast.parse((ROOT / "src/bonsai/test/tool/test_blender.py").read_text())
test_class = next(node for node in tests.body if isinstance(node, ast.ClassDef) and node.name == "TestPinSceneCameraToOtherViewports")
test = next(node for node in test_class.body if isinstance(node, ast.FunctionDef) and node.name == "test_activating_from_local_view_preserves_other_viewport")
test.decorator_list = []
test_module = ast.Module(body=[test], type_ignores=[])
namespace["subject"] = namespace["Blender"]
exec(compile(ast.fix_missing_locations(test_module), "proposed-regression-test", "exec"), namespace)

bpy.ops.wm.read_factory_settings(use_empty=True)
other_local_view = sys.argv[sys.argv.index("--") + 1] == "true"
print("CARRIER_REPRO other_local_view=", other_local_view, flush=True)
namespace[test.name](None, other_local_view)
print("CARRIER_REPRO_PASS", other_local_view, flush=True)
