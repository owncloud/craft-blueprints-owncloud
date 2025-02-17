import info
from Package.CMakePackageBase import *
from Utils import CraftHash

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Implementation of the FreeDesktop specifications to be used in c++ projects"

        for ver in ["1.0.1"]:
            self.targets[ver] = f"https://github.com/azubieta/xdg-utils-cxx/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"xdg-utils-cxx-{ver}"

        self.targetDigests["1.0.1"] = (
            ["2cdeda2385faa0ce496a5b276f5145f2dfb3f67ee77789cf8f57752abc83e69b"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "1.0.1"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += [
            "-DXDG_UTILS_SHARED=ON",
        ]
