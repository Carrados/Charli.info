import bpy, bmesh, math, random, sys, os, time
import numpy as np
from mathutils import Vector

ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
MODE = ARGS[0] if ARGS else 'preview'          # preview | final
OUT = ARGS[1] if len(ARGS) > 1 else r'C:\Temp\blind_ant.png'
SUN_ROT = float(os.environ.get('SUN_ROT', '4.05'))
SUN_EL = float(os.environ.get('SUN_EL', '6.5'))
EXPOSURE = float(os.environ.get('EXPOSURE', '-3.2'))
HAZE = float(os.environ.get('HAZE', '0.00035'))
PLAIN_Z = -90.0
T0 = time.time()
def log(*a): print('[%.0fs]' % (time.time() - T0), *a, flush=True)

random.seed(7)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ---------------------------------------------------------------- noise
_tab = np.random.default_rng(11).random((512, 512))
def vnoise(x, y, off=0):
    x = np.asarray(x, float) + off * 37.13
    y = np.asarray(y, float) + off * 17.71
    xi = np.floor(x).astype(np.int64); yi = np.floor(y).astype(np.int64)
    xf = x - xi; yf = y - yi
    u = xf * xf * (3 - 2 * xf); v = yf * yf * (3 - 2 * yf)
    a = _tab[xi & 511, yi & 511]; b = _tab[(xi + 1) & 511, yi & 511]
    c = _tab[xi & 511, (yi + 1) & 511]; d = _tab[(xi + 1) & 511, (yi + 1) & 511]
    return (a * (1 - u) + b * u) * (1 - v) + (c * (1 - u) + d * u) * v

def fbm(x, y, octs=5, seed=0, ridged=False, gain=0.5):
    tot = 0.0; amp = 1.0; norm = 0.0
    ca, sa = math.cos(0.7), math.sin(0.7)
    x = np.asarray(x, float); y = np.asarray(y, float)
    for o in range(octs):
        n = vnoise(x, y, seed + o * 3)
        if ridged:
            n = 1 - np.abs(2 * n - 1); n = n * n
        tot = tot + amp * n; norm += amp
        x, y = (x * ca - y * sa) * 2.0, (x * sa + y * ca) * 2.0
        amp *= gain
    return tot / norm

def smooth(a, b, t):
    t = np.clip((np.asarray(t, float) - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)

# ---------------------------------------------------------------- letters
FONT = r'C:\Windows\Fonts\ariblk.ttf'
font = bpy.data.fonts.load(FONT)
CAP = 62.0           # letter height in metres
DEPTH = 7.0
TRACK = 6.0
WORD_GAP = 80.0

def make_letter_mesh(ch):
    cu = bpy.data.curves.new('c' + ch, 'FONT')
    cu.body = ch; cu.size = 90; cu.font = font
    cu.extrude = 0.5; cu.bevel_depth = 0.0
    ob = bpy.data.objects.new('t' + ch, cu)
    scene.collection.objects.link(ob)
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    bpy.data.objects.remove(ob); bpy.data.curves.remove(cu)
    n = len(me.vertices)
    co = np.empty(n * 3); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    xmin, xmax = co[:, 0].min(), co[:, 0].max()
    ymin, ymax = co[:, 1].min(), co[:, 1].max()
    zmin, zmax = co[:, 2].min(), co[:, 2].max()
    sc = CAP / (ymax - ymin)
    w = (xmax - xmin) * sc
    zc = 0.5 * (zmin + zmax)
    # depth: stretch extrusion to DEPTH
    zsc = DEPTH / max(zmax - zmin, 1e-6)
    X = (co[:, 0] - 0.5 * (xmin + xmax)) * sc
    Y = (co[:, 2] - zc) * zsc * -1.0           # world y (facing -y after rotation)
    Z = (co[:, 1] - ymin) * sc                 # world z, bottom at 0
    new = np.stack([X, Y, Z], 1)
    me.vertices.foreach_set('co', new.ravel()); me.update()
    me.polygons.foreach_set('use_smooth', [False] * len(me.polygons))
    # rotation flips winding: flip normals
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    return me, w

TEXT = ['B', 'L', 'I', 'N', 'D', None, 'A', 'N', 'T']
letters = []
for ch in TEXT:
    if ch is None: letters.append((None, WORD_GAP, None)); continue
    me, w = make_letter_mesh(ch)
    letters.append((ch, w, me))
rel = []; xx = 0.0; gap_rel = None
for ch, w, me in letters:
    if ch is None:
        gap_rel = xx - TRACK + WORD_GAP / 2; xx += WORD_GAP - TRACK; continue
    rel.append((ch, xx + w / 2, w, me)); xx += w + TRACK
total = xx - TRACK
SIGN_CX = 410.0
shift = SIGN_CX - total / 2
layout = [(ch, cx + shift, w, me) for ch, cx, w, me in rel]
gap_x = gap_rel + shift
log('sign span', SIGN_CX - total / 2, SIGN_CX + total / 2, 'gap at', gap_x)
Y0 = 950.0      # sign line

# ---------------------------------------------------------------- terrain
H_HILL = 320.0
def lowfreq(x, y):
    wx = smooth(-330, 120, x)
    prof = H_HILL * smooth(640, 1500, y) + 0.09 * np.clip(y - 1500, 0, 3000)
    plain = PLAIN_Z + 3.0 * fbm(x / 800, y / 800, 3, seed=4)
    broad = (fbm(x / 420, y / 560, 5, seed=1) - 0.5) * 105 * smooth(520, 1500, y) * wx
    swale = -9.0 * np.exp(-((x - gap_x) / 55.0) ** 2) * smooth(700, 1050, y) * (1 - smooth(1100, 1500, y))
    r2 = ((x - 380) ** 2 + (y + 430) ** 2) / 330.0 ** 2
    knoll = 230.0 * np.exp(-r2 ** 1.2)
    ridge = 62.0 * np.exp(-((y - 390) / 135.0) ** 2) * smooth(-60, 220, x) * (1 + 0.3 * (fbm(x / 160, y / 160, 3, seed=40) - 0.5))
    mtn = 700.0 * smooth(3300, 6800, y) * (0.2 + 0.9 * fbm(x / 1900, y / 1900, 5, seed=5, ridged=True))
    return prof * wx + broad + swale + plain + knoll + mtn + ridge

def detail(x, y):
    wx = smooth(-330, 120, x)
    face = smooth(560, 1500, y) * wx
    gull = (fbm(x / 70, y / 340, 5, seed=2, ridged=True) - 0.4) * 34
    fine = (fbm(x / 20, y / 20, 4, seed=3) - 0.5) * 4.0
    micro = (fbm(x / 5, y / 5, 3, seed=6) - 0.5) * 0.9
    knoll_d = (fbm(x / 60, y / 60, 4, seed=8) - 0.5) * 8 * smooth(-900, -300, y) * (1 - smooth(-100, 500, y))
    ridge_d = (fbm(x / 25, y / 25, 4, seed=41) - 0.5) * 7 * np.exp(-((y - 330) / 170.0) ** 2)
    return face * (gull + fine) + micro + knoll_d + ridge_d

def height(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    h = lowfreq(x, y) + detail(x, y)
    s = lowfreq(x, np.full(x.shape, Y0))
    w = 1 - smooth(14, 46, np.abs(y - Y0))
    w = w * smooth(-250, 60, x)
    return h * (1 - w) + s * w

def mesh_from_arrays(name, verts, faces):
    verts = np.ascontiguousarray(verts, dtype=np.float32); faces = np.ascontiguousarray(faces, dtype=np.int32)
    k = faces.shape[1]
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.ravel())
    me.loops.add(len(faces) * k); me.polygons.add(len(faces))
    me.loops.foreach_set('vertex_index', faces.ravel())
    me.polygons.foreach_set('loop_start', np.arange(len(faces), dtype=np.int32) * k)
    me.update(calc_edges=True)
    return me

def grid_mesh(name, x0, x1, y0, y1, step, sink_rects=()):
    xs = np.arange(x0, x1 + 1e-6, step); ys = np.arange(y0, y1 + 1e-6, step)
    X, Y = np.meshgrid(xs, ys)
    Z = height(X, Y)
    for (a, b, c, d) in sink_rects:
        inside = (X > a) & (X < b) & (Y > c) & (Y < d)
        Z = np.where(inside, Z - 9.0, Z)
    nx, ny = len(xs), len(ys)
    verts = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    idx = np.arange(nx * ny).reshape(ny, nx)
    a = idx[:-1, :-1].ravel(); b = idx[:-1, 1:].ravel(); c = idx[1:, 1:].ravel(); d = idx[1:, :-1].ravel()
    me = mesh_from_arrays(name, verts, np.stack([a, b, c, d], 1))
    try: me.shade_smooth()
    except Exception: pass
    ob = bpy.data.objects.new(name, me)
    scene.collection.objects.link(ob)
    return ob

PATCH_HILL = (-400, 1120, 600, 1680)
PATCH_FG = (-120, 920, -440, 520)
log('terrain...')
terrains = [
    grid_mesh('coarse', -9000, 6200, -1200, 12000, 40.0, [PATCH_HILL, PATCH_FG]),
    grid_mesh('hill', PATCH_HILL[0], PATCH_HILL[1], PATCH_HILL[2], PATCH_HILL[3], 2.5),
    grid_mesh('fg', PATCH_FG[0], PATCH_FG[1], PATCH_FG[2], PATCH_FG[3], 2.5),
]
log('terrain done')
for t in terrains:
    co = np.empty(len(t.data.vertices) * 3); t.data.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    print('TER', t.name, len(co), co.min(0), co.max(0))
print('H', height(np.array([400., 400., 400., 400., 400.]), np.array([-250., 300., 700., 950., 1300.])))


# ---------------------------------------------------------------- materials
def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL': nt.nodes.remove(n)
    out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    return m, nt, out

def N(nt, typ, **kw):
    n = nt.nodes.new(typ)
    for k, v in kw.items(): setattr(n, k, v)
    return n

def L(nt, a, b, c=None):
    if c is None: nt.links.new(a, b)
    else: nt.links.new(a.outputs[b], c)

def ramp(nt, stops):
    r = N(nt, 'ShaderNodeValToRGB')
    r.color_ramp.elements[0].position = stops[0][0]; r.color_ramp.elements[0].color = stops[0][1]
    r.color_ramp.elements[1].position = stops[-1][0]; r.color_ramp.elements[1].color = stops[-1][1]
    for p, c in stops[1:-1]:
        e = r.color_ramp.elements.new(p); e.color = c
    return r

def noise(nt, scale, detail=5, rough=0.55, vec=None):
    n = N(nt, 'ShaderNodeTexNoise')
    n.inputs['Scale'].default_value = scale; n.inputs['Detail'].default_value = detail
    n.inputs['Roughness'].default_value = rough
    if vec is not None: nt.links.new(vec, n.inputs['Vector'])
    return n

def mathn(nt, op, a=None, b=None, clamp=False):
    m = N(nt, 'ShaderNodeMath', operation=op); m.use_clamp = clamp
    if a is not None:
        if isinstance(a, (int, float)): m.inputs[0].default_value = a
        else: nt.links.new(a, m.inputs[0])
    if b is not None:
        if isinstance(b, (int, float)): m.inputs[1].default_value = b
        else: nt.links.new(b, m.inputs[1])
    return m

def mixc(nt, fac, a, b):
    m = N(nt, 'ShaderNodeMix', data_type='RGBA')
    if isinstance(fac, (int, float)): m.inputs[0].default_value = fac
    else: nt.links.new(fac, m.inputs[0])
    for i, v in ((6, a), (7, b)):
        if isinstance(v, tuple): m.inputs[i].default_value = v
        else: nt.links.new(v, m.inputs[i])
    return m.outputs[2]

def principled(nt, color, rough=0.8, metal=0.0, spec=0.35):
    p = N(nt, 'ShaderNodeBsdfPrincipled')
    if isinstance(color, tuple): p.inputs['Base Color'].default_value = color
    else: nt.links.new(color, p.inputs['Base Color'])
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    for k in ('Specular IOR Level', 'Specular'):
        if k in p.inputs: p.inputs[k].default_value = spec; break
    return p

# --- terrain material
m_ter, nt, out = new_mat('terrain')
geo = N(nt, 'ShaderNodeNewGeometry')
P = geo.outputs['Position']
sep = N(nt, 'ShaderNodeSeparateXYZ'); L(nt, P, sep.inputs[0])
n_big = noise(nt, 0.0035, 6, 0.6, P)
n_mid = noise(nt, 0.03, 6, 0.6, P)
n_fine = noise(nt, 0.9, 5, 0.6, P)
n_micro = noise(nt, 7.0, 3, 0.5, P)
mixv = mathn(nt, 'ADD', mathn(nt, 'MULTIPLY', n_big.outputs['Fac'], 0.45).outputs[0],
             mathn(nt, 'ADD', mathn(nt, 'MULTIPLY', n_mid.outputs['Fac'], 0.35).outputs[0],
                   mathn(nt, 'MULTIPLY', n_fine.outputs['Fac'], 0.25).outputs[0]).outputs[0])
hill = ramp(nt, [(0.30, (0.030, 0.026, 0.012, 1)), (0.46, (0.090, 0.075, 0.032, 1)),
                 (0.58, (0.190, 0.150, 0.062, 1)), (0.72, (0.330, 0.265, 0.110, 1)),
                 (0.90, (0.470, 0.400, 0.195, 1))])
L(nt, mixv.outputs[0], hill.inputs['Fac'])
sage_mask = ramp(nt, [(0.56, (0, 0, 0, 1)), (0.68, (1, 1, 1, 1))])
L(nt, n_mid.outputs['Fac'], sage_mask.inputs['Fac'])
sage = mixc(nt, sage_mask.outputs['Color'], hill.outputs['Color'], (0.045, 0.050, 0.020, 1))
bare_mask = ramp(nt, [(0.70, (0, 0, 0, 1)), (0.80, (1, 1, 1, 1))])
n_bare = noise(nt, 0.012, 5, 0.6, P)
L(nt, n_bare.outputs['Fac'], bare_mask.inputs['Fac'])
hillcol = mixc(nt, bare_mask.outputs['Color'], sage, (0.240, 0.165, 0.105, 1))
# plain / city ground
fx = mathn(nt, 'FRACT', mathn(nt, 'DIVIDE', sep.outputs['X'], 72.0).outputs[0])
fy = mathn(nt, 'FRACT', mathn(nt, 'DIVIDE', sep.outputs['Y'], 72.0).outputs[0])
road = mathn(nt, 'MAXIMUM', mathn(nt, 'LESS_THAN', fx.outputs[0], 0.07).outputs[0],
             mathn(nt, 'LESS_THAN', fy.outputs[0], 0.07).outputs[0])
n_city = noise(nt, 0.004, 4, 0.5, P)
cityground = mixc(nt, n_city.outputs['Fac'], (0.22, 0.20, 0.17, 1), (0.13, 0.15, 0.09, 1))
cityground = mixc(nt, road.outputs[0], cityground, (0.075, 0.075, 0.08, 1))
zc = mathn(nt, 'SUBTRACT', sep.outputs['Z'], PLAIN_Z + 6.0)
zc2 = mathn(nt, 'DIVIDE', zc.outputs[0], 14.0, True)
xr = mathn(nt, 'DIVIDE', mathn(nt, 'ADD', sep.outputs['X'], 150.0).outputs[0], 100.0, True)
fmask = mathn(nt, 'MAXIMUM', zc2.outputs[0], xr.outputs[0])
colfinal = mixc(nt, fmask.outputs[0], cityground, hillcol)
bump = N(nt, 'ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.55; bump.inputs['Distance'].default_value = 0.5
L(nt, n_micro.outputs['Fac'], bump.inputs['Height'])
pr = principled(nt, colfinal, 0.92)
L(nt, bump.outputs['Normal'], pr.inputs['Normal'])
L(nt, pr.outputs['BSDF'], out.inputs['Surface'])
for t in terrains: t.data.materials.append(m_ter)

# --- vertex-colour materials (bushes, city)
def attr_mat(name, rough, metal=0.0, spec=0.4):
    m, nt, out = new_mat(name)
    a = N(nt, 'ShaderNodeAttribute'); a.attribute_name = 'tint'; a.attribute_type = 'GEOMETRY'
    p = principled(nt, a.outputs['Color'], rough, metal, spec)
    L(nt, p.outputs['BSDF'], out.inputs['Surface'])
    return m
m_bush = attr_mat('bush', 1.0, 0.0, 0.05)
m_city = attr_mat('city', 0.38, 0.0, 0.7)

m_white, nt, out = new_mat('letter_white')
geo = N(nt, 'ShaderNodeNewGeometry')
tc = N(nt, 'ShaderNodeTexCoord')
sepo = N(nt, 'ShaderNodeSeparateXYZ'); L(nt, tc.outputs['Object'], sepo.inputs[0])
dirt_h = mathn(nt, 'DIVIDE', sepo.outputs['Z'], CAP, True)
dirt = mathn(nt, 'SUBTRACT', 1.0, dirt_h.outputs[0])
dirt_p = mathn(nt, 'POWER', dirt.outputs[0], 3.0)
n_streak = noise(nt, 1.0, 4, 0.6)
vec_s = N(nt, 'ShaderNodeCombineXYZ')
L(nt, mathn(nt, 'MULTIPLY', sepo.outputs['X'], 0.5).outputs[0], vec_s.inputs['X'])
L(nt, mathn(nt, 'MULTIPLY', sepo.outputs['Z'], 0.05).outputs[0], vec_s.inputs['Z'])
L(nt, vec_s.outputs[0], n_streak.inputs['Vector'])
streak = mathn(nt, 'MULTIPLY', n_streak.outputs['Fac'], dirt_p.outputs[0])
wcol = mixc(nt, mathn(nt, 'MULTIPLY', streak.outputs[0], 1.6, True).outputs[0], (0.86, 0.85, 0.80, 1), (0.30, 0.24, 0.17, 1))
pr = principled(nt, wcol, 0.5, 0.0, 0.5)
L(nt, pr.outputs['BSDF'], out.inputs['Surface'])

m_steel, nt, out = new_mat('steel')
pr = principled(nt, (0.05, 0.05, 0.055, 1), 0.45, 0.9, 0.5)
L(nt, pr.outputs['BSDF'], out.inputs['Surface'])
m_conc, nt, out = new_mat('concrete')
pr = principled(nt, (0.45, 0.43, 0.40, 1), 0.9)
L(nt, pr.outputs['BSDF'], out.inputs['Surface'])
m_dust, nt, out = new_mat('dust')
geo = N(nt, 'ShaderNodeNewGeometry')
nn = noise(nt, 0.8, 4, 0.5, geo.outputs['Position'])
dc = mixc(nt, nn.outputs['Fac'], (0.30, 0.235, 0.165, 1), (0.44, 0.36, 0.26, 1))
pr = principled(nt, dc, 0.95)
L(nt, pr.outputs['BSDF'], out.inputs['Surface'])
m_red, nt, out = new_mat('beacon')
em = N(nt, 'ShaderNodeEmission'); em.inputs['Color'].default_value = (1.0, 0.05, 0.03, 1); em.inputs['Strength'].default_value = 60
L(nt, em.outputs['Emission'], out.inputs['Surface'])
m_mastw, nt, out = new_mat('mast_white')
pr = principled(nt, (0.75, 0.74, 0.70, 1), 0.5)
L(nt, pr.outputs['BSDF'], out.inputs['Surface'])
m_mastr, nt, out = new_mat('mast_red')
pr = principled(nt, (0.55, 0.06, 0.04, 1), 0.5)
L(nt, pr.outputs['BSDF'], out.inputs['Surface'])

# ---------------------------------------------------------------- sign
log('sign...')
sign_objs = []
curve_all = []   # curve splines for steel
def add_poly(cu, pts):
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts): p.co = (c[0], c[1], c[2], 1)

steel = bpy.data.curves.new('steel', 'CURVE'); steel.dimensions = '3D'
steel.bevel_depth = 0.55; steel.bevel_resolution = 1; steel.use_fill_caps = True
foot_boxes = []
for ch, cx, w, me in layout:
    # ground under the letter: bench height
    xs = np.linspace(cx - w / 2, cx + w / 2, 9)
    bench = float(np.max(lowfreq(xs, np.full(9, Y0)))) if False else float(np.max(height(xs, np.full(9, Y0))))
    zb = bench + 9.0
    ob = bpy.data.objects.new('letter_' + ch, me)
    ob.location = (cx, Y0, zb)
    if ch == 'N': ob.rotation_euler = (0, math.radians(1.8 if cx < SIGN_CX else -1.4), 0)
    scene.collection.objects.link(ob); ob.data.materials.append(m_white)
    sign_objs.append(ob)
    # posts: rows front/back, 3-4 columns
    ncol = 4 if w > 55 else 3
    fr = np.linspace(0.12, 0.88, ncol)
    post_top = {}
    for j, yy in enumerate((Y0 - DEPTH * 0.35, Y0 + DEPTH * 0.35)):
        for i, f in enumerate(fr):
            px = cx - w / 2 + f * w
            gz = float(height(np.array([px]), np.array([yy]))[0]) - 1.2
            add_poly(steel, [(px, yy, gz), (px, yy, zb + 2)])
            post_top[(i, j)] = (px, yy, gz)
            foot_boxes.append((px, yy, gz + 0.4))
    # cross braces
    for j in (0, 1):
        for i in range(ncol - 1):
            a = post_top[(i, j)]; b = post_top[(i + 1, j)]
            za = zb - 0.5; zbm = a[2] + (zb - a[2]) * 0.35
            add_poly(steel, [(a[0], a[1], zbm), (b[0], b[1], za)])
            add_poly(steel, [(b[0], b[1], (b[2] + (zb - b[2]) * 0.35)), (a[0], a[1], za)])
    for i in range(ncol):
        a = post_top[(i, 0)]; b = post_top[(i, 1)]
        add_poly(steel, [(a[0], a[1], zb + 1), (b[0], b[1], zb + 1)])
    # rear diagonal braces up the hill
    for f in (0.25, 0.75):
        px = cx - w / 2 + f * w
        gz = float(height(np.array([px]), np.array([Y0 + 70.0]))[0])
        add_poly(steel, [(px, Y0 + DEPTH * 0.4, zb + CAP * 0.55), (px, Y0 + 70.0, gz)])
steel_ob = bpy.data.objects.new('steel', steel); scene.collection.objects.link(steel_ob)
steel_ob.data.materials.append(m_steel)

# footings
bm = bmesh.new()
for (px, py, pz) in foot_boxes:
    bmesh.ops.create_cube(bm, size=1.0, matrix=__import__('mathutils').Matrix.LocRotScale((px, py, pz), None, (3.2, 3.2, 1.6)))
me = bpy.data.meshes.new('footings'); bm.to_mesh(me); bm.free()
fo = bpy.data.objects.new('footings', me); scene.collection.objects.link(fo); me.materials.append(m_conc)

# ---------------------------------------------------------------- track ribbons
def ribbon(name, pts, width, lift=0.4):
    pts = np.array(pts, float)
    d = np.gradient(pts, axis=0); d /= np.linalg.norm(d, axis=1)[:, None] + 1e-9
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    L_ = pts + nrm * width / 2; R_ = pts - nrm * width / 2
    zl = height(L_[:, 0], L_[:, 1]) + lift; zr = height(R_[:, 0], R_[:, 1]) + lift
    n = len(pts)
    verts = np.zeros((2 * n, 3))
    verts[0::2] = np.column_stack([L_, zl]); verts[1::2] = np.column_stack([R_, zr])
    faces = [(2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2) for i in range(n - 1)]
    me = bpy.data.meshes.new(name); me.from_pydata(verts.tolist(), [], faces); me.update()
    me.materials.append(m_dust)
    ob = bpy.data.objects.new(name, me); scene.collection.objects.link(ob)
    return ob
ys_ = np.arange(470, 1500, 3.0)
xs_ = gap_x + 85 * np.sin((ys_ - 330) / 190.0) * (1 - 0.35 * smooth(900, 1500, ys_)) + 25 * np.sin(ys_ / 47.0)
xs_ = xs_ + (gap_x - (gap_x + 85 * np.sin((Y0 - 330) / 190.0) * (1 - 0.35 * smooth(900, 1500, Y0)) + 25 * np.sin(Y0 / 47.0))) * np.exp(-((ys_ - Y0) / 120.0) ** 2)
ribbon('track', list(zip(xs_, ys_)), 5.0)
bx = np.arange(-120, 900, 3.0)
ribbon('bench_track', list(zip(bx, np.full_like(bx, Y0 - 12.0) + 3 * np.sin(bx / 90.0))), 4.0)
# a small side track climbing to the mast
ys2 = np.arange(1380, 1520, 2.0)
ribbon('mast_track', list(zip(450 + 0 * ys2 - (ys2 - 1380) * 0.3, ys2)), 3.5)

# ---------------------------------------------------------------- masts
def lattice(cx, cy, hgt, base_w, top_w, levels, thick=0.35):
    cu = bpy.data.curves.new('mast', 'CURVE'); cu.dimensions = '3D'
    cu.bevel_depth = thick; cu.bevel_resolution = 1
    gz = float(height(np.array([cx]), np.array([cy]))[0]) - 1.0
    def ring(t):
        r = base_w + (top_w - base_w) * t
        return [(cx + r * math.cos(a), cy + r * math.sin(a), gz + hgt * t) for a in (math.pi / 2, math.pi / 2 + 2.094, math.pi / 2 + 4.189)]
    prev = ring(0)
    for k in range(1, levels + 1):
        t = k / levels
        cur = ring(t)
        for i in range(3):
            add_poly(cu, [prev[i], cur[i]])
            j = (i + 1) % 3
            add_poly(cu, [prev[i], cur[j]] if k % 2 else [prev[j], cur[i]])
            add_poly(cu, [cur[i], cur[j]])
        prev = cur
    ob = bpy.data.objects.new('mast', cu); scene.collection.objects.link(ob)
    cu.materials.append(m_mastw)
    top = ring(1)
    return ob, (cx, cy, gz + hgt), gz
mast1, top1, gz1 = lattice(455, 1485, 105.0, 6.5, 1.6, 14, 0.45)
mast2, top2, gz2 = lattice(655, 1500, 68.0, 4.5, 1.2, 10, 0.32)
mast3, top3, gz3 = lattice(300, 1470, 48.0, 3.6, 1.0, 8, 0.28)
bm = bmesh.new()
import mathutils
def box(bm, c, s, rot=0.0):
    bmesh.ops.create_cube(bm, size=1.0, matrix=mathutils.Matrix.LocRotScale(c, mathutils.Euler((0, 0, rot)), s))
box(bm, (455, 1485, gz1 + 108), (1.2, 1.2, 8))
box(bm, (500, 1485, gz1 + 2.0), (9, 6, 4.0))
box(bm, (655, 1500, gz2 + 70), (0.9, 0.9, 6))
box(bm, (330, 1460, gz3 + 1.5), (6, 4, 3.0))
for zz in (0.55, 0.72, 0.88):   # dishes as thin boxes
    box(bm, (455 + 5.0, 1485 - 5.0, gz1 + 105 * zz), (5.5, 0.5, 5.5), 0.6)
me = bpy.data.meshes.new('masthw'); bm.to_mesh(me); bm.free(); me.materials.append(m_mastw)
ob = bpy.data.objects.new('masthw', me); scene.collection.objects.link(ob)
bm = bmesh.new()
bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=1.4, matrix=mathutils.Matrix.Translation((455, 1485, gz1 + 113)))
bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=1.1, matrix=mathutils.Matrix.Translation((655, 1500, gz2 + 77)))
me = bpy.data.meshes.new('beacons'); bm.to_mesh(me); bm.free(); me.materials.append(m_red)
ob = bpy.data.objects.new('beacons', me); scene.collection.objects.link(ob)

# ---------------------------------------------------------------- bushes
log('bushes...')
ico_bm = bmesh.new(); bmesh.ops.create_icosphere(ico_bm, subdivisions=1, radius=1.0)
ico_v = np.array([v.co[:] for v in ico_bm.verts]); ico_f = np.array([[v.index for v in f.verts] for f in ico_bm.faces])
ico_bm.free()
rng = np.random.default_rng(3)
def scatter(n_cand, rect, accept, size_lo, size_hi, palette, name, jitter=0.25, flat=0.7):
    x = rng.uniform(rect[0], rect[1], n_cand); y = rng.uniform(rect[2], rect[3], n_cand)
    keep = rng.random(n_cand) < accept(x, y)
    x, y = x[keep], y[keep]
    # avoid the track bench and swale line
    z = height(x, y)
    n = len(x)
    s = np.exp(rng.uniform(np.log(size_lo), np.log(size_hi), n))
    sx = s * rng.uniform(0.8, 1.4, n); sy = s * rng.uniform(0.8, 1.4, n); sz = s * flat * rng.uniform(0.7, 1.1, n)
    V = ico_v[None, :, :] * np.stack([sx, sy, sz], 1)[:, None, :]
    V = V * (1 + jitter * rng.standard_normal(V.shape))
    V[:, :, 2] += (sz * 0.3 + z)[:, None]
    V[:, :, 0] += x[:, None]; V[:, :, 1] += y[:, None]
    nv = ico_v.shape[0]
    F = ico_f[None, :, :] + (np.arange(n) * nv)[:, None, None]
    pal = np.array(palette)
    cols = pal[rng.integers(0, len(pal), n)] * rng.uniform(0.7, 1.25, (n, 1))
    C = np.repeat(cols[:, None, :], nv, 1)
    C = np.concatenate([C, np.ones((n, nv, 1))], 2)
    verts = V.reshape(-1, 3); faces = F.reshape(-1, 3)
    me = mesh_from_arrays(name, verts, faces)
    a = me.color_attributes.new('tint', 'FLOAT_COLOR', 'POINT')
    a.data.foreach_set('color', C.reshape(-1))
    me.materials.append(m_bush)
    ob = bpy.data.objects.new(name, me); scene.collection.objects.link(ob)
    return ob
sage_pal = [(0.014, 0.020, 0.007), (0.026, 0.034, 0.011), (0.040, 0.044, 0.014), (0.030, 0.020, 0.008), (0.070, 0.058, 0.022), (0.020, 0.028, 0.012)]
def acc_hill(x, y):
    g = fbm(x / 90, y / 260, 4, seed=21)
    return np.clip((g - 0.35) * 2.2, 0, 1) ** 1.3 * 0.9 * smooth(620, 700, y) * (1 - smooth(1600, 1680, y)) * (1 - 0.8 * np.exp(-((y - Y0) / 30) ** 2))
scatter(300000 if MODE == 'final' else 100000, (-400, 1120, 600, 1680), acc_hill, 1.0, 3.6, sage_pal, 'bush_hill', 0.42, 0.55)
def acc_fg(x, y):
    g = fbm(x / 40, y / 40, 4, seed=33)
    return np.clip((g - 0.38) * 3.0, 0, 1) * smooth(-440, -300, y) * (1 - smooth(440, 520, y)) * 0.75
scatter(70000, (-120, 920, -440, 520), acc_fg, 0.5, 2.0, sage_pal, 'bush_fg', 0.45, 0.6)

# ---------------------------------------------------------------- city
log('city...')
brng = np.random.default_rng(5)
bm_verts = []; bm_faces = []; bm_cols = []
cpal = [(0.34, 0.29, 0.24), (0.28, 0.30, 0.33), (0.42, 0.40, 0.36), (0.16, 0.22, 0.30), (0.28, 0.15, 0.11), (0.48, 0.46, 0.42), (0.22, 0.25, 0.28)]
cube_v = np.array([[-.5, -.5, 0], [.5, -.5, 0], [.5, .5, 0], [-.5, .5, 0], [-.5, -.5, 1], [.5, -.5, 1], [.5, .5, 1], [-.5, .5, 1]])
cube_f = np.array([[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]])
PITCH = 54.0
bxs = np.arange(-5600, 1500, PITCH); bys = np.arange(430, 3900, PITCH)
BX, BY = np.meshgrid(bxs, bys); BX = BX.ravel(); BY = BY.ravel()
dt = np.exp(-(((BX + 1900) / 800.0) ** 2 + ((BY - 2300) / 700.0) ** 2))
dens = 0.55 + 0.4 * fbm(BX / 600, BY / 600, 3, seed=9) + 0.6 * dt
verts = []; faces = []; cols = []; base = 0
for bx, by, dn, dd in zip(BX, BY, dens, dt):
    if brng.random() > dn: continue
    z0 = float(height(np.array([bx]), np.array([by]))[0])
    if z0 > PLAIN_Z + 7 or bx > -120: continue
    nb = int(brng.integers(2, 6))
    for _ in range(nb):
        w = brng.uniform(10, 26); d = brng.uniform(10, 26)
        px = bx + brng.uniform(-20, 20); py = by + brng.uniform(-20, 20)
        h = float(np.exp(brng.normal(2.35, 0.5))) * (1 + 7 * dd * brng.random()) * (1 + 0.5 * dd)
        v = cube_v * np.array([w, d, h]) + np.array([px, py, z0 - 0.5])
        verts.append(v); faces.append(cube_f + base); base += 8
        c = np.array(cpal[brng.integers(0, len(cpal))]) * brng.uniform(0.75, 1.2)
        cols.append(np.tile(np.append(c, 1.0), (8, 1)))
verts = np.concatenate(verts); faces = np.concatenate(faces); cols = np.concatenate(cols)
me = mesh_from_arrays('city', verts, faces)
try: me.shade_flat()
except Exception: pass
a = me.color_attributes.new('tint', 'FLOAT_COLOR', 'POINT'); a.data.foreach_set('color', cols.ravel())
me.materials.append(m_city)
ob = bpy.data.objects.new('city', me); scene.collection.objects.link(ob)
log('buildings', len(verts) // 8)

# ---------------------------------------------------------------- haze volume
m_haze, nt, out = new_mat('haze')
geo = N(nt, 'ShaderNodeNewGeometry'); sp_ = N(nt, 'ShaderNodeSeparateXYZ'); L(nt, geo.outputs['Position'], sp_.inputs[0])
zz = mathn(nt, 'MAXIMUM', mathn(nt, 'SUBTRACT', sp_.outputs['Z'], PLAIN_Z).outputs[0], 0.0)
ex = mathn(nt, 'EXPONENT', mathn(nt, 'MULTIPLY', mathn(nt, 'DIVIDE', zz.outputs[0], 520.0).outputs[0], -1.0).outputs[0])
dens_n = mathn(nt, 'MULTIPLY', ex.outputs[0], HAZE)
vs = N(nt, 'ShaderNodeVolumeScatter')
vs.inputs['Color'].default_value = (0.80, 0.86, 1.0, 1)
vs.inputs['Anisotropy'].default_value = 0.55
L(nt, dens_n.outputs[0], vs.inputs['Density'])
L(nt, vs.outputs['Volume'], out.inputs['Volume'])
bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
me = bpy.data.meshes.new('hazebox'); bm.to_mesh(me); bm.free(); me.materials.append(m_haze)
hb = bpy.data.objects.new('hazebox', me); scene.collection.objects.link(hb)
hb.location = (-1500, 4600, 700); hb.scale = (14000, 12000, 1900)
hb.visible_shadow = False
if os.environ.get('NOHAZE'): hb.hide_render = True

# ---------------------------------------------------------------- world
world = bpy.data.worlds.new('sky'); scene.world = world; world.use_nodes = True
wn = world.node_tree
for n in list(wn.nodes): wn.nodes.remove(n)
sky = wn.nodes.new('ShaderNodeTexSky')
sky.sky_type = 'MULTIPLE_SCATTERING' if 'MULTIPLE_SCATTERING' in [e.identifier for e in sky.bl_rna.properties['sky_type'].enum_items] else 'SINGLE_SCATTERING'
sky.sun_disc = True; sky.sun_size = math.radians(0.7)
sky.sun_elevation = math.radians(SUN_EL); sky.sun_rotation = SUN_ROT
print('SKYPROPS', [p.identifier for p in sky.bl_rna.properties if 'dens' in p.identifier or 'aerosol' in p.identifier or 'sun' in p.identifier])
sky.air_density = 1.0; sky.sun_intensity = 1.0
for k, v in (('dust_density', 3.2), ('aerosol_density', 3.2), ('ozone_density', 1.0)):
    if hasattr(sky, k): setattr(sky, k, v)
bg = wn.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = 1.0
wo = wn.nodes.new('ShaderNodeOutputWorld')
sdir = (math.sin(SUN_ROT) * math.cos(math.radians(SUN_EL)), math.cos(SUN_ROT) * math.cos(math.radians(SUN_EL)), math.sin(math.radians(SUN_EL)))
tcw = wn.nodes.new('ShaderNodeTexCoord')
sepw = wn.nodes.new('ShaderNodeSeparateXYZ'); wn.links.new(tcw.outputs['Generated'], sepw.inputs[0])
def wmath(op, a=None, b=None, clamp=False):
    m = wn.nodes.new('ShaderNodeMath'); m.operation = op; m.use_clamp = clamp
    for i, v in enumerate((a, b)):
        if v is None: continue
        if isinstance(v, (int, float)): m.inputs[i].default_value = v
        else: wn.links.new(v, m.inputs[i])
    return m
zc_ = wmath('MAXIMUM', sepw.outputs['Z'], 0.0)
den = wmath('ADD', zc_.outputs[0], 0.16)
px_ = wmath('DIVIDE', sepw.outputs['X'], den.outputs[0]); py_ = wmath('DIVIDE', sepw.outputs['Y'], den.outputs[0])
cvec = wn.nodes.new('ShaderNodeCombineXYZ')
wn.links.new(wmath('MULTIPLY', px_.outputs[0], 0.55).outputs[0], cvec.inputs['X'])
wn.links.new(wmath('MULTIPLY', py_.outputs[0], 1.5).outputs[0], cvec.inputs['Y'])
nz = wn.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.6; nz.inputs['Detail'].default_value = 7; nz.inputs['Roughness'].default_value = 0.62
wn.links.new(cvec.outputs[0], nz.inputs['Vector'])
cr = wn.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.46; cr.color_ramp.elements[1].position = 0.64
wn.links.new(nz.outputs['Fac'], cr.inputs['Fac'])
horizon_fade = wmath('MULTIPLY', wmath('SUBTRACT', sepw.outputs['Z'], 0.03).outputs[0], 5.0, True)
cmask = wmath('MULTIPLY', cr.outputs['Color'], horizon_fade.outputs[0]) if False else None
sepc = wn.nodes.new('ShaderNodeSeparateColor'); wn.links.new(cr.outputs['Color'], sepc.inputs[0])
cmask = wmath('MULTIPLY', sepc.outputs[0], horizon_fade.outputs[0])
vd = wn.nodes.new('ShaderNodeVectorMath'); vd.operation = 'DOT_PRODUCT'
wn.links.new(tcw.outputs['Generated'], vd.inputs[0]); vd.inputs[1].default_value = sdir
facing = wmath('POWER', wmath('MAXIMUM', vd.outputs['Value'], 0.0).outputs[0], 1.4)
ccol = wn.nodes.new('ShaderNodeMix'); ccol.data_type = 'RGBA'
wn.links.new(facing.outputs[0], ccol.inputs[0])
ccol.inputs[6].default_value = (2.3, 1.25, 1.15, 1); ccol.inputs[7].default_value = (3.4, 1.35, 0.45, 1)
lp = wn.nodes.new('ShaderNodeLightPath')
cam_mask = wmath('MULTIPLY', cmask.outputs[0], lp.outputs['Is Camera Ray'])
skymix = wn.nodes.new('ShaderNodeMix'); skymix.data_type = 'RGBA'
wn.links.new(cam_mask.outputs[0], skymix.inputs[0])
wn.links.new(sky.outputs['Color'], skymix.inputs[6]); wn.links.new(ccol.outputs[2], skymix.inputs[7])
wn.links.new(skymix.outputs[2], bg.inputs['Color']); wn.links.new(bg.outputs['Background'], wo.inputs['Surface'])

# ---------------------------------------------------------------- camera
cam_x, cam_y = 380.0, -250.0
cam_z = float(height(np.array([cam_x]), np.array([cam_y]))[0]) + 4.0
cam = bpy.data.cameras.new('cam'); cam.lens = 35; cam.sensor_width = 36; cam.clip_start = 1.0; cam.clip_end = 80000.0
cob = bpy.data.objects.new('cam', cam); scene.collection.objects.link(cob)
cob.location = (cam_x, cam_y, cam_z)
target = Vector((400, 1100, float(os.environ.get('AIMZ', '38'))))
cob.rotation_euler = (target - cob.location).to_track_quat('-Z', 'Y').to_euler()
scene.camera = cob
log('camera z', cam_z, 'sun_direction', tuple(sky.sun_direction))

# ---------------------------------------------------------------- render
r = scene.render
r.engine = 'CYCLES'
if MODE == 'final':
    r.resolution_x, r.resolution_y = 3200, 1800; scene.cycles.samples = 160
else:
    r.resolution_x, r.resolution_y = int(os.environ.get('RX', '960')), int(os.environ.get('RY', '540')); scene.cycles.samples = int(os.environ.get('SAMPLES', '24'))
scene.cycles.device = 'CPU'
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 6; scene.cycles.volume_bounces = 1
scene.cycles.volume_step_rate = 1.5 if MODE == 'preview' else 0.8
scene.cycles.volume_max_steps = 256
scene.cycles.use_adaptive_sampling = True
scene.view_settings.view_transform = 'Standard'
r.image_settings.file_format = 'OPEN_EXR'; r.image_settings.color_depth = '32'
if MODE == 'final': scene.cycles.volume_step_rate = 2.5
exr = OUT.replace('.png', '.exr')
r.filepath = exr
log('render start')
bpy.ops.render.render(write_still=True)
log('render done')

# ------------------------------------------------------------ grade
img = bpy.data.images.load(exr)
w_, h_ = img.size
a = np.empty(w_ * h_ * 4, np.float32); img.pixels.foreach_get(a); a = a.reshape(h_, w_, 4)
lum0 = (a[:, :, :3] * np.array([0.2126, 0.7152, 0.0722])).sum(2)
print('LUM pct', np.percentile(lum0, [5, 25, 50, 75, 95, 99.5]))
rgb = a[:, :, :3] * (2.0 ** EXPOSURE)
def blur(x, k, passes=3):
    for _ in range(passes):
        for ax in (0, 1):
            c = np.cumsum(np.pad(x, [(k, k) if i == ax else (0, 0) for i in range(3)], mode='edge'), axis=ax)
            sl_hi = [slice(None)] * 3; sl_lo = [slice(None)] * 3
            sl_hi[ax] = slice(2 * k, None); sl_lo[ax] = slice(0, -2 * k)
            x = (c[tuple(sl_hi)] - c[tuple(sl_lo)]) / (2 * k)
    return x
bright = np.clip(rgb - 1.6, 0, None)
bloom = blur(bright[::4, ::4], 6) if False else None
small = bright[::4, ::4]
bl = blur(small, 8)
bl = np.repeat(np.repeat(bl, 4, 0), 4, 1)[:h_, :w_]
bl2 = np.repeat(np.repeat(blur(bright[::8, ::8], 8), 8, 0), 8, 1)[:h_, :w_]
rgb = rgb + 0.18 * bl + 0.14 * bl2
# aces approximation
def aces(x):
    return np.clip((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0, 1)
t = aces(rgb * 0.9)
lum = (t * np.array([0.2126, 0.7152, 0.0722])).sum(2, keepdims=True)
t = np.clip(lum + (t - lum) * 1.12, 0, 1)
# gentle S-curve for contrast
t = np.clip(t, 0, 1); t = t + 0.18 * (t - 0.5) * (1 - np.abs(2 * t - 1)) * 2 * 0.5
# vignette
yy, xx = np.mgrid[0:h_, 0:w_]
vx = (xx / w_ - 0.5) * 2; vy = (yy / h_ - 0.5) * 2
vig = 1 - 0.22 * np.clip(vx ** 2 * 0.8 + vy ** 2 * 0.9, 0, 1.4)
t = t * vig[:, :, None]
# srgb
t = np.where(t <= 0.0031308, t * 12.92, 1.055 * np.power(np.clip(t, 1e-8, 1), 1 / 2.4) - 0.055)
grain = np.random.default_rng(1).normal(0, 0.006, (h_, w_, 1))
t = np.clip(t + grain, 0, 1)
out = np.concatenate([t, np.ones((h_, w_, 1))], 2).astype(np.float32)
res = bpy.data.images.new('graded', w_, h_, alpha=False, float_buffer=False)
res.colorspace_settings.name = 'sRGB'
res.pixels.foreach_set(out.ravel()); res.update()
res.filepath_raw = OUT; res.file_format = 'PNG'; res.save()
log('graded', OUT)
