import os
import shutil

import info
from CraftCore import CraftCore
from Package.SourceOnlyPackageBase import SourceOnlyPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Linux

    def setTargets(self):
        for ver in ["chrome/4147", "main"]:
            self.svnTargets[ver] = f"https://chromium.googlesource.com/chromium/tools/depot_tools.git|{ver}|"

        self.webpage = "https://dev.chromium.org/developers/how-tos/depottools"
        self.defaultTarget = "chrome/4147"

    def setDependencies(self):
        self.buildDependencies["dev-utils/system-python3"] = None
        self.buildDependencies["virtual/base"] = None


class Package(SourceOnlyPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
