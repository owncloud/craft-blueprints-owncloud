# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None
        self.runtimeDependencies["perl-modules/test-pod"] = None
        self.runtimeDependencies["perl-modules/test-pod-coverage"] = None

    def setTargets(self):
        for ver in ["0.4234"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Module-Build-{ver}"
        self.targetDigests["0.4234"] = (["66aeac6127418be5e471ead3744648c766bd01482825c5b66652675f2bc86a8f"], CraftHash.HashAlgorithm.SHA256)

        self.tags = "Config-File"
        self.defaultTarget = "0.4234"


class Package(PerlPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
