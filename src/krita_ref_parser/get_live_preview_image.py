import os

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
    #PresetChooser(brush_previewer).setCurrentPreset(preset)
    preset_chooser = PresetChooser(QWidget=brush_previewer); preset_chooser.setCurrentPreset(preset)
    print(preset_chooser.currentPreset())
    pixmap = brush_previewer.grab()
    filename = os.path.join(".", "Desktop", "presets", name + '.png')
    return pixmap.save(filename)

name = "b) Airbrush Soft"
preset = get_preset(name)
save_preset(name, preset)

if __name__ == "__main__":
    name = "b) Airbrush Soft"
    preset = get_preset(name)
    save_preset(name, preset)
    #for name, preset in ALL_PRESETS.items(): save_preset(name, preset)

'''
from Krita import *

def add_document_to_window():
    d = Application.createDocument(100, 100, "Test", "RGBA", "U8", "", 120.0)
    Application.activeWindow().addView(d)
    View.setCurrentBrushPreset(Resource)
    Window.activeView()

add_document_to_window()
'''
