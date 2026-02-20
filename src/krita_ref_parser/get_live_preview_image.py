import os
from pathlib import Path
from krita import *

# initialize Krita
#K = Krita.instance()

# get preset
name = "b) Airbrush Soft"
preset = Application.resources("preset")[name]

# declare filename and cleanup
filename = os.path.join(".", "Desktop", "presets", name + '.png')
Path(filename).unlink(missing_ok=True)

# open document
document = Application.createDocument(1, 1, "GET_BRUSH_PREVIEW", "RGBA", "U8", "", 120.0)
active_window = Application.activeWindow()
active_window.addView(document)
active_view = active_window.activeView()
print(active_view.currentBrushPreset())
print(active_view.currentBrushPreset())

# locate brush previewer
qmwin = active_window.qwindow()
presets_editor = qmwin.findChild(QWidget, "KisPaintOpPresetsEditor")
active_view.setCurrentBrushPreset(preset)
brush_previewer = presets_editor.findChild(QGraphicsView, "liveBrushPreviewView")
#active_view.setCurrentBrushPreset(preset)

# extract and save
pixmap = brush_previewer.grab()
pixmap.save(filename)

'''
import os
from krita import *
def func():
    k = Krita.instance()
    window = k.activeWindow() 
    qmwin = window.qwindow()
    presets_editor = qmwin.findChild(QWidget, "KisPaintOpPresetsEditor")
    brush_previewer = presets_editor.findChild(QGraphicsView, "liveBrushPreviewView")
    pixmap = brush_previewer.grab()
    fp = os.path.join("Desktop", "presets", "test" + '.png')
    pixmap.save(fp)
func()
'''
