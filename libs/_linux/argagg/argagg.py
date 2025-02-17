import info
from Package.CMakePackageBase import *
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "A simple C++11 command line argument parser"

        for ver in ["0.4.3"]:
            self.targets[ver] = f"https://github.com/vietjtnguyen/argagg/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"argagg-{ver}"

        self.targetDigests["0.4.3"] = (
            ["0ced3ccdda7deb776137a4f1c119ae6f0d1304893ab7421c1ebd9ce020de7a52"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "0.4.3"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += ["-DARGAGG_BUILD_EXAMPLES=OFF", "-DARGAGG_BUILD_TESTS=OFF", "-DARGAGG_BUILD_DOCS=OFF"]
