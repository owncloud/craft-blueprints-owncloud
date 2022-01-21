import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "C++ Requests: Curl for People, a spiritual port of Python Requests."

        for ver in ["1.7.2"]:
            self.targets[ver] = f"https://github.com/libcpr/cpr/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"cpr-{ver}"

        self.targetDigests["1.7.2"] = (
            ["aa38a414fe2ffc49af13a08b6ab34df825fdd2e7a1213d032d835a779e14176f"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "1.7.2"

    def setDependencies(self):
        self.runtimeDependencies["libs/libcurl"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += ["-DCPR_FORCE_USE_SYSTEM_CURL=ON"]
