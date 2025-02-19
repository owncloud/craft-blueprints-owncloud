# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *
from Utils import CraftHash

class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None

    def setTargets(self):
        for ver in ["1.52"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/E/ET/ETHER/Test-Pod-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Test-Pod-{ver}"
        self.targetDigests["1.52"] = (["60a8dbcc60168bf1daa5cc2350236df9343e9878f4ab9830970a5dde6fe8e5fc"], CraftHash.HashAlgorithm.SHA256)

        self.tags = "Config-File"
        self.defaultTarget = "1.52"


class Package(PerlPackageBase):
    def __init__(self, **args):
        PerlPackageBase.__init__(self)
