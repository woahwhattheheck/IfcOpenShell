# This file was generated with the assistance of an AI coding tool.
# SPDX-License-Identifier: GPL-3.0-or-later
# Reconstructed from the actually executed isolated native-method review script.
# See README.md: source must be the ORIGINAL RETAINED PATCH.
import ast
from pathlib import Path
from typing import Optional, Union, Iterable
from types import SimpleNamespace
import bpy

source = Path('/workspace/ifc6432-verify-20261111/src/bonsai/bonsai/tool/drawing.py').read_text()
tree = ast.parse(source)
source_class = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Drawing')
names = {'is_viewport_locked_to_drawing', 'is_drawing_local_view', 'unlock_viewport_from_drawing', 'exit_viewport_local_view'}
methods = [n for n in source_class.body if isinstance(n, ast.FunctionDef) and n.name in names]
review_class = ast.ClassDef(name='Reviewed', bases=[], keywords=[], body=methods, decorator_list=[])
module = ast.fix_missing_locations(ast.Module(body=[review_class], type_ignores=[]))
exec(compile(module, '<actual-drawing-lock-methods>', 'exec'), globals())
bpy.ops.wm.read_factory_settings(use_empty=False)
screen = bpy.context.screen
area_a = next(a for a in screen.areas if a.type == 'VIEW_3D')
area_b = next(a for a in screen.areas if a.type == 'DOPESHEET_EDITOR')
area_b.type = 'VIEW_3D'
areas = [area_a, area_b]
tool = SimpleNamespace(Blender=SimpleNamespace(get_view3d_areas=lambda: areas))
wall_a = bpy.data.objects['Cube']
wall_a.name = 'WallA'
bpy.ops.mesh.primitive_cube_add(location=(10, 0, 0))
wall_b = bpy.context.active_object
wall_b.name = 'WallB'
camera_a = bpy.data.objects['Camera']
camera_a.name = 'DrawingA'
camera_b = bpy.data.objects.new('DrawingB', bpy.data.cameras.new('DrawingB'))
bpy.context.scene.collection.objects.link(camera_b)
bpy.context.scene.camera = camera_b
Reviewed.is_drawing_camera = classmethod(lambda cls, obj: obj in (camera_a, camera_b))

def enter_local_view(area, objects):
    region = next(r for r in area.regions if r.type == 'WINDOW')
    with bpy.context.temp_override(area=area, region=region, space_data=area.spaces.active):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = objects[0]
        bpy.ops.view3d.localview(frame_selected=False)
    area.spaces.active.region_3d.view_perspective = 'CAMERA'

enter_local_view(area_a, [wall_a, camera_a])
area_a.spaces.active.camera = camera_a
area_a.spaces.active.use_local_camera = True
enter_local_view(area_b, [wall_b, camera_b])
area_b.spaces.active.use_local_camera = False
assert Reviewed.is_viewport_locked_to_drawing(area_a.spaces.active)
assert Reviewed.is_drawing_local_view(area_b.spaces.active)
assert not wall_a.hide_get() and not wall_b.hide_get()
Reviewed.unlock_viewport_from_drawing(area_a)
print('B_STILL_LOCAL', bool(area_b.spaces.active.local_view))
print('B_RECOGNIZED_AS_DRAWING_LOCAL', Reviewed.is_drawing_local_view(area_b.spaces.active))
print('OLD_WALL_GLOBALLY_VISIBLE', not wall_a.hide_get())
assert area_b.spaces.active.local_view is None, 'Transient local view survives final unlock'
