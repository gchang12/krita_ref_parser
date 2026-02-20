import os
from krita import *

# initialize Krita
K = Krita.instance()
# open document
document = K.createDocument(1, 1, "GET_BRUSH_PREVIEW", "RGBA", "U8", "", 120.0)
#active_window = K.activeWindow()
#view = active_window.addView(document)
# get preset
ALL_PRESETS = Application.resources("preset")
name = "b) Airbrush Soft"
preset = ALL_PRESETS[name]
# change brush preset of view
view = active_window.activeView()
view.setCurrentBrushPreset(preset)
# locate brush previewer
qmwin = active_window.qwindow()
presets_editor = qmwin.findChild(QWidget, "KisPaintOpPresetsEditor")
brush_previewer = presets_editor.findChild(QGraphicsView, "liveBrushPreviewView")
# extract and save
pixmap = brush_previewer.grab()
filename = os.path.join(".", "Desktop", "presets", name + '.png')
pixmap.save(filename)
