import os
from krita import *

# initialize Krita
K = Krita.instance()
# open document
ACTIVE_WINDOW = K.activeWindow()

def save_preset(name, preset, directory):
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
    # save live-previews of ten presets
    directory = "Desktop/presets"
    maximum = 10
    presets = set()
    for preset_no, (name, preset) in enumerate(ALL_PRESETS.items(), start=1):
        if preset_no == maximum:
            break
        ACTIVE_WINDOW.activeView().setCurrentBrushPreset(preset)
        presets.add(ACTIVE_WINDOW.activeView().currentBrushPreset().name())
        save_preset(name, preset, directory)
    print(len(presets)) # output should imply that this is equal to 1.
