# Blind Ant Cards: "Christmas With Love", round 2 (Sloppy Jo, Jewel Box treatment), built in Blender from its description.
# Description (written first, always true):
#   Two lit ivory candles lean towards each other on a dark wooden table, the taller one just behind as if
#   sheltering the smaller and sharing its light, among glossy holly leaves, red berries and a small gold bauble,
#   with soft golden lights blurred in the darkness above.
# Palette: ivory and amber-gold candlelight on deep oxblood-black, with deep holly green and ruby berries as the only accents.
# Focal point: the taller flame bending towards the smaller one.
# Run: blender -b --factory-startup -P scene.py -- <out.png> [samples] [size]
import bpy, bmesh, math, random, sys
from mathutils import Vector, Matrix, Euler

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
    floor = nt.nodes.new('ShaderNodeMath'); floor.operation = 'ADD'; floor.inputs[1].default_value = 0.08
    nt.links.new(mul.outputs['Value'], floor.inputs[0])   # a little inner warmth everywhere, so shaded wax never goes grey
    total = floor.outputs['Value']
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
nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac'])
sepw = nt.nodes.new('ShaderNodeSeparateXYZ'); geo = nt.nodes.new('ShaderNodeNewGeometry')
nt.links.new(geo.outputs['Position'], sepw.inputs['Vector'])
fade = nt.nodes.new('ShaderNodeMapRange')            # 1 near the candles, 0 far behind
fade.inputs['From Min'].default_value = 0.5; fade.inputs['From Max'].default_value = 2.6
fade.inputs['To Min'].default_value = 1.0; fade.inputs['To Max'].default_value = 0.35
nt.links.new(sepw.outputs['Y'], fade.inputs['Value'])
darken = nt.nodes.new('ShaderNodeMix'); darken.data_type = 'RGBA'; darken.blend_type = 'MULTIPLY'
darken.inputs['Factor'].default_value = 1.0
nt.links.new(ramp.outputs['Color'], darken.inputs['A'])
fcol = nt.nodes.new('ShaderNodeCombineXYZ')
for k in ('X', 'Y', 'Z'): nt.links.new(fade.outputs['Result'], fcol.inputs[k])
nt.links.new(fcol.outputs['Vector'], darken.inputs['B'])
nt.links.new(darken.outputs['Result'], p.inputs['Base Color'])
rough = nt.nodes.new('ShaderNodeMapRange')           # and rougher with distance, so it stops reflecting the far lights
rough.inputs['From Min'].default_value = 0.5; rough.inputs['From Max'].default_value = 2.2
rough.inputs['To Min'].default_value = 0.42; rough.inputs['To Max'].default_value = 0.95
nt.links.new(sepw.outputs['Y'], rough.inputs['Value']); nt.links.new(rough.outputs['Result'], p.inputs['Roughness'])
nt.links.new(fade.outputs['Result'], p.inputs['Coat Weight'])
# Far away, the table melts into the background (turns transparent) instead of ending in an edge or a dark band.
melt = nt.nodes.new('ShaderNodeMapRange')
melt.inputs['From Min'].default_value = 1.2; melt.inputs['From Max'].default_value = 2.6
nt.links.new(sepw.outputs['Y'], melt.inputs['Value'])
clear = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
wout = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
nt.links.new(melt.outputs['Result'], mix.inputs['Fac'])
nt.links.new(p.outputs['BSDF'], mix.inputs[1]); nt.links.new(clear.outputs[0], mix.inputs[2])
nt.links.new(mix.outputs[0], wout.inputs['Surface'])
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
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 4, 0))   # fades to black with distance (see Wood), so it has no visible edge
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
candle('Small', (0.19, -0.05), 0.34, 0.102, tilt_deg=-10.0, glow=0.9, flame_bend=-0.2, light_w=6, flame_scale=0.92, side_glow=2.2)

# The shared light is in the small candle's wax (side_glow): the side facing the tall one glows warm.


# The shared light, made visible: a soft warm haze in the air from the tall flame to the small one.
# It's a camera-only card (it lights nothing), shaped as a soft ellipse along the line between the flames.
def shared_glow():
    a = Vector((-0.06, 0.12, 0.60)); b = Vector((0.13, -0.05, 0.40))
    mid = (a + b) / 2
    bpy.ops.mesh.primitive_plane_add(size=1, location=mid)
    g = bpy.context.object; g.name = 'SharedGlow'
    d = b - a
    span = math.hypot(d.x, d.z)
    g.scale = (span * 1.05, span * 0.45, 1)
    g.rotation_euler = (math.radians(90), -math.atan2(d.z, d.x), 0)   # stand it up facing the camera, along the line
    m = bpy.data.materials.new('SharedGlow'); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL': nt.nodes.remove(n)
    out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    tc = nt.nodes.new('ShaderNodeTexCoord')
    grad = nt.nodes.new('ShaderNodeTexGradient'); grad.gradient_type = 'SPHERICAL'
    sc = nt.nodes.new('ShaderNodeMapping'); sc.inputs['Scale'].default_value = (2.0, 2.0, 2.0)
    nt.links.new(tc.outputs['Object'], sc.inputs['Vector']); nt.links.new(sc.outputs['Vector'], grad.inputs['Vector'])
    pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 2.0
    nt.links.new(grad.outputs['Fac'], pw.inputs[0])
    st = nt.nodes.new('ShaderNodeMath'); st.operation = 'MULTIPLY'; st.inputs[1].default_value = GLOW_STRENGTH
    nt.links.new(pw.outputs['Value'], st.inputs[0])
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (1.0, 0.66, 0.32, 1)
    nt.links.new(st.outputs['Value'], em.inputs['Strength'])
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    add = nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(tr.outputs[0], add.inputs[0]); nt.links.new(em.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], out.inputs['Surface'])
    g.data.materials.append(m)
    for attr in ('visible_diffuse', 'visible_glossy', 'visible_transmission', 'visible_volume_scatter', 'visible_shadow'):
        setattr(g, attr, False)

GLOW_STRENGTH = 0.7
shared_glow()

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
    for v in bm.verts:   # fold along the midrib and arch along the length, like a real holly leaf
        v.co.z += 0.22 * abs(v.co.y) - 0.9 * (v.co.x / length) ** 2 * length * 0.25
    me = bpy.data.meshes.new('leaf'); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new('leaf', me); bpy.context.collection.objects.link(ob)
    so = ob.modifiers.new('solid', 'SOLIDIFY'); so.thickness = 0.004
    link(ob, LEAF); smooth(ob)
    return ob

def sprig(x, y, angle, berries=0, leaves=3):
    for i in range(leaves):
        L = random.uniform(0.13, 0.24)
        lf = holly_leaf(length=L, width=L * random.uniform(0.42, 0.5))
        a = angle + (i - (leaves - 1) / 2) * 0.75 + random.uniform(-0.08, 0.08)
        off = Vector((math.cos(a), math.sin(a), 0)) * (L * 0.5)
        lf.location = (x + off.x, y + off.y, 0.006 + 0.008 * i)
        lf.rotation_euler = (random.uniform(-0.10, 0.10), random.uniform(-0.10, 0.10), a)
    # Berries in a tight, deliberate cluster, sitting on the leaves.
    for j in range(berries):
        a = j / max(1, berries) * math.tau + 0.4
        rr = 0.0 if j == 0 else 0.036
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=random.uniform(0.018, 0.023),
            location=(x + rr * math.cos(a), y + rr * math.sin(a), 0.03 + (0.014 if j == 0 else 0)))
        b = bpy.context.object; link(b, BERRY); smooth(b)

# Sprigs placed by hand around the pair, clear of both candles' bases (tall: centre -0.13, 0.12, radius 0.12;
# small: centre 0.19, -0.05, radius 0.10). Leaves point away from the candles. Three berry clusters, no more.
# One continuous garland hugging the front of both bases, leaves running along it. Three berry clusters.
garland = [  # x, y, direction the leaves run, berries
    (-0.33, 0.06, -1.9, 0), (-0.27, -0.05, -0.9, 3), (-0.15, -0.11, -0.3, 0), (-0.03, -0.13, 0.0, 0),
    (0.04, -0.15, 0.1, 4), (0.13, -0.18, 0.0, 0), (0.24, -0.18, 0.3, 0), (0.33, -0.10, 0.9, 3), (0.37, 0.02, 1.6, 0),
]
for x, y, angle, nb in garland:
    sprig(x, y, angle, berries=nb, leaves=2)
    sprig(x, y, angle + math.pi, berries=0, leaves=1)

# One small gold bauble, placed on purpose: front right, catching both flames. It has a cap and a
# hanging loop, so it reads as a Christmas bauble rather than a polished ball.
BX, BY, BR = 0.47, -0.17, 0.038
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=BR, location=(BX, BY, BR))
b = bpy.context.object; link(b, GOLD); smooth(b)
CAP = mat('Cap', (0.75, 0.62, 0.42), rough=0.3, metal=1.0)      # paler, brushed: a different metal from the bauble
# Lying on its side, the cap points sideways (towards the right and back, away from the candles).
cap_dir = Vector((0.75, 0.45, 0.25)).normalized()
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=BR * 0.32, depth=BR * 0.28,
                                    location=Vector((BX, BY, BR)) + cap_dir * BR * 1.02)
c = bpy.context.object; c.rotation_euler = cap_dir.to_track_quat('Z', 'Y').to_euler(); link(c, CAP); smooth(c)
bv = c.modifiers.new('bevel', 'BEVEL'); bv.width = 0.002; bv.segments = 3
bpy.ops.mesh.primitive_torus_add(major_radius=BR * 0.22, minor_radius=BR * 0.045,
                                 location=Vector((BX, BY, BR)) + cap_dir * BR * 1.32)
t = bpy.context.object
t.rotation_euler = (cap_dir.to_track_quat('Z', 'Y') @ Euler((math.radians(90), 0, 0)).to_quaternion()).to_euler()
link(t, CAP); smooth(t)

# ---------- soft golden lights far behind, gathered in the top third behind the headline ----------
N_BOKEH = 80
for i in range(N_BOKEH):
    x = -3.4 + 6.8 * (i + random.random()) / N_BOKEH; y = random.uniform(3.8, 8.5)   # evenly spread left to right
    z = 0.2 + 2.3 * (random.random() ** 0.6)          # weighted upwards, thinning towards the flames
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=random.uniform(0.015, 0.06) * (2.2 if random.random() < 0.12 else 1.0), location=(x, y, z))
    s = bpy.context.object
    g = random.choice(GOLDS)
    link(s, mat(f'bokeh{i}', g, emit=g, strength=random.uniform(1.2, 7) * (0.35 if s.dimensions.x > 0.13 else 1.0)))

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
bpy.ops.object.camera_add(location=(0, -1.85, 0.80))
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
