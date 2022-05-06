import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Implements functionality for dealing with AppImage files"

        for ver in ["1.0.4-1"]:
            self.targets[ver] = f"https://github.com/AppImage/libappimage/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libappimage-{ver}"

        self.targetDigests["1.0.4-1"] = (
            ["b03ce735c7672ae01f152be24367844dd0d1111000c34a62d970f83e025fe716"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "1.0.4-1"

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
