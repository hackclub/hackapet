import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

import timer

class Dialogue:
    def __init__(self):
        self.bgSheet = displayio.OnDiskBitmap("assets/dialogue.bmp")
        self.bgSprite = displayio.TileGrid(
            self.bgSheet,
            pixel_shader=self.bgSheet.pixel_shader
        )

        self.bgSprite.hidden = True
        self.speakers = {}
        
        self.font = bitmap_font.load_font("assets/RobotoMono.bdf")

        self.label = label.Label(self.font, text="", color=0xFFFFFF)
        self.label.line_spacing = 0.6
        self.label.x = 10
        self.label.y = 10
        
        self.texts = []
        self.currentText = 0
        self.textCutoff = 0
        self.speaking = False

        self.finishedSpeaking = False
        self.autoContinue = False
        
        self.afterDialogue = None
    
    def loadSpeaker(self, file, name):
        sheet = displayio.OnDiskBitmap(file)
        self.speakers[name] = displayio.TileGrid(sheet, pixel_shader=sheet.pixel_shader, x=87, y=9)
        self.speakers[name].hidden = True
    
    def speak(self, speaker, dialogue, afterDialogue, autoContinue):
        self.bgSprite.hidden = False

        if speaker != None:
            self.speakers[speaker].hidden = False
        
        self.speaking = True
        self.texts = dialogue
        self.currentText = 0
        self.textCutoff = 0
        self.afterDialogue = afterDialogue
        self.autoContinue = autoContinue

    def hide(self):
        self.label.text = ""
        self.bgSprite.hidden = True
        self.speaking = False
        
        for _, speaker in self.speakers.items():
            speaker.hidden = True
        
        
    def update(self):
        if self.speaking:
            if self.textCutoff < len(self.texts[self.currentText]):
                self.textCutoff += 1
            else:
                if self.autoContinue and not self.finishedSpeaking:
                    self.finishedSpeaking = True
                    timer.createAndStartTimer(15, self.nextText)
            
            
            self.label.text = self.texts[self.currentText][:self.textCutoff]
    
    def nextText(self):
        if self.currentText >= len(self.texts): return

        if self.textCutoff < len(self.texts[self.currentText]):
            self.textCutoff = len(self.texts[self.currentText])
            return

        self.textCutoff = 0
        self.currentText += 1
        self.finishedSpeaking = False
        
        if self.currentText >= len(self.texts):
            self.hide()

            if self.afterDialogue != None: self.afterDialogue()
            

    


