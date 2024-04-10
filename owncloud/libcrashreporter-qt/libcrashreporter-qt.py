import configparser
import glob
import io
import os
import re
import subprocess
import sys

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/dschmidt/libcrashreporter-qt.git"
        self.patchLevel["master"] = 3
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["dev-utils/cmake"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        if CraftCore.compiler.isLinux:
            self.buildDependencies["dev-utils/breakpad"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.fetch.checkoutSubmodules = not CraftCore.compiler.isLinux
