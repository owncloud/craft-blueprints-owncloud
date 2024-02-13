import os
import shutil

import info
import utils
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import *
from Package.MakeFilePackageBase import MakeFilePackageBase
from Package.MSBuildPackageBase import MSBuildPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Linux

    def setTargets(self):
        for ver in ["v2022.07.12"]:
            self.svnTargets[ver] = f"https://chromium.googlesource.com/breakpad/breakpad||{ver}"
            self.targetSrcSuffix[ver] = "upstream"
            self.targetInstSrc[ver] = "src"
            self.defaultTarget = ver

        self.patchToApply["v2022.07.12"] = [("0001-No-werror.patch", 1)]
        self.patchLevel["v2022.07.12"] = 1

        self.description = "The tools part of the breakpad crash-reporting system."
        self.webpage = "https://github.com/jon-turney/google-breakpad"

    def setDependencies(self):
        self.buildDependencies["dev-utils/depot-tools"] = None
        if CraftCore.compiler.isLinux:
            self.buildDependencies["libs/elfutils"] = None
        self.buildDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)

    def fetch(self):
        depot_tools = CraftPackageObject.get("dev-utils/depot-tools").instance.sourceDir()
        srcParent = self.sourceDir().parent
        scriptSuffix = ".bat" if CraftCore.compiler.isWindows else ""
        if not srcParent.exists():
            if not (utils.createDir(srcParent) and utils.system([depot_tools / f"fetch{scriptSuffix}", "--no-history", "breakpad"], cwd=srcParent)):
                return False
        if not (utils.system(["git", "clean", "-xdf"], cwd=self.sourceDir()) and utils.system(["git", "reset", "--hard"], cwd=self.sourceDir())):
            return False
        if not utils.system([depot_tools / f"gclient{scriptSuffix}", "sync", "--revision", self.buildTarget], cwd=srcParent):
            return False
        for patch, lvl in self.subinfo.patchesToApply():
            if not utils.applyPatch(self.sourceDir(), self.blueprintDir() / patch, lvl):
                return False
        return True

    def unpack(self):
        return True
