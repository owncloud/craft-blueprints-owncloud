import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Implements functionality for dealing with AppImage files. Minimal build variant."

        for ver in ["1.0.4-5"]:
            self.targets[ver] = f"https://github.com/AppImage/libappimage/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libappimage-{ver}"

        self.targetDigests["1.0.4-5"] = (
            ["2c4e18860a790c5959da6eb064cbd07f165fe6a9b15989491a3a3f176d06af31"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "1.0.4-5"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            "-DBUILD_TESTING=OFF",
            "-DLIBAPPIMAGE_SHARED_ONLY=ON",
        ]
