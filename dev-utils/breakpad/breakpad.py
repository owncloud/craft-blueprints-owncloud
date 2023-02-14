import os
import shutil

import info
import utils
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import *
from Package.MakeFilePackageBase import MakeFilePackageBase
from Package.MSBuildPackageBase import MSBuildPackageBase


class subinfo(info.infoclass):
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

    def _fetch(self, package):
        depot_tools = CraftPackageObject.get("dev-utils/depot-tools").instance.sourceDir()
        srcParent = package.sourceDir().parent
        scriptSuffix = ".bat" if CraftCore.compiler.isWindows else ""
        if not srcParent.exists():
            if not (utils.createDir(srcParent) and utils.system([depot_tools / f"fetch{scriptSuffix}", "--no-history", "breakpad"], cwd=srcParent)):
                return False
        if not (utils.system(["git", "clean", "-xdf"], cwd=package.sourceDir()) and utils.system(["git", "reset", "--hard"], cwd=package.sourceDir())):
            return False
        if not utils.system([depot_tools / f"gclient{scriptSuffix}", "sync", "--revision", self.buildTarget], cwd=srcParent):
            return False
        for patch, lvl in self.patchesToApply():
            if not utils.applyPatch(package.sourceDir(), package.packageDir() / patch, lvl):
                return False
        return True

    def _configure(self, package):
        depot_tools = CraftPackageObject.get("dev-utils/depot-tools").instance.sourceDir()
        srcParent = package.sourceDir().parent
        scriptSuffix = ".bat" if CraftCore.compiler.isWindows else ""
        if not utils.system([depot_tools / f"gclient{scriptSuffix}", "runhooks"], cwd=srcParent):
            return False
        return True


if CraftCore.compiler.isLinux:

    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            AutoToolsPackageBase.__init__(self)

        def fetch(self):
            return self.subinfo._fetch(self)

        def unpack(self):
            return True

elif CraftCore.compiler.isWindows:

    class Package(MSBuildPackageBase):
        def __init__(self, **args):
            MSBuildPackageBase.__init__(self)
            self.subinfo.options.configure.projectFile = self.sourceDir() / "src/tools/windows/dump_syms/dump_syms.sln"
            self.msbuildTargets = ["Clean", "Build"]

        def fetch(self):
            return self.subinfo._fetch(self)

        def unpack(self):
            return True

        def configure(self):
            with utils.ScopedEnv({"GYP_MSVS_VERSION": "2015"}):
                return self.subinfo._configure(self)

        def install(self):
            if not BuildSystemBase.install(self):
                return False
            return utils.copyFile(self.sourceDir() / "src/tools/windows/dump_syms/Release/dump_syms.exe", self.installDir() / "bin/dump_syms.exe")

else:

    class Package(MakeFilePackageBase):
        def __init__(self, **args):
            MakeFilePackageBase.__init__(self)

        def fetch(self):
            return self.subinfo._fetch(self)

        def unpack(self):
            return True

        def configure(self):
            return self.subinfo._configure(self)

        def make(self):
            return utils.system(
                [
                    "xcodebuild",
                    "-configuration",
                    "Release",
                    "-target",
                    "dump_syms",
                    "-project",
                    self.sourceDir() / "src/tools/mac/dump_syms/dump_syms.xcodeproj",
                ]
            )

        def install(self):
            if not BuildSystemBase.install(self):
                return False
            return utils.copyFile(self.sourceDir() / "src/tools/mac/dump_syms/build/Release/dump_syms", self.installDir() / "bin/dump_syms")
