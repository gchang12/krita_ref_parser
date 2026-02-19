import os
from pathlib import Path

from krita import *

ALL_PRESETS = Application.resources("preset")

def get_preset(name):
    return ALL_PRESETS[name]

def save_preset(name, preset):
    k = Krita.instance()
    window = k.activeWindow() 
    qmwin = window.qwindow()
    presets_editor = qmwin.findChild(QWidget, "KisPaintOpPresetsEditor")
    brush_previewer = presets_editor.findChild(QGraphicsView, "liveBrushPreviewView")
    presets_chooser = PresetChooser(brush_previewer)
    presets_chooser.setCurrentPreset(preset)
    pixmap = presets_chooser.grab()
    pixmap.save(os.path.join(".", "Desktop", "presets", name + '.png'))

if __name__ == "__main__":
    #name = "b) Airbrush Soft"
    #preset = get_preset(name)
    #save_preset(name, preset)
    for name, preset in ALL_PRESETS.items():
        save_preset(name, preset)

'''
a) Eraser Circle
a) Eraser Small
a) Eraser Soft
b) Airbrush Soft
b) Basic-1
b) Basic-2 Opacity
b) Basic-3 Flow
b) Basic-4 Flow Opacity
b) Basic-5 Size
b) Basic-5 Size Opacity
b) Basic-6 Details
c) Pencil 1 Sketch (mypaint)
c) Pencil 2b (mypaint)
c) Pencil-1 Hard
c) Pencil-2
c) Pencil-3 Large 4B
c) Pencil-4 Soft
c) Pencil-5 Tilted
c) Pencil-6 Quick Shade
d) Ink pen (mypaint)
d) Ink-1 Precision
d) Ink-2 Fineliner
d) Ink-3 Gpen
d) Ink-4 Pen Rough
d) Ink-7 Brush Rough
d) Ink-8 Sumi-e
e) Marker Chisel Smooth
e) Marker Details
e) Marker Dry
e) Marker Medium (mypaint)
e) Marker Plain (mypaint)
f) Bristles-1 Details
f) Bristles-2 Flat Rough
f) Bristles-3 Large Smooth
f) Bristles-4 Glaze
f) Bristles-5 Flat
f) Charcoal Rock Soft
f) Dry Roller
g) Dry Bristles
g) Dry Bristles Eroded
g) Dry Brushing
g) Dry Textured Creases
h) Chalk Details
h) Chalk Grainy
h) Chalk Soft
h) Charcoal Pencil Medium
h) Charcoal Pencil Thin
h) Charcoal pencil large
i) Wet Bristles
i) Wet Bristles Rough
i) Wet Circle
i) Wet Knife
i) Wet Knife Plus (mypaint)
i) Wet Paint
i) Wet Paint Details
i) Wet Paint Plus (mypaint)
i) Wet Smear
i) Wet Textured Soft
j) WaterC Basic Lines-Dry
j) WaterC Basic Lines-Wet
j) WaterC Basic Lines-Wet-Pattern
j) WaterC Basic Round-Fringe 02
j) WaterC Basic Round-Grain
j) WaterC Basic Round-Grunge
j) WaterC Flat Big-Grain Tilt
j) WaterC Flat Decay Tilt
j) WaterC Special Blobs
j) WaterC Special Splats
j) WaterC Spread
j) WaterC Spread WideArea
j) WaterC Spread-Pattern
j) WaterC Water-Pattern
j) Watercolor Fringe
j) Watercolor Texture
j) Waterpaint Hard Edges
j) Waterpaint Soft Edges
k) Blender Basic
k) Blender Blur
k) Blender Knife Edge
k) Blender Pixelize
k) Blender Rake
k) Blender Smear
k) Blender Textured Soft
l) Adjust Color
l) Adjust Dodge
l) Adjust Lighten
l) Adjust Multiply
l) Adjust Overlay Burn
m) RGBA 01 Thick-dry
m) RGBA 02 Thickpaint
m) RGBA 03 Rake
m) RGBA 04 Impasto
m) RGBA 05 Impasto-details
m) RGBA 06 Rock
t) Shapes Fill
t) Shapes Mecha
t) Shapes Rounded
t) Shapes Spikes
t) Shapes Square
u) Pixel Art
u) Pixel Art Dithering
u) Pixel Art Fill
v) Clone Tool
v) Distort Grow
v) Distort Move
v) Distort Shrink
v) Experimental Webs
v) Sketching-1 Chrome Thin
v) Sketching-2 Chrome Large
v) Sketching-3 Leaky
v) Texture Impressionism
v) Texture Pointillism
w) Texture Normal Map
x) Filter Blur
x) Filter Sharpen
y) Screentone Moire
y) Screentone Pressure
y) Screentones Regular
y) Texture Big
y) Texture Crackles
y) Texture Hair
y) Texture Large Splat
y) Texture Noise
y) Texture Random Particles
y) Texture Reptile
y) Texture Snow Pile
y) Texture Spines
y) Texture Splat
y) Texture Spray
y) Texture Starfield
y) Texture Wood Fiber
z) Stamp Bokeh
z) Stamp Floor
z) Stamp Grass
z) Stamp Grass Patch
z) Stamp Hearts
z) Stamp Herbals
z) Stamp Leaves
z) Stamp Mountains Distant
z) Stamp Shoujo Bubbles
z) Stamp Sparkles
z) Stamp Stylised Tree
z) Stamp Vegetal
z) Stamp Water
'''
