import os
from krita import *

# initialize Krita
K = Krita.instance()

# get preset
name = "b) Airbrush Soft"
preset = K.resources("preset")[name]

# open document
document = K.createDocument(1, 1, "GET_BRUSH_PREVIEW", "RGBA", "U8", "", 120.0)
active_window = K.activeWindow()
active_window.addView(document)
active_view = active_window.activeView()

# locate brush previewer
active_view.setCurrentBrushPreset(preset)
qmwin = active_window.qwindow()
presets_editor = qmwin.findChild(QWidget, "KisPaintOpPresetsEditor")
brush_previewer = presets_editor.findChild(QGraphicsView, "liveBrushPreviewView")

# extract and save
pixmap = brush_previewer.grab()
filename = os.path.join(".", "Desktop", "presets", name + '.png')
pixmap.save(filename)
