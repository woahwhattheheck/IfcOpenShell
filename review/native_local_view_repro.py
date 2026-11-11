# This file was generated with the assistance of an AI coding tool.
# SPDX-License-Identifier: GPL-3.0-or-later
# Reconstructed from the actually executed isolated native-method review script.
# See README.md: "current" means the ORIGINAL RETAINED PATCH, not b1de4db.
import ast
import os
import subprocess
from pathlib import Path
from typing import Optional
import bpy

checkout = '/workspace/ifc6432-verify-20261111'
mode = os.environ.get('REVIEW_MODE', 'current')
if mode == 'baseline':
    source = subprocess.check_output(['git', '-C', checkout, 'show', 'HEAD:src/bonsai/bonsai/tool/blender.py'], text=True)
else:
    source = Path(checkout + '/src/bonsai/bonsai/tool/blender.py').read_text()
tree = ast.parse(source)
cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Blender')
method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'activate_camera')
if mode == 'narrow':
    loop = next(n for n in method.body if isinstance(n, ast.For))
    loop.body.insert(0, ast.parse('if a != area: continue').body[0])
review_cls = ast.ClassDef(name='Reviewed', bases=[], keywords=[], body=[method], decorator_list=[])
module = ast.fix_missing_locations(ast.Module(body=[review_cls], type_ignores=[]))
exec(compile(module, '<actual-activate_camera>', 'exec'), globals())
bpy.ops.wm.read_factory_settings(use_empty=False)
screen = bpy.context.screen
area_a = next(a for a in screen.areas if a.type == 'VIEW_3D')
area_b = next(a for a in screen.areas if a.type == 'DOPESHEET_EDITOR')
area_b.type = 'VIEW_3D'
space_b = area_b.spaces.active
region = next(r for r in area_b.regions if r.type == 'WINDOW')
bpy.ops.object.select_all(action='DESELECT')
obj = bpy.data.objects.get('Cube')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
with bpy.context.temp_override(area=area_b, region=region, space_data=space_b):
    bpy.ops.view3d.localview(frame_selected=False)
assert space_b.local_view is not None
assert area_a.spaces.active.local_view is None
assert not space_b.use_local_camera
print('BEFORE', bool(space_b.local_view))
Reviewed.get_view3d_area = classmethod(lambda cls: area_a)
Reviewed.activate_camera(bpy.data.objects['Camera'])
print('AFTER', bool(space_b.local_view))
assert space_b.local_view is not None, 'Unrelated user local view was exited'
print('PRESERVED', mode)
