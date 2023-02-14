import os
import shutil

import info
from Package.SourceOnlyPackageBase import SourceOnlyPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://chromium.googlesource.com/chromium/tools/depot_tools.git|main|"

        self.webpage = "https://dev.chromium.org/developers/how-tos/depottools"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["dev-utils/python3"] = None
        self.buildDependencies["virtual/base"] = None


class Package(SourceOnlyPackageBase):
    def __init__(self, **args):
        SourceOnlyPackageBase.__init__(self)
