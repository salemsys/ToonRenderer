import os
import time

from panda3d.core import *

loadPrcFile("config/default/Config.prc")

from direct.showbase import ShowBase
base = ShowBase.ShowBase()
from direct.showbase import DirectObject
from toon.MakeAToon import *

class StartGame(DirectObject):
    def __init__(self):
        self.accept('f9', self.takeScreenShot)
        MakeAToon()

    def takeScreenShot(self):
        if not os.path.exists('screenshots/'):
            os.mkdir('screenshots/')

        namePrefix = '%s%s-%s.png' % (
        'screenshots/', 'renderer', str(int(time.time())))
        base.graphicsEngine.renderFrame()
        screenshot = base.screenshot(
            namePrefix = namePrefix,
            defaultFilename = 0
        )

        pandafile = Filename(str(ExecutionEnvironment.getCwd()) + '/' + str(screenshot))
        global filePath
        filePath = pandafile.toOsSpecific()
        self.lastScreenShotTime = globalClock.getRealTime()
        return

StartGame()
base.run()

