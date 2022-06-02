import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Partial/differential file download client over HTTP(S)"

        for ver in ["2.0.0-alpha-1-20220602"]:
            self.targets[ver] = f"https://github.com/AppImage/zsync2/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"zsync2-{ver}"

        self.targetDigests["2.0.0-alpha-1-20220602"] = (
            ["6e25905fa4fc3ce387c42d78a99f002c5721f3ba5fa657c77968e29bba254e26"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "2.0.0-alpha-1-20220602"

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
