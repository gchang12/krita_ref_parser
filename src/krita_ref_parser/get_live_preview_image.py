import os
from krita import *

# initialize Krita
K = Krita.instance()

# get all presets
ALL_PRESETS = K.resources("preset")

# get preset for testing
name = "b) Airbrush Soft"
preset = ALL_PRESETS[name]

# open document
active_window = K.activeWindow()
active_view = active_window.activeView()
#document = K.createDocument(1, 1, "GET_BRUSH_PREVIEW", "RGBA", "U8", "", 120.0)
#active_window.addView(document)

active_view.setCurrentBrushPreset(preset) # TODO: Figure out where this goes.

# locate brush previewer
qmwin = active_window.qwindow()
presets_editor = qmwin.findChild(QWidget, "KisPaintOpPresetsEditor")
brush_previewer = presets_editor.findChild(QGraphicsView, "liveBrushPreviewView")

# extract and save
pixmap = brush_previewer.grab()
filename = os.path.join(".", "Desktop", "presets", name + '.png')
pixmap.save(filename)

