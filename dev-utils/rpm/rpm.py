import stat
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import *
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.18.1"]:
            self.targets[ver] = f"https://ftp.osuosl.org/pub/rpm/releases/rpm-{'.'.join(ver.split('.')[:2])}.x/rpm-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"rpm-{ver}"

        self.targetDigests["4.18.1"] = (["37f3b42c0966941e2ad3f10fde3639824a6591d07197ba8fd0869ca0779e1f56"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "4.18.1"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["libs/nss"] = None
        self.buildDependencies["libs/lua"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)

        self.subinfo.options.configure.autoreconf = False

    def compile(self):
        env = {
            "LDFLAGS": "-Wl,--copy-dt-needed-entries",
        }
        with utils.ScopedEnv(env):
            return super().compile()
