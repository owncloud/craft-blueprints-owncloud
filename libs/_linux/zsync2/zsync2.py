import info
from Package.CMakePackageBase import *
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Partial/differential file download client over HTTP(S)"

        self.svnTargets["master"] = "https://github.com/AppImageCommunity/zsync2.git|master|"

        for ver in ["2.0.0-alpha-1-20230304"]:
            self.targets[ver] = f"https://github.com/AppImageCommunity/zsync2/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"zsync2-{ver}"

        self.targetDigests["2.0.0-alpha-1-20230304"] = (
            ["8d0652b92a29783dd04ccf7d0b475341bedef8f7b45e69f8d667bbaa41beedb2"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "2.0.0-alpha-1-20230304"

    def setDependencies(self):
        self.runtimeDependencies["libs/cpr"] = None
        self.runtimeDependencies["libs/args"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            "-DUSE_SYSTEM_CPR=ON",
            "-DUSE_SYSTEM_ARGS=ON",
            "-DBUILD_TESTING=OFF",
        ]
