# Blind Ant Cards: "Christmas With Love", round 2 (Sloppy Jo, Jewel Box treatment), built in Blender from its description.
# Description (written first, always true):
#   Two lit ivory candles lean towards each other on a dark wooden table, the taller one just behind as if
#   sheltering the smaller and sharing its light, among glossy holly leaves, red berries and a small gold bauble,
#   with soft golden lights blurred in the darkness above.
# Palette: ivory and amber-gold candlelight on deep oxblood-black, with deep holly green and ruby berries as the only accents.
# Focal point: the taller flame bending towards the smaller one.
# Run: blender -b --factory-startup -P scene.py -- <out.png> [samples] [size]
import bpy, bmesh, math, random, sys
from mathutils import Vector, Matrix

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = args[0] if args else '//christmas_with_love.png'
SAMPLES = int(args[1]) if len(args) > 1 else 64
SIZE = int(args[2]) if len(args) > 2 else 1080
random.seed(12)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ---------- palette ----------
IVORY = (0.95, 0.88, 0.75)
GOLDS = [(1.0, 0.70, 0.34), (1.0, 0.78, 0.46), (1.0, 0.64, 0.28)]   # the only bokeh hues: no pink
OXBLOOD_BLACK = (0.009, 0.0025, 0.002)
HOLLY = (0.025, 0.14, 0.05)
RUBY = (0.50, 0.012, 0.02)

# ---------- materials ----------
def mat(name, color, rough=0.5, metal=0.0, emit=None, strength=0.0, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if coat:
        p.inputs['Coat Weight'].default_value = coat
        p.inputs['Coat Roughness'].default_value = 0.05
    if emit:
        p.inputs['Emission Color'].default_value = (*emit, 1)
        p.inputs['Emission Strength'].default_value = strength
    return m

WICK = mat('Wick', (0.03, 0.02, 0.015), rough=0.9)
FLAME = mat('Flame', (1, 0.5, 0.12), emit=(1.0, 0.45, 0.10), strength=9)
FLAME_CORE = mat('FlameCore', (1, 0.85, 0.5), emit=(1.0, 0.80, 0.45), strength=18)
LEAF = mat('Holly', HOLLY, rough=0.18, coat=1.0)
BERRY = mat('Berry', RUBY, rough=0.12, coat=1.0)
GOLD = mat('Gold', (1.0, 0.76, 0.40), rough=0.14, metal=1.0)

def alabaster(name, h, glow, r=0.1, side_glow=0.0):
    # Luminous ivory wax: deep subsurface so light passes through it, and a warm inner glow near the top
    # that fades to ivory, never brown. glow sets how strongly this candle is lit from within.
    m = mat(name, IVORY, rough=0.38)
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Subsurface Weight'].default_value = 1.0
    p.inputs['Subsurface Radius'].default_value = (1.0, 0.7, 0.45)
    p.inputs['Subsurface Scale'].default_value = 0.05
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value = h - 0.20; mr.inputs['From Max'].default_value = h
    pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 2.2
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = glow
    nt.links.new(tc.outputs['Object'], sep.inputs['Vector']); nt.links.new(sep.outputs['Z'], mr.inputs['Value'])
    nt.links.new(mr.outputs['Result'], pw.inputs[0]); nt.links.new(pw.outputs['Value'], mul.inputs[0])
    total = mul.outputs['Value']
    if side_glow:
        # The shared light, stylised: the side facing the tall candle (local -X) glows warm, strongest high up.
        mx = nt.nodes.new('ShaderNodeMapRange')
        mx.inputs['From Min'].default_value = 0.2 * r; mx.inputs['From Max'].default_value = -r
        mz = nt.nodes.new('ShaderNodeMapRange')
        mz.inputs['From Min'].default_value = 0.3 * h; mz.inputs['From Max'].default_value = h
        nt.links.new(sep.outputs['X'], mx.inputs['Value']); nt.links.new(sep.outputs['Z'], mz.inputs['Value'])
        both = nt.nodes.new('ShaderNodeMath'); both.operation = 'MULTIPLY'
        nt.links.new(mx.outputs['Result'], both.inputs[0]); nt.links.new(mz.outputs['Result'], both.inputs[1])
        sg = nt.nodes.new('ShaderNodeMath'); sg.operation = 'MULTIPLY'; sg.inputs[1].default_value = side_glow
        nt.links.new(both.outputs['Value'], sg.inputs[0])
        add = nt.nodes.new('ShaderNodeMath'); add.operation = 'ADD'
        nt.links.new(total, add.inputs[0]); nt.links.new(sg.outputs['Value'], add.inputs[1])
        total = add.outputs['Value']
    nt.links.new(total, p.inputs['Emission Strength'])
    p.inputs['Emission Color'].default_value = (1.0, 0.80, 0.55, 1)   # cream-gold, not orange
    return m

# Dark wood with a hint of oxblood: a stretched noise for grain.
WOOD = bpy.data.materials.new('Wood'); WOOD.use_nodes = True
nt = WOOD.node_tree; p = nt.nodes['Principled BSDF']
tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
mp.inputs['Scale'].default_value = (1.0, 14.0, 1.0)
nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3.0; nz.inputs['Detail'].default_value = 8
ramp = nt.nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].color = (0.028, 0.010, 0.007, 1)
ramp.color_ramp.elements[1].color = (0.085, 0.032, 0.020, 1)
nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], p.inputs['Base Color'])
p.inputs['Roughness'].default_value = 0.42
p.inputs['Coat Weight'].default_value = 0.12
p.inputs['Coat Roughness'].default_value = 0.25

def link(obj, m):
    obj.data.materials.append(m); return obj

def smooth(obj):
    for f in obj.data.polygons: f.use_smooth = True

def teardrop(obj):
    # Narrow the top half of a sphere into a flame tip.
    for v in obj.data.vertices:
        if v.co.z > 0:
            k = 1 - 0.75 * v.co.z ** 1.3
            v.co.x *= k; v.co.y *= k

def bend(obj, amount):
    # Bend a flame sideways (towards +x for a positive amount), more at the tip: the flame leans into its partner.
    for v in obj.data.vertices:
        if v.co.z > -0.3:
            t = (v.co.z + 0.3) / 1.3
            v.co.x += amount * t * t

# ---------- table ----------
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0.6, 0))   # ends in the dark, so the far table doesn't haze
link(bpy.context.object, WOOD)

# ---------- candles ----------
def candle_mesh(r, h):
    # A pillar with a shallow pool in the top, built with its base at the origin (the bevel rounds the rim).
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=96, radius1=r, radius2=r, depth=h,
                          matrix=Matrix.Translation((0, 0, h / 2)))
    top = [f for f in bm.faces if f.normal.z > 0.9][0]
    bmesh.ops.inset_region(bm, faces=[top], thickness=0.022, depth=0.0)
    bmesh.ops.translate(bm, vec=(0, 0, -0.010), verts=list(top.verts))
    me = bpy.data.meshes.new('candle'); bm.to_mesh(me); bm.free()
    return me

def candle(name, base, h, r, tilt_deg, glow, flame_bend, light_w, flame_scale=1.0, side_glow=0.0):
    pivot = bpy.data.objects.new(name, None); bpy.context.collection.objects.link(pivot)
    c = bpy.data.objects.new(name + '_wax', candle_mesh(r, h)); bpy.context.collection.objects.link(c)
    c.parent = pivot; link(c, alabaster(name + '_wax', h, glow, r, side_glow)); smooth(c)
    bv = c.modifiers.new('bevel', 'BEVEL'); bv.width = 0.02; bv.segments = 8; bv.limit_method = 'ANGLE'
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.004, depth=0.045, location=(0, 0, h + 0.008))
    w = bpy.context.object; link(w, WICK); w.parent = pivot
    s = flame_scale
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1, location=(0, 0, h + 0.075 * s))
    f = bpy.context.object; teardrop(f); bend(f, flame_bend); f.scale = (0.018 * s, 0.018 * s, 0.052 * s)
    link(f, FLAME); smooth(f); f.parent = pivot
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=(0, 0, h + 0.062 * s))
    k = bpy.context.object; teardrop(k); bend(k, flame_bend * 0.8); k.scale = (0.008 * s, 0.008 * s, 0.025 * s)
    link(k, FLAME_CORE); smooth(k); k.parent = pivot
    bpy.ops.object.light_add(type='POINT', location=(0.012 * flame_bend * 4, 0, h + 0.085 * s))
    L = bpy.context.object; L.data.energy = light_w; L.data.color = (1.0, 0.64, 0.32); L.data.shadow_soft_size = 0.025
    L.parent = pivot
    # Lean the whole candle about its base. Sink it a little so the lifted edge of the base stays on the table.
    t = math.radians(tilt_deg)
    pivot.location = (base[0], base[1], -abs(math.sin(t)) * r)
    pivot.rotation_euler = (0, t, 0)
    return pivot

# The taller candle: further back, leaning right towards the small one, burning brighter,
# its flame bending towards the small one to share its light.
candle('Tall', (-0.13, 0.12), 0.54, 0.118, tilt_deg=7.5, glow=0.9, flame_bend=0.55, light_w=16, flame_scale=1.08)
# The smaller candle: in front, leaning gently back towards the tall one.
candle('Small', (0.17, -0.05), 0.34, 0.102, tilt_deg=-5.0, glow=0.9, flame_bend=-0.2, light_w=6, flame_scale=0.92, side_glow=2.2)

# The shared light is in the small candle's wax (side_glow): the side facing the tall one glows warm.

# ---------- holly: a lacquered crescent in front of the candles, wholly in frame ----------
def holly_leaf(length=0.2, width=0.085, spikes=4):
    bm = bmesh.new()
    pts = []
    n = spikes * 2
    for side in (1, -1):
        rng = range(n + 1) if side == 1 else range(n, -1, -1)
        for i in rng:
            t = i / n
            w = math.sin(math.pi * t) * width / 2
            w *= 1.35 if i % 2 == 1 else 0.8
            pts.append(Vector((t * length - length / 2, side * w, 0)))
    verts = [bm.verts.new(p) for p in pts]
    centre = bm.verts.new((0, 0, 0.006))     # a gentle ridge down the middle
    for i in range(len(verts)):
        bm.faces.new((centre, verts[i], verts[(i + 1) % len(verts)]))
    me = bpy.data.meshes.new('leaf'); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new('leaf', me); bpy.context.collection.objects.link(ob)
    so = ob.modifiers.new('solid', 'SOLIDIFY'); so.thickness = 0.004
    link(ob, LEAF); smooth(ob)
    return ob

def sprig(x, y, angle, berries=0, leaves=3):
    for i in range(leaves):
        lf = holly_leaf(length=random.uniform(0.18, 0.22), width=random.uniform(0.088, 0.1))
        a = angle + (i - (leaves - 1) / 2) * 0.75 + random.uniform(-0.08, 0.08)
        off = Vector((math.cos(a), math.sin(a), 0)) * 0.10
        lf.location = (x + off.x, y + off.y, 0.006 + 0.008 * i)
        lf.rotation_euler = (random.uniform(-0.10, 0.10), random.uniform(-0.10, 0.10), a)
    # Berries in a tight, deliberate cluster, sitting on the leaves.
    for j in range(berries):
        a = j / max(1, berries) * math.tau + 0.4
        rr = 0.0 if j == 0 else 0.026
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.021,
            location=(x + rr * math.cos(a), y + rr * math.sin(a), 0.03 + (0.014 if j == 0 else 0)))
        b = bpy.context.object; link(b, BERRY); smooth(b)

# Sprigs along an arc in front of the pair, from front-left to front-right.
cx, cy, R = 0.03, 0.04, 0.34
arc = [(-160, 0, 3), (-128, 3, 3), (-95, 0, 3), (-62, 4, 3), (-30, 0, 3)]
for deg, nb, nl in arc:
    a = math.radians(deg)
    x, y = cx + R * math.cos(a), cy + R * 0.62 * math.sin(a)
    sprig(x, y, a + math.pi / 2 + 0.3, berries=nb, leaves=nl)
# one berry cluster tucked behind, at the tall candle's left, to close the crescent
sprig(-0.30, 0.18, 0.2, berries=3, leaves=2)

# One small gold bauble, placed on purpose: front right, catching both flames.
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.038, location=(0.43, -0.24, 0.038))
b = bpy.context.object; link(b, GOLD); smooth(b)

# ---------- soft golden lights far behind, gathered in the top third behind the headline ----------
for i in range(80):
    x = random.uniform(-3.4, 3.4); y = random.uniform(5.0, 7.5)
    z = 1.2 + 2.6 * (random.random() ** 0.6)          # weighted upwards, thinning towards the flames
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=random.uniform(0.025, 0.055), location=(x, y, z))
    s = bpy.context.object
    g = random.choice(GOLDS)
    link(s, mat(f'bokeh{i}', g, emit=g, strength=random.uniform(2.5, 6)))

# ---------- world ----------
world = bpy.data.worlds.new('World'); scene.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (*OXBLOOD_BLACK, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0

# A warm rim from behind and above, to separate the candles from the darkness.
bpy.ops.object.light_add(type='AREA', location=(0.1, 0.7, 1.2))
rim = bpy.context.object; rim.data.energy = 10; rim.data.size = 0.6; rim.data.color = (1.0, 0.72, 0.45)
rim.rotation_euler = (Vector((0.0, 0.0, 0.4)) - rim.location).to_track_quat('-Z', 'Y').to_euler()
rim.visible_camera = False
# A faint, low warm fill from the front so the holly's gloss reads.
bpy.ops.object.light_add(type='AREA', location=(-0.6, -1.4, 0.5))
fill = bpy.context.object; fill.data.energy = 2; fill.data.size = 1.5; fill.data.color = (1.0, 0.75, 0.55)
fill.rotation_euler = (Vector((0.0, 0.0, 0.05)) - fill.location).to_track_quat('-Z', 'Y').to_euler()
fill.visible_camera = False

# ---------- camera ----------
bpy.ops.object.camera_add(location=(0, -1.9, 0.58))
cam = bpy.context.object; scene.camera = cam
target = Vector((0.0, 0.05, 0.46))   # aimed above the candles, leaving the top of the picture for the headline
cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 56
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = (Vector((0.03, 0.03, 0.3)) - cam.location).length
cam.data.dof.aperture_fstop = 1.6

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
    for k, v in (('Threshold', 1.1), ('Strength', 0.45), ('Size', 0.35)):
        if k in gl.inputs: gl.inputs[k].default_value = v
    ng.links.new(rl.outputs['Image'], gl.inputs['Image']); ng.links.new(gl.outputs['Image'], out.inputs[0])
    scene.compositing_node_group = ng
    print('GLOW on')
except Exception as e:
    print('GLOW off:', e)
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT.rsplit('.', 1)[0] + '.blend')
print('WROTE', OUT)
