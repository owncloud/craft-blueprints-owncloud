import info
from Package.CMakePackageBase import *
from Utils import CraftHash

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "C++ Requests: Curl for People, a spiritual port of Python Requests."

        for ver in ["1.10.5"]:
            self.targets[ver] = f"https://github.com/libcpr/cpr/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"cpr-{ver}"

        self.targetDigests["1.8.3"] = (
            ["0784d4c2dbb93a0d3009820b7858976424c56578ce23dcd89d06a1d0bf5fd8e2"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["1.10.5"] = (
            ["c8590568996cea918d7cf7ec6845d954b9b95ab2c4980b365f582a665dea08d8"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "1.10.5"

    def setDependencies(self):
        self.runtimeDependencies["libs/libcurl"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += ["-DCPR_USE_SYSTEM_CURL=ON"]
