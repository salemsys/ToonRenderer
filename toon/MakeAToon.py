from toon import ToonDNA, Toon
from panda3d.core import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject

speciesDict = {
    'dog': 'doghead',
    'cat': 'cathead',
    'monkey': 'monkeyhead',
    'bear': 'bearhead',
    'rabbit': 'bunnyhead',
    'duck': 'duckhead',
    'mouse': 'mousehead',
    'horse': 'horsehead',
    'pig': 'pighead',
    'crocodile': 'crocodilehead'
}

class MakeAToon(DirectObject):

    def __init__(self):
        camera.hide()

        self.dna = ToonDNA.ToonDNA()
        self.dna.newToonRandom(stage=1)
        self.dna.head = 'ass'
        self.toon = Toon.Toon()
        self.toon.setDNA(self.dna)
        self.toon.useLOD(1000)
        self.toon.reparentTo(render)
        self.toon.loop('neutral')

        self.editing = False

        self.toonFont = loader.loadFont('phase_3/fonts/ImpressBT.ttf')
        self.mickeyFont = loader.loadFont('phase_3/fonts/MickeyFontMaximum.bam')

        self.clickSfx = loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg')
        self.rolloverSfx = loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg')

        # GUI #
        geom = loader.loadModel('phase_3/models/gui/tt_m_gui_ups_panelBg.bam')
        self.mainFrame = DirectFrame(geom=geom, frameSize=(-.35, .35, -.4, .4))
        self.mainFrame.setPos(-1.0, 0, .12)
        self.mainFrame.setScale(1.8)
        self.mainFrame.hide()

        self.matPage = self.mainFrame.attachNewNode('matPages')
        self.matPageNum = 0

        geom = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui.bam')
        self.rightPageButton = DirectButton(geom=(
        geom.find('**/tt_t_gui_mat_arrowUp'), geom.find('**/tt_t_gui_mat_arrowDown'),
        geom.find('**/tt_t_gui_mat_arrowUp')), clickSound=self.clickSfx,
                                            frameSize=(.1, -.12, .07, -.07), frameVisibleScale=(0, 0),
                                            pos=(-.75, 0, -.85), command=self.changePage, extraArgs=[1])
        self.leftPageButton = DirectButton(geom=(
        geom.find('**/tt_t_gui_mat_arrowUp'), geom.find('**/tt_t_gui_mat_arrowDown'),
        geom.find('**/tt_t_gui_mat_arrowUp')), clickSound=self.clickSfx,
                                           frameSize=(.1, -.12, .07, -.07), frameVisibleScale=(0, 0),
                                           pos=(-1.25, 0, -.85), hpr=(0, 0, 180), command=self.changePage,
                                           extraArgs=[-1])
        self.leftPageButton["state"] = DGG.DISABLED

        # SPECIES PAGE #
        self.speciesPage = self.matPage.attachNewNode('speciesPage')
        self.speciesPage.setScale(.9)
        self.speciesText = OnscreenText(text='Toon Species', parent=self.speciesPage, font=self.mickeyFont, fg=(1,0,0,1),pos=(0, .37))
        laffMeter = loader.loadModel('phase_3/models/gui/laff_o_meter.bam')
        x = -.6
        z = .21
        for species in speciesDict:
            speciesFace = laffMeter.find('**/%s' % (speciesDict[species]))
            smile = loader.loadModel('phase_3/models/gui/laff_o_meter.bam').find('**/smile')
            smile.reparentTo(speciesFace)
            smile.setZ(-.3)
            smile.setScale(.75)
            if x >= .1:
                z -= .17
                x = -.6
            x += .3
            DirectButton(geom=speciesFace, scale=.055, pos=(x, 0, z), frameSize=(.9, -.9, .9, -.9),
                         frameVisibleScale=(0, 0),
                         parent=self.speciesPage, command=self.changeSpecies, extraArgs=[species],
                         clickSound=self.clickSfx)

        # LIMB PAGE #
        self.limbPage = self.matPage.attachNewNode('limbPage')
        self.limbText = OnscreenText(text='Toon Body', parent=self.limbPage, font=self.mickeyFont, fg=(1,0,0,1),pos=(0, .33),
                                     scale=.069)
        torsombutton = DirectButton(text='medium shorts', geom=(
        geom.find('**/tt_t_gui_mat_shuffleUp'), geom.find('**/tt_t_gui_mat_shuffleDown'),
        geom.find('**/tt_t_gui_mat_shuffleUp')
                                    ), scale=.045, pos=(-0.2, 0, .23),
                                    frameSize=(1.2, -1.2, .9, -.9),text_fg=(1,1,1,1),
                                    frameVisibleScale=(0, 0), geom_scale=(18,12,12), text_pos=(0,-.3),
                                    parent=self.limbPage, command=self.changeTorso, extraArgs="m",
                                    clickSound=self.clickSfx, text_font=self.mickeyFont
                                    )
        torsolbutton = DirectButton(text='tall shorts', geom=(
        geom.find('**/tt_t_gui_mat_shuffleUp'), geom.find('**/tt_t_gui_mat_shuffleDown'),
        geom.find('**/tt_t_gui_mat_shuffleUp')
                                    ), scale=.045, pos=(-0.2, 0, .13), frameSize=(1.2, -1.2, .9, -.9),
                                    frameVisibleScale=(0, 0),text_fg=(1,1,1,1),  geom_scale=(18,12,12), text_pos=(0,-.3),
                                    parent=self.limbPage, text_font=self.mickeyFont, command=self.changeTorso, extraArgs="l",
                                    clickSound=self.clickSfx)
        torsosbutton = DirectButton(text='short shorts', geom=(
        geom.find('**/tt_t_gui_mat_shuffleUp'), geom.find('**/tt_t_gui_mat_shuffleDown'),
        geom.find('**/tt_t_gui_mat_shuffleUp')
                                    ), scale=.045, pos=(-0.2, 0, 0.03),
                                    frameSize=(1.2, -1.2, .9, -.9),text_fg=(1,1,1,1),
                                    frameVisibleScale=(0, 0),  geom_scale=(18,12,12), text_pos=(0,-.3),
                                    parent=self.limbPage, command=self.changeTorso, extraArgs="s",
                                    clickSound=self.clickSfx, text_font=self.mickeyFont)
        torsomsbutton = DirectButton(text='medium skirt', geom=(
        geom.find('**/tt_t_gui_mat_shuffleUp'), geom.find('**/tt_t_gui_mat_shuffleDown'),
        geom.find('**/tt_t_gui_mat_shuffleUp')
                                    ), scale=.045, pos=(0.2, 0, .23),
                                    frameSize=(1.2, -1.2, .9, -.9),text_fg=(1,1,1,1),
                                    frameVisibleScale=(0, 0), geom_scale=(18,12,12), text_pos=(0,-.3),
                                    parent=self.limbPage, command=self.changeTorso, extraArgs="d",
                                    clickSound=self.clickSfx, text_font=self.mickeyFont
                                    )
        torsolsbutton = DirectButton(text='tall skirt', geom=(
        geom.find('**/tt_t_gui_mat_shuffleUp'), geom.find('**/tt_t_gui_mat_shuffleDown'),
        geom.find('**/tt_t_gui_mat_shuffleUp')
                                    ), scale=.045, pos=(0.2, 0, .13), frameSize=(1.2, -1.2, .9, -.9),
                                    frameVisibleScale=(0, 0),text_fg=(1,1,1,1),  geom_scale=(18,12,12), text_pos=(0,-.3),
                                    parent=self.limbPage, text_font=self.mickeyFont, command=self.changeTorso, extraArgs="j",
                                    clickSound=self.clickSfx)
        torsossbutton = DirectButton(text='short skirt', geom=(
        geom.find('**/tt_t_gui_mat_shuffleUp'), geom.find('**/tt_t_gui_mat_shuffleDown'),
        geom.find('**/tt_t_gui_mat_shuffleUp')
                                    ), scale=.045, pos=(0.2, 0, 0.03),
                                    frameSize=(1.2, -1.2, .9, -.9),text_fg=(1,1,1,1),
                                    frameVisibleScale=(0, 0),  geom_scale=(18,12,12), text_pos=(0,-.3),
                                    parent=self.limbPage, command=self.changeTorso, extraArgs="k",
                                    clickSound=self.clickSfx, text_font=self.mickeyFont)
        legmbutton = DirectButton(text='medium legs', geom=(
        geom.find('**/tt_t_gui_mat_shuffleUp'), geom.find('**/tt_t_gui_mat_shuffleDown'),
        geom.find('**/tt_t_gui_mat_shuffleUp')
                                    ), scale=.045, pos=(0, 0, -.15),
                                    frameSize=(1.2, -1.2, .9, -.9),text_fg=(1,1,1,1),
                                    frameVisibleScale=(0, 0),  geom_scale=(18,12,12), text_pos=(0,-.3),
                                    parent=self.limbPage, command=self.changeLegs, extraArgs="m",
                                    clickSound=self.clickSfx, text_font=self.mickeyFont)
        leglbutton = DirectButton(text='tall legs', geom=(
        geom.find('**/tt_t_gui_mat_shuffleUp'), geom.find('**/tt_t_gui_mat_shuffleDown'),
        geom.find('**/tt_t_gui_mat_shuffleUp')
                                    ), text_fg=(1,1,1,1),scale=.045, pos=(0, 0, -.25), frameSize=(1.2, -1.2, .9, -.9),
                                    frameVisibleScale=(0, 0),  geom_scale=(18,12,12), text_pos=(0,-.3),
                                    parent=self.limbPage, command=self.changeLegs, extraArgs="l",
                                    clickSound=self.clickSfx, text_font=self.mickeyFont)
        legsbutton = DirectButton(text='short legs', geom=(
        geom.find('**/tt_t_gui_mat_shuffleUp'), geom.find('**/tt_t_gui_mat_shuffleDown'),
        geom.find('**/tt_t_gui_mat_shuffleUp')
                                    ), text_fg=(1,1,1,1),scale=.045, pos=(0, 0, -.35),
                                    frameSize=(1.2, -1.2, .9, -.9),
                                    frameVisibleScale=(0, 0),  geom_scale=(18,12,12), text_pos=(0,-.3),
                                    parent=self.limbPage, command=self.changeLegs, extraArgs="s",
                                    clickSound=self.clickSfx, text_font=self.mickeyFont)

        self.limbPage.hide()

        # COLOR PAGE #
        self.colorPage = self.matPage.attachNewNode('colorPage')
        self.colorText = OnscreenText(text='Toon Color', parent=self.colorPage, font=self.mickeyFont,fg=(1,0,0,1), pos=(0, .33),
                                      scale=.069)
        self.colorPage.hide()
        x = -.45
        z = .21
        colorIndex = -1
        for color in ToonDNA.allColorsList:
            colorIndex = colorIndex+1
            if x >= .2:
                z -= .125
                x = -.45
            x += .15
            colorButton = DirectButton(geom=None, scale=.045, pos=(x, 0, z), frameSize=(.9, -.9, .9, -.9),
                                       frameColor=color,
                                       parent=self.colorPage, command=self.changeColor, extraArgs=[colorIndex],
                                       clickSound=self.clickSfx)

        # OUTFIT PAGE #
        self.outfitPage = self.matPage.attachNewNode('outfitPage')
        self.outfitPage.setScale(0.75)
        self.outfitPage.setZ(0.045)
        self.colorText = OnscreenText(text='Toon Clothes', parent=self.outfitPage, font=self.mickeyFont,fg=(1,0,0,1), pos=(0, 0.37),
                                      scale=.095)
        self.outfitPage.hide()

        shirtString = OnscreenText(text="Shirt Index", pos=(-0.1, 0.20), scale=0.03, align=TextNode.ACenter,
                                  mayChange=1, font=self.toonFont, parent=self.outfitPage)
        shirtEntry = DirectEntry(text="", scale=.04, command=self.setShirt, parent=self.outfitPage,
                            numLines=1, focus=1, pos=(-0.25, 0, 0.25))

        shirtColorString = OnscreenText(text="Shirt Color Index", pos=(-0.1, 0.08), scale=0.03, align=TextNode.ACenter,
                                  mayChange=1, font=self.toonFont, parent=self.outfitPage)
        shirtColorEntry = DirectEntry(text="", scale=.04, command=self.setShirtColor, parent=self.outfitPage,
                            numLines=1, focus=1,pos=(-0.25, 0, 0.13))

        sleeveString = OnscreenText(text="Sleeve Index", pos=(-0.1, -0.07), scale=0.03, align=TextNode.ACenter,
                                  mayChange=1, font=self.toonFont, parent=self.outfitPage)
        sleeveEntry = DirectEntry(text="", scale=.04, command=self.setSleeve, parent=self.outfitPage,
                            numLines=1, focus=1,pos=(-0.25, 0, -0.02))

        sleeveColorString = OnscreenText(text="Sleeve Color Index", pos=(-0.1, -0.22), scale=0.03, align=TextNode.ACenter,
                                  mayChange=1, font=self.toonFont, parent=self.outfitPage)
        sleeveColorEntry = DirectEntry(text="", scale=.04, command=self.setSleeveColor, parent=self.outfitPage,
                            numLines=1, focus=1,pos=(-0.25, 0, -0.17))

        botString = OnscreenText(text="Bottom Index", pos=(-0.1, -0.37), scale=0.03, align=TextNode.ACenter,
                                  mayChange=1, font=self.toonFont, parent=self.outfitPage)
        botEntry = DirectEntry(text="", scale=.04, command=self.setBottom, parent=self.outfitPage,
                            numLines=1, focus=1,pos=(-0.25, 0, -0.32))

        botColorString = OnscreenText(text="Bottom Color Index", pos=(-0.1, -0.52), scale=0.03, align=TextNode.ACenter,
                                  mayChange=1, font=self.toonFont, parent=self.outfitPage)
        botColorEntry = DirectEntry(text="", scale=.04, command=self.setBottomColor, parent=self.outfitPage,
                            numLines=1, focus=1,pos=(-0.25, 0, -0.47))

        # ANIMATION PAGE #
        self.animPage = self.matPage.attachNewNode('animPage')
        self.animText = OnscreenText(text='Toon Animation', parent=self.animPage, font=self.mickeyFont,fg=(1,0,0,1), pos=(0, .33),
                                      scale=.069)
        self.animPage.hide()

        animString = OnscreenText(text="Animation Name", pos=(-0.1, 0.20), scale=0.03, align=TextNode.ACenter,
                                  mayChange=1, font=self.toonFont, parent=self.animPage)
        animEntry = DirectEntry(text="", scale=.04, command=self.playAnim, parent=self.animPage,
                            numLines=1, focus=1, pos=(-0.25, 0, 0.25))


        # MAKE-A-TOON PAGES #
        self.matPages = [
            self.speciesPage,
            self.limbPage,
            self.colorPage,
            self.outfitPage,
            self.animPage
        ]

        self.accept('f2', self.toggleGUI)

        self.toggleGUI()

        base.oobe()

    def toggleGUI(self):
        if self.editing:
            self.mainFrame.hide()
            self.rightPageButton.hide()
            self.leftPageButton.hide()
            self.editing = False
        else:
            self.mainFrame.show()
            self.rightPageButton.show()
            self.leftPageButton.show()
            self.editing = True

    def changePage(self, flip):
        self.matPageNum += flip
        if self.matPageNum == 0:
            self.leftPageButton["state"] = DGG.DISABLED
        else:
            self.leftPageButton["state"] = DGG.NORMAL
        if self.matPageNum == len(self.matPages) - 1:
            self.rightPageButton["state"] = DGG.DISABLED
        else:
            self.rightPageButton["state"] = DGG.NORMAL

        for page in self.matPages:
            page.hide()
        self.matPages[self.matPageNum].show()

    def changeLegs(self, legs):
        if legs == 's':
            self.dna = self.toon.style
            self.dna.legs = 's'
        elif legs == 'm':
            self.dna = self.toon.style
            self.dna.legs = 'm'
        elif legs == 'l':
            self.dna = self.toon.style
            self.dna.legs = 'l'
        self.updateToon()

    def setShirt(self, index):
        self.dna = self.toon.style
        self.dna.topTex = int(index)
        self.updateToon()

    def setShirtColor(self, index):
        self.dna = self.toon.style
        self.dna.topTexColor = int(index)
        self.updateToon()

    def setSleeve(self, index):
        self.dna = self.toon.style
        self.dna.sleeveTex = int(index)
        self.updateToon()

    def setSleeveColor(self, index):
        self.dna = self.toon.style
        self.dna.sleeveTexColor = int(index)
        self.updateToon()

    def setBottom(self, index):
        self.dna = self.toon.style
        self.dna.botTex = int(index)
        self.updateToon()

    def setBottomColor(self, index):
        self.dna = self.toon.style
        self.dna.botTexColor = int(index)
        self.updateToon()

    def playAnim(self, anim):
        self.toon.loop(anim)

    def changeTorso(self, torso):
        if torso == 's':
            self.dna = self.toon.style
            self.dna.torso = 'ss'
            self.dna.gender = 'm'
        elif torso == 'm':
            self.dna = self.toon.style
            self.dna.torso = 'ms'
            self.dna.gender = 'm'
        elif torso == 'l':
            self.dna = self.toon.style
            self.dna.torso = 'ls'
            self.dna.gender = 'm'
        elif torso == 'd':
            self.dna = self.toon.style
            self.dna.torso = 'md'
            self.dna.gender = 'f'
        elif torso == 'k':
            self.dna = self.toon.style
            self.dna.torso = 'sd'
            self.dna.gender = 'f'
        elif torso == 'j':
            self.dna = self.toon.style
            self.dna.torso = 'ld'
            self.dna.gender = 'f'
        self.updateToon()

    def changeSpecies(self, species):
        if species == 'dog':
            self.dna = self.toon.style
            self.dna.head = 'dss'
        elif species == 'cat':
            self.dna = self.toon.style
            self.dna.head = 'css'
        elif species == 'monkey':
            self.dna = self.toon.style
            self.dna.head = 'pss'
        elif species == 'mouse':
            self.dna = self.toon.style
            self.dna.head = 'mss'
        elif species == 'pig':
            self.dna = self.toon.style
            self.dna.head = 'sss'
        elif species == 'horse':
            self.dna = self.toon.style
            self.dna.head = 'hss'
        elif species == 'bear':
            self.dna = self.toon.style
            self.dna.head = 'bss'
        elif species == 'duck':
            self.dna = self.toon.style
            self.dna.head = 'fss'
        elif species == 'rabbit':
            self.dna = self.toon.style
            self.dna.head = 'rss'
        elif species == 'crocodile':
            self.dna = self.toon.style
            self.dna.head = 'ass'
        self.updateToon()

    def changeColor(self, furColor):
        self.dna = self.toon.style
        self.dna.headColor = furColor
        self.dna.armColor = furColor
        self.dna.legColor = furColor
        self.updateToon()

    def updateToon(self):
        self.toon.delete()
        self.toon = None

        self.toon = Toon.Toon()
        self.toon.setDNA(self.dna)
        self.toon.reparentTo(render)
        self.toon.loop('neutral')