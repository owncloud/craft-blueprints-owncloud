import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Implements functionality for dealing with AppImage files"

        for ver in ["1.0.4-2"]:
            self.targets[ver] = f"https://github.com/AppImage/libappimage/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libappimage-{ver}"

        self.targetDigests["1.0.4-2"] = (
            ["ad3044a9a41e9446d5d486b61b08236a0083ec455503a876968a3d88be90ccff"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "1.0.4-2"

    def setDependencies(self):
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/squashfuse"] = None
        self.runtimeDependencies["libs/libarchive"] = None
        self.runtimeDependencies["libs/boost/boost-filesystem"] = None
        self.runtimeDependencies["libs/xdg-utils-cxx"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += [
            "-DUSE_SYSTEM_XZ=ON",
            "-DUSE_SYSTEM_SQUASHFUSE=ON",
            "-DUSE_SYSTEM_LIBARCHIVE=ON",
            "-DUSE_SYSTEM_BOOST=ON",
            "-DUSE_SYSTEM_XDGUTILS=ON",
            "-DBUILD_TESTING=OFF",
        ]
