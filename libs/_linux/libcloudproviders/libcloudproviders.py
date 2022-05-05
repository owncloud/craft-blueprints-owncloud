import info
from Package.MesonPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "DBus API that allows cloud storage sync clients to expose their services"

        for ver in ["0.3.1"]:
            self.targets[ver] = f"https://gitlab.gnome.org/World/libcloudproviders/-/archive/0.3.1/libcloudproviders-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libcloudproviders-{ver}"

        self.targetDigests["0.3.1"] = (
            ["de4aa746c1695f30fcd3b52a4a6ee149ce567a2f7e185499bf2963f77dd1bad0"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "0.3.1"

    def setDependencies(self):
        self.runtimeDependencies["libs/glib"] = None


class Package(MesonPackageBase):
    def __init__(self, **args):
        MesonPackageBase.__init__(self)
