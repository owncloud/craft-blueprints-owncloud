import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Libgcrypt is a general purpose cryptographic library originally based on code from GnuPG."

        # 1.8.10 is an LTS version
        for ver in ["1.8.10"]:
            self.targets[ver] = f"https://gnupg.org/ftp/gcrypt/libgcrypt/libgcrypt-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libgcrypt-{ver}"

        self.targetDigests["1.8.10"] = (
            ["6896915501f951e23d02dcb0453469c2cc22aa4d77a001ff73a2647c2d29e7dd"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "1.8.10"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
