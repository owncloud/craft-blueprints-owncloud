import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "AppImageUpdate lets you update AppImages in a decentral way using information embedded in the AppImage itself."

        self.svnTargets["master"] = "https://github.com/AppImageCommunity/AppImageUpdate.git|main|"

        for ver in ["2.0.0-alpha-1-20220512"]:
            self.targets[ver] = f"https://github.com/AppImage/AppImageUpdate/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"AppImageUpdate-{ver}"

        self.targetDigests["2.0.0-alpha-1-20220512"] = (
            ["adbfbb49b6a0ee945ed3cac1909ba9f52173416181aacd7ee1faef844b0c2240"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "2.0.0-alpha-1-20220512"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/zsync2"] = None
        self.runtimeDependencies["libs/libappimage-minimal"] = None
        self.runtimeDependencies["libs/cpr"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += [
            "-DUSE_SYSTEM_ZSYNC2=ON",
            "-DUSE_SYSTEM_LIBAPPIMAGE=ON",
            "-DBUILD_QT_UI=OFF",
            "-DBUILD_TESTING=OFF",
            "-DBUILD_LIBAPPIMAGEUPDATE_ONLY=ON",
        ]
