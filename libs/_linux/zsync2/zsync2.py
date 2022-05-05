import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Partial/differential file download client over HTTP(S)"

        for ver in ["2.0.0-alpha-1-20220505"]:
            self.targets[ver] = f"https://github.com/AppImage/zsync2/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"zsync2-{ver}"

        self.targetDigests["2.0.0-alpha-1-20220505"] = (
            ["43057b5d6ded0736cb3cece5d955f2e6fd3ab04e6f6577292f8bb1f4326af8ac"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "2.0.0-alpha-1-20220505"

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
