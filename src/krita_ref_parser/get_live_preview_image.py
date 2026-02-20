import os
from krita import *

# initialize Krita
K = Krita.instance()
# open document
ACTIVE_WINDOW = K.activeWindow()

def save_preset(name: str, preset, directory: str):
    """
    """
    # locate brush previewer
    qmwin = ACTIVE_WINDOW.qwindow()
    presets_editor = qmwin.findChild(QWidget, "KisPaintOpPresetsEditor")
    brush_previewer = presets_editor.findChild(QGraphicsView, "liveBrushPreviewView")
    # render
    #brush_previewer.render(QPainter())
    # extract and save
    pixmap = brush_previewer.grab()
    filename = os.path.join(directory, name + '.png')
    return pixmap.save(filename)

if __name__ == "__main__":
    # get all presets
    ALL_PRESETS = K.resources("preset")
    # save live-previews of all presets
    directory = "Desktop/presets"
    '''
    for name, preset in ALL_PRESETS.items():
        ACTIVE_WINDOW.activeView().setCurrentBrushPreset(preset)
        save_preset(name, preset, directory)
    '''
    name = "b) Airbrush Soft"
    preset = ALL_PRESETS[name]
    save_preset(name, preset, directory)
