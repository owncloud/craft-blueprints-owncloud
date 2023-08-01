import stat
import os
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import *
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["0.13.1+nmu4"] = f"https://deb.debian.org/debian/pool/main/d/dpkg-sig/dpkg-sig_0.13.1+nmu4.tar.gz"
        self.targetInstSrc["0.13.1+nmu4"] = f"dpkg-sig-0.13.1+nmu2"

        self.targetDigests["0.13.1+nmu4"] = (["7c33d26c371f67e3a0aa658bb925336e8584d43fef9938e16da8da6272f47bc3"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.13.1+nmu4"

    def setDependencies(self):
        self.buildDependencies["dev-utils/perl"] = None


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not super().install():
            return False

        return utils.createShim(os.path.join(self.imageDir(), "bin", "dpkg-sig"), os.path.join(self.imageDir(), "dpkg-sig"))
