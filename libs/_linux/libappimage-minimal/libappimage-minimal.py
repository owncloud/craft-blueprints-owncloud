import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Implements functionality for dealing with AppImage files. Minimal build variant."

        for ver in ["1.0.4-3"]:
            self.targets[ver] = f"https://github.com/AppImage/libappimage/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libappimage-{ver}"

        self.targetDigests["1.0.4-3"] = (
             ["3ed38d08338b66137cf56a3ba3cdd3ef26dfa75dfa6ca02e7faa74f7683dbc12"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "1.0.4-3"

    def setDependencies(self):
        pass

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += [
            "-DBUILD_TESTING=OFF",
            "-DLIBAPPIMAGE_SHARED_ONLY=ON",
        ]
