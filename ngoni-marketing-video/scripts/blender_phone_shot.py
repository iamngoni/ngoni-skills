# App phone shot: graphite phone, real app capture as an emissive screen, slow push-in.
# Usage: Blender -b -P phone_shot.py -- <screen.png> <out.mp4> [frames] [save.blend]
import bpy, sys, math, os

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
SCREEN = os.path.abspath(argv[0]); OUT = os.path.abspath(argv[1])
FRAMES = int(argv[2]) if len(argv) > 2 else 90
SAVE = os.path.abspath(argv[3]) if len(argv) > 3 else None

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# --- render settings ---
engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
sc.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in engines else "BLENDER_EEVEE_NEXT"
sc.eevee.taa_render_samples = 24
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, 100
sc.render.fps = 30
sc.frame_start, sc.frame_end = 1, FRAMES
sc.view_settings.view_transform = "Standard"   # keep app UI colours true
sc.render.image_settings.media_type = "VIDEO" if hasattr(sc.render.image_settings, "media_type") else None
sc.render.image_settings.file_format = "FFMPEG"
sc.render.ffmpeg.format = "MPEG4"; sc.render.ffmpeg.codec = "H264"
sc.render.ffmpeg.constant_rate_factor = "HIGH"
sc.render.filepath = OUT

# --- world: warm evening backdrop ---
w = bpy.data.worlds.new("World"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.32, 0.22, 0.15, 1); bg.inputs[1].default_value = 0.6

def mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; return m

# backdrop card with soft gradient (warm lamp glow)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0.35, 0)); bd = bpy.context.object
bd.scale = (1.6, 1.6, 1); bd.rotation_euler = (math.radians(90), 0, 0)
mb = mat("Backdrop"); nt = mb.node_tree; p = nt.nodes["Principled BSDF"]
tc = nt.nodes.new("ShaderNodeTexCoord"); gr = nt.nodes.new("ShaderNodeTexGradient"); gr.gradient_type = "SPHERICAL"
mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Location"].default_value = (0.5, 0.5, 0); mp.inputs["Scale"].default_value = (1.4, 1.4, 1)
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (0.12, 0.07, 0.04, 1); ramp.color_ramp.elements[1].color = (0.85, 0.55, 0.32, 1)
nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], gr.inputs["Vector"])
nt.links.new(gr.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], p.inputs["Base Color"])
p.inputs["Roughness"].default_value = 1.0
bd.data.materials.append(mb)

# --- phone body ---
W, H, D = 0.0755, 0.1636, 0.0082
import bmesh
R = 0.0105; seg = 10; pts = []
for cx, cz, a0 in ((W/2-R, H/2-R, 0), (-W/2+R, H/2-R, 90), (-W/2+R, -H/2+R, 180), (W/2-R, -H/2+R, 270)):
    for i in range(seg + 1):
        a = math.radians(a0 + 90 * i / seg); pts.append((cx + R*math.cos(a), 0.0, cz + R*math.sin(a)))
me = bpy.data.meshes.new("PhoneBody"); bm = bmesh.new()
vs = [bm.verts.new(v) for v in pts]; bm.faces.new(vs); bm.to_mesh(me); bm.free()
body = bpy.data.objects.new("PhoneBody", me); sc.collection.objects.link(body)
body.location = (0, D/2, 0)
so = body.modifiers.new("solid", "SOLIDIFY"); so.thickness = D; so.offset = 1
bv = body.modifiers.new("bevel", "BEVEL"); bv.width = 0.0016; bv.segments = 4
bpy.ops.object.select_all(action="DESELECT")
mbody = mat("Graphite"); pb = mbody.node_tree.nodes["Principled BSDF"]
pb.inputs["Base Color"].default_value = (0.05, 0.055, 0.06, 1); pb.inputs["Metallic"].default_value = 0.9; pb.inputs["Roughness"].default_value = 0.28
body.data.materials.append(mbody)

# --- screen: real capture, emissive, alpha-rounded corners ---
SW, SH = W * 0.92, W * 0.92 * (2622 / 1206)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -D / 2 - 0.0004, 0)); scr = bpy.context.object; scr.name = "Screen"
scr.scale = (SW, SH, 1); scr.rotation_euler = (math.radians(90), 0, 0)
ms = mat("ScreenMat"); n = ms.node_tree; n.nodes.clear()
tex = n.nodes.new("ShaderNodeTexImage"); tex.image = bpy.data.images.load(SCREEN); tex.interpolation = "Cubic"
em = n.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 1.0
tr = n.nodes.new("ShaderNodeBsdfTransparent"); mix = n.nodes.new("ShaderNodeMixShader"); out = n.nodes.new("ShaderNodeOutputMaterial")
n.links.new(tex.outputs["Color"], em.inputs["Color"]); n.links.new(tex.outputs["Alpha"], mix.inputs["Fac"])
n.links.new(tr.outputs[0], mix.inputs[1]); n.links.new(em.outputs[0], mix.inputs[2]); n.links.new(mix.outputs[0], out.inputs["Surface"])
if hasattr(ms, "surface_render_method"): ms.surface_render_method = "BLENDED"
scr.data.materials.append(ms)
# flip so the image reads correctly from the front (-Y)
scr.rotation_euler = (math.radians(90), 0, math.radians(180)); scr.scale.x = -SW

phone = bpy.data.objects.new("Phone", None); sc.collection.objects.link(phone)
body.parent = phone; scr.parent = phone
phone.location = (0, 0, 0)
phone.rotation_euler = (math.radians(-8), 0, math.radians(14))
phone.keyframe_insert("rotation_euler", frame=1)
phone.rotation_euler = (math.radians(-3), 0, math.radians(4))
phone.keyframe_insert("rotation_euler", frame=FRAMES)

# --- lights ---
def area(loc, energy, color, size):
    l = bpy.data.lights.new("A", "AREA"); l.energy = energy; l.color = color; l.size = size
    o = bpy.data.objects.new("A", l); sc.collection.objects.link(o); o.location = loc
    c = o.constraints.new("TRACK_TO"); c.target = phone; return o
area((-0.35, -0.4, 0.35), 18, (1.0, 0.78, 0.55), 0.35)   # warm key
area((0.4, -0.2, 0.1), 6, (0.8, 0.9, 1.0), 0.5)           # cool rim

# --- camera: slow push-in with shallow depth of field ---
cd = bpy.data.cameras.new("Cam"); cd.lens = 70; cd.dof.use_dof = True; cd.dof.aperture_fstop = 4.0
cam = bpy.data.objects.new("Cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cd.dof.focus_object = phone
aim = bpy.data.objects.new("Aim", None); sc.collection.objects.link(aim); aim.location = (0, 0, 0.036)
cam.location = (0.03, -0.60, 0.05); cam.keyframe_insert("location", frame=1)
cam.location = (0.0, -0.49, 0.036); cam.keyframe_insert("location", frame=FRAMES)
tt = cam.constraints.new("TRACK_TO"); tt.target = aim
for fc in (cam.animation_data.action.fcurves if hasattr(cam.animation_data.action, "fcurves") else []):
    for k in fc.keyframe_points: k.interpolation = "SINE"

if SAVE: bpy.ops.wm.save_as_mainfile(filepath=SAVE)
bpy.ops.render.render(animation=True)
print("RENDERED", OUT)
