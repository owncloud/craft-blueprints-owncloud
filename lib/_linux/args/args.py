import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "A simple header-only C++ argument parser library."

        for ver in ["6.3.0"]:
            self.targets[ver] = f"https://github.com/Taywee/args/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"args-{ver}"

        self.targetDigests["6.3.0"] = (
            ["e072c4a9d6990872b0ecb45480a5487db82e0dc3d27c3c3eb9fc0930c0d796ae"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "6.3.0"


class Package(CMakePackageBase):
    pass
