import io
import os
import re

import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.registerOption("buildWithQt6", False)

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/KDAB/KDSingleApplication.git"
        self.defaultTarget = "master"

        self.patchToApply["master"] = [("5.patch", 1)]
        self.patchLevel["master"] = 1

        self.description = "KDSingleApplication is a helper class for single-instance policy applications written by KDAB."
        self.webpage = "https://github.com/KDAB/KDSingleApplication"

    def setDependencies(self):
        self.buildDependencies["craft/craft-blueprints-owncloud"] = None
        if not self.options.dynamic.buildWithQt6:
            self.runtimeDependencies["libs/qt5/qtbase"] = None
        else:
            self.runtimeDependencies["libs/qt6/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        if self.subinfo.options.dynamic.buildWithQt6:
            self.subinfo.options.configure.args += ["-DKDSingleApplication_QT6=ON"]
