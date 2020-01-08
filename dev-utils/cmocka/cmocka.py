import info
import os
import shutil

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.1.5"]:
            self.targets[ver] = f"https://cmocka.org/files/1.1/cmocka-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"cmocka-{ver}"

        self.targetDigests["1.1.5"] = (['f0ccd8242d55e2fd74b16ba518359151f6f8383ff8aef4976e48393f77bba8b6'], CraftHash.HashAlgorithm.SHA256)
        self.description = "unit testing framework for C."
        self.webpage = "https://cmocka.org/"
        self.defaultTarget = '1.1.5'

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None

class Package(CMakePackageBase):
    pass