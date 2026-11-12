# Reuse a saved phone .blend: swap the screen capture and retime. Usage: Blender -b X.blend -P retexture.py -- <screen.png> <out.mp4> <frames>
import bpy, sys, time
a = sys.argv[sys.argv.index("--") + 1:]; t = time.time(); sc = bpy.context.scene; F = int(a[2])
tex = [n for n in bpy.data.materials["ScreenMat"].node_tree.nodes if n.type == "TEX_IMAGE"][0]
tex.image = bpy.data.images.load(a[0])
for ob in (bpy.data.objects["Cam"], bpy.data.objects["Phone"]):
    act = ob.animation_data.action
    fcs = list(act.fcurves) if hasattr(act, "fcurves") else [fc for l in act.layers for s in l.strips for cb in s.channelbags for fc in cb.fcurves]
    for fc in fcs:
        for k in fc.keyframe_points:
            if k.co.x > 1: k.co.x = F; k.handle_left.x = F - 10; k.handle_right.x = F + 10
sc.frame_end = F; sc.render.filepath = a[1]
bpy.ops.render.render(animation=True)
print("RETEXTURED", round(time.time() - t, 1), "s")
