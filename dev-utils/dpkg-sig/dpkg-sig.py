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
        self.targetInstallPath["0.13.1+nmu4"] = "bin"

        self.patchToApply["0.13.1+nmu4"] = [("dpkg-sig-0.13.1+nmu4-20230803.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None
        self.runtimeDependencies["perl-modules/config-file"] = None


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
