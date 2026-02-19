from krita import *

all_presets = Application.resources("preset")

name = "b) Airbrush Soft"
resource = all_presets[name]

#qmwin = Krita.instance().activeWindow().qwindow()
k = Krita.instance()
window = k.activeWindow() 
#window.activeView().setCurrentBrushPreset(resource)
qmwin = window.qwindow()
#print(view)
#view.setCurrentBrushPreset(resource)
#qmwin = window.qwindow()
#qmwin = view.window().qwindow()
w1 = qmwin.findChild(QWidget, "KisPaintOpPresetsEditor")
pc = PresetChooser(w1)
pc.setCurrentPreset(resource)
#w1.paintopActivated(name)
#w1.KisPaintOpPresetsEditor
##w1.setCurrentPaintOpId(name)
#stuff = (dir(w1.staticMetaObject.connectSlotsByName))
#w1.metaObject.KisPaintOpPresetsEditor
w2 = w1.findChild(QWidget, "liveBrushPreviewView")
pc = PresetChooser(w2)
pc.setCurrentPreset(resource)
#w2.setForegroundBrush(all_presets[name])
    #print(all_presets)
#print(type(all_presets))
#stuff = (dir(w2.staticMetaObject))
#with open("./Desktop/debugging.txt", mode="w") as wfile: wfile.writelines([thing + "\n" for thing in stuff])
pixmap = w2.grab()
pixmap.save("./Desktop/presets/%s.png" % name, format="png")

#for name, resource in all_presets.items(): pass
#help(all_presets)
    #psc = PresetChooser()
#rs = "c) Pencil-1 Hard"
    #psc.setCurrentPreset(resource)
    #pixmap = w2.grab()
    #pixmap.save("./Desktop/presets/%s.png" % name, format="png")
#w2.grab

'''
with open("./Desktop/presets.txt", mode="w") as wfile:
    wfile.writelines([preset + "\n" for preset in all_presets])
'''
