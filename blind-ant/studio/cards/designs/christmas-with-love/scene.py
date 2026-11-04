# Blind Ant Cards: "Christmas With Love", built in Blender from its description.
# Description (written first, always true):
#   Two lit candles glow side by side on a dark wooden table, among glossy holly leaves
#   and clusters of red berries, with soft golden lights blurred in the darkness behind them.
# Run: blender -b -P christmas_with_love.py -- <out.png> [samples] [size]
import bpy, bmesh, math, random, sys
from mathutils import Vector

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = args[0] if args else '//christmas_with_love.png'
SAMPLES = int(args[1]) if len(args) > 1 else 64
SIZE = int(args[2]) if len(args) > 2 else 1080
random.seed(12)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ---------- materials ----------
def mat(name, color, rough=0.5, metal=0.0, emit=None, strength=0.0, sss=0.0, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if sss:
        p.inputs['Subsurface Weight'].default_value = sss
        p.inputs['Subsurface Radius'].default_value = (0.6, 0.35, 0.2)
        p.inputs['Subsurface Scale'].default_value = 0.08
    if coat:
        p.inputs['Coat Weight'].default_value = coat
        p.inputs['Coat Roughness'].default_value = 0.08
    if emit:
        p.inputs['Emission Color'].default_value = (*emit, 1)
        p.inputs['Emission Strength'].default_value = strength
    return m

WAX = mat('Wax', (0.93, 0.86, 0.74), rough=0.45, sss=0.6)
WICK = mat('Wick', (0.03, 0.02, 0.015), rough=0.9)
FLAME = mat('Flame', (1, 0.5, 0.12), emit=(1.0, 0.42, 0.08), strength=9)
FLAME_CORE = mat('FlameCore', (1, 0.85, 0.5), emit=(1.0, 0.78, 0.4), strength=18)

def wax_for(h):
    # Wax that glows warm near the top, where the flame's light passes through it.
    m = mat(f'Wax{h}', (0.88, 0.74, 0.55), rough=0.45, sss=0.6)
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value = h / 2 - 0.16; mr.inputs['From Max'].default_value = h / 2
    mr.inputs['To Min'].default_value = 0.0; mr.inputs['To Max'].default_value = 1.0
    pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 2.5
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 1.6
    nt.links.new(tc.outputs['Object'], sep.inputs['Vector']); nt.links.new(sep.outputs['Z'], mr.inputs['Value'])
    nt.links.new(mr.outputs['Result'], pw.inputs[0]); nt.links.new(pw.outputs['Value'], mul.inputs[0])
    nt.links.new(mul.outputs['Value'], p.inputs['Emission Strength'])
    p.inputs['Emission Color'].default_value = (1.0, 0.55, 0.22, 1)
    return m

def teardrop(obj):
    # Narrow the top half of a sphere into a flame tip.
    for v in obj.data.vertices:
        if v.co.z > 0:
            k = 1 - 0.75 * v.co.z ** 1.3
            v.co.x *= k; v.co.y *= k
LEAF = mat('Holly', (0.02, 0.12, 0.04), rough=0.22, coat=0.6)
BERRY = mat('Berry', (0.55, 0.01, 0.02), rough=0.15, coat=1.0)
GOLD = mat('Gold', (1.0, 0.72, 0.32), rough=0.25, metal=1.0)

# Dark wood: a stretched noise for grain.
WOOD = bpy.data.materials.new('Wood'); WOOD.use_nodes = True
nt = WOOD.node_tree; p = nt.nodes['Principled BSDF']
tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
mp.inputs['Scale'].default_value = (1.0, 14.0, 1.0)
nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3.0; nz.inputs['Detail'].default_value = 8
ramp = nt.nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].color = (0.035, 0.016, 0.008, 1)
ramp.color_ramp.elements[1].color = (0.11, 0.05, 0.025, 1)
nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], p.inputs['Base Color'])
p.inputs['Roughness'].default_value = 0.35

def link(obj, m):
    obj.data.materials.append(m); return obj

def smooth(obj):
    for f in obj.data.polygons: f.use_smooth = True

# ---------- table ----------
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 2, 0))
link(bpy.context.object, WOOD)

# ---------- candles ----------
flames = []
def candle(x, y, h, r=0.11):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r, depth=h, location=(x, y, h / 2))
    c = bpy.context.object; link(c, wax_for(h)); smooth(c)
    bv = c.modifiers.new('bevel', 'BEVEL'); bv.width = 0.018; bv.segments = 5
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.004, depth=0.05, location=(x, y, h + 0.02))
    link(bpy.context.object, WICK)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=(x, y, h + 0.075))
    f = bpy.context.object; teardrop(f); f.scale = (0.017, 0.017, 0.05); link(f, FLAME); smooth(f)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=1, location=(x, y, h + 0.062))
    k = bpy.context.object; teardrop(k); k.scale = (0.008, 0.008, 0.024); link(k, FLAME_CORE); smooth(k)
    bpy.ops.object.light_add(type='POINT', location=(x, y, h + 0.09))
    L = bpy.context.object.data; L.energy = 9; L.color = (1.0, 0.58, 0.26); L.shadow_soft_size = 0.02
    flames.append((x, y, h))

candle(-0.13, 0.05, 0.50)
candle(0.14, -0.02, 0.36)

# ---------- holly ----------
def holly_leaf(length=0.2, width=0.085, spikes=4):
    bm = bmesh.new()
    pts = []
    n = spikes * 2
    for side in (1, -1):
        rng = range(n + 1) if side == 1 else range(n, -1, -1)
        for i in rng:
            t = i / n
            w = math.sin(math.pi * t) * width / 2
            if i % 2 == 1:
                w *= 1.35          # spike tips
            else:
                w *= 0.8           # the scallops between
            pts.append(Vector((t * length - length / 2, side * w, 0)))
    verts = [bm.verts.new(p) for p in pts]
    centre = bm.verts.new((0, 0, 0.004))
    for i in range(len(verts)):
        bm.faces.new((centre, verts[i], verts[(i + 1) % len(verts)]))
    me = bpy.data.meshes.new('leaf'); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new('leaf', me); bpy.context.collection.objects.link(ob)
    so = ob.modifiers.new('solid', 'SOLIDIFY'); so.thickness = 0.004
    link(ob, LEAF); smooth(ob)
    return ob

def sprig(x, y, angle, berries=3, leaves=3, z=0.006):
    for i in range(leaves):
        lf = holly_leaf(length=random.uniform(0.17, 0.23))
        a = angle + (i - (leaves - 1) / 2) * 0.9 + random.uniform(-0.15, 0.15)
        off = Vector((math.cos(a), math.sin(a), 0)) * 0.1
        lf.location = (x + off.x, y + off.y, z + 0.012 * i)
        lf.rotation_euler = (random.uniform(-0.25, 0.25), random.uniform(-0.2, 0.2), a)
    for j in range(berries):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=random.uniform(0.019, 0.024),
            location=(x + random.uniform(-0.03, 0.03), y + random.uniform(-0.03, 0.03), z + 0.03 + 0.01 * j))
        b = bpy.context.object; link(b, BERRY); smooth(b)

sprig(-0.36, -0.10, 0.4, berries=4)
sprig(0.38, -0.12, 2.7, berries=4)
sprig(0.00, -0.22, 1.5, berries=5, leaves=4)
sprig(-0.30, 0.28, -0.7)
sprig(0.36, 0.26, 3.7)
sprig(-0.52, 0.10, 0.1, berries=2, leaves=2)

# two small gold baubles for richness
for (x, y, r) in [(-0.18, -0.25, 0.04), (0.52, 0.06, 0.035)]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=r, location=(x, y, r))
    b = bpy.context.object; link(b, GOLD); smooth(b)

# ---------- soft golden lights far behind (they become bokeh) ----------
for i in range(70):
    x = random.uniform(-3.2, 3.2); y = random.uniform(4.5, 7.5); z = random.uniform(0.35, 3.4)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=random.uniform(0.02, 0.05), location=(x, y, z))
    s = bpy.context.object
    warm = random.choice([(1.0, 0.62, 0.22), (1.0, 0.48, 0.14), (1.0, 0.74, 0.36), (0.9, 0.3, 0.12)])
    m = mat(f'bokeh{i}', warm, emit=warm, strength=random.uniform(3, 7))
    link(s, m)

# ---------- world ----------
world = bpy.data.worlds.new('World'); scene.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.006, 0.003, 0.002, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0

# a faint warm fill so the leaves read
bpy.ops.object.light_add(type='AREA', location=(-1.2, -1.6, 1.4))
fill = bpy.context.object; fill.data.energy = 9; fill.data.size = 2.0; fill.data.color = (1.0, 0.75, 0.55)
fill.rotation_euler = (math.radians(60), 0, math.radians(-35))

# ---------- camera ----------
bpy.ops.object.camera_add(location=(0, -1.8, 0.62))
cam = bpy.context.object; scene.camera = cam
target = Vector((0.0, 0.05, 0.47))   # aimed above the candles, leaving the top of the picture for the headline
cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 52
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = (Vector((0, 0.0, 0.3)) - cam.location).length
cam.data.dof.aperture_fstop = 1.4

# ---------- render ----------
r = scene.render
r.resolution_x = r.resolution_y = SIZE
r.resolution_percentage = 100
r.image_settings.file_format = 'PNG'
r.filepath = OUT
scene.render.engine = 'CYCLES'
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    for kind in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI', 'METAL'):
        try:
            prefs.compute_device_type = kind; prefs.get_devices()
            if any(d.type != 'CPU' for d in prefs.devices):
                for d in prefs.devices: d.use = True
                scene.cycles.device = 'GPU'; print('GPU:', kind); break
        except Exception:
            pass
except Exception as e:
    print('no GPU prefs', e)
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Punchy' if 'AgX - Punchy' in [l.identifier for l in type(scene.view_settings).bl_rna.properties['look'].enum_items] else 'None'
# A soft glow round the flames and lights (compositor). If this Blender's compositor API differs, render without it.
try:
    ng = bpy.data.node_groups.new('Glow', 'CompositorNodeTree')
    ng.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    rl = ng.nodes.new('CompositorNodeRLayers'); out = ng.nodes.new('NodeGroupOutput')
    gl = ng.nodes.new('CompositorNodeGlare')
    for k, v in (('Type', 'Bloom'), ('Quality', 'High')):
        if k in gl.inputs: gl.inputs[k].default_value = v
    for k, v in (('Threshold', 0.9), ('Strength', 0.55), ('Size', 0.6)):
        if k in gl.inputs: gl.inputs[k].default_value = v
    ng.links.new(rl.outputs['Image'], gl.inputs['Image']); ng.links.new(gl.outputs['Image'], out.inputs[0])
    scene.compositing_node_group = ng
    print('GLOW on')
except Exception as e:
    print('GLOW off:', e)
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT.rsplit('.', 1)[0] + '.blend')
print('WROTE', OUT)
