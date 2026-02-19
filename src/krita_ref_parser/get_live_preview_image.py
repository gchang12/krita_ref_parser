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

