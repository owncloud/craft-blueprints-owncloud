import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "AppImageUpdate lets you update AppImages in a decentral way using information embedded in the AppImage itself."

        for ver in ["2.0.0-alpha-1-20220124"]:
            self.targets[ver] = f"https://github.com/AppImage/AppImageUpdate/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"AppImageUpdate-{ver}"

        self.targetDigests["2.0.0-alpha-1-20220124"] = (
            ["d1b9edea302b982fd1d3be4783d3cd6d3ebe0c6c7e284b73abc20925d0e1e246"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "2.0.0-alpha-1-20220124"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/zsync2"] = None
        self.runtimeDependencies["libs/libappimage-minimal"] = None
        self.runtimeDependencies["libs/cpr"] = None
        self.runtimeDependencies["libs/argagg"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += [
            "-DUSE_SYSTEM_ZSYNC2=ON",
            "-DUSE_SYSTEM_LIBAPPIMAGE=ON",
            "-DBUILD_QT_UI=ON",
            "-DBUILD_TESTING=OFF",
        ]
