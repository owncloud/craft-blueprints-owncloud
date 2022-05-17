import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Partial/differential file download client over HTTP(S)"

        for ver in ["2.0.0-alpha-1-20220517"]:
            self.targets[ver] = f"https://github.com/AppImage/zsync2/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"zsync2-{ver}"

        self.targetDigests["2.0.0-alpha-1-20220517"] = (
            ["d213063d6c5c951a394771cc3e700ef9f07ebcbd381480661c29b62f4d4743bf"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "2.0.0-alpha-1-20220517"

    def setDependencies(self):
        self.runtimeDependencies["libs/cpr"] = None
        self.runtimeDependencies["libs/args"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += [
            "-DUSE_SYSTEM_CPR=ON",
            "-DUSE_SYSTEM_ARGS=ON",
            "-DBUILD_TESTING=OFF",
        ]
