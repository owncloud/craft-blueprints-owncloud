import stat
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.7.0"]:
            self.targetInstallPath[ver] = "dev-utils/bin"
            if CraftCore.compiler.isWindows:
                self.targets[ver] = f"https://github.com/getsentry/symbolicator/releases/download/0.7.0/symsorter-Windows-x86_64.exe"
                self.targetDigests["0.7.0"] = (["08d9fe1cd902dabdf0f37be88f482bb1cd614e17a98481fe5011288bbe8c09d1"], CraftHash.HashAlgorithm.SHA256)
            elif CraftCore.compiler.isMacOS:
                self.targets[ver] = f"https://github.com/getsentry/symbolicator/releases/download/0.7.0/symsorter-Darwin-universal"
            elif CraftCore.compiler.isLinux:
                # sysmsorter is a rust binary and we need a build on centos7...
                self.targets[ver] = f"https://download.owncloud.com/desktop/craft/symsorter/symsorter.7z"
                self.targetDigests["0.7.0"] = (["4665df5b6f0d2b59f28deae5ffebe68de677406b0c965b87ea6d54940187614d"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.7.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        if not super().install():
            return False
        dest = self.installDir() / f"symsorter{CraftCore.compiler.executableSuffix}"
        if not dest.exists():
            # in case we directly downloaded a binary move it
            if not utils.copyFile(self.sourceDir() / Path(self.subinfo.target()).name, dest):
                return False
        if CraftCore.compiler.isUnix:
            dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return True
