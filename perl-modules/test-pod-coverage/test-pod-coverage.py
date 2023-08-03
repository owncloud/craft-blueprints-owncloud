# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None

    def setTargets(self):
        for ver in ["1.10"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/N/NE/NEILB/Test-Pod-Coverage-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Test-Pod-Coverage-{ver}"
        self.targetDigests["1.10"] = (["48c9cca9f7d99eee741176445b431adf09c029e1aa57c4703c9f46f7601d40d4"], CraftHash.HashAlgorithm.SHA256)

        self.tags = "Config-File"
        self.defaultTarget = "1.10"


class Package(PerlPackageBase):
    def __init__(self, **args):
        PerlPackageBase.__init__(self)
