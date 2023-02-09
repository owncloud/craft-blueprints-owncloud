import info

import configparser
import os
import io
import re
import sys
import subprocess
import glob

class subinfo(info.infoclass):

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/dschmidt/libcrashreporter-qt.git"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["dev-utils/cmake"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = not CraftCore.compiler.isLinux
