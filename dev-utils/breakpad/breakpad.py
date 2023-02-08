import info
import os
import shutil

from Package.CMakePackageBase import *
from Package.AutoToolsPackageBase import AutoToolsPackageBase

class subinfo(info.infoclass):

    def setTargets(self):
        if not CraftCore.compiler.isLinux:
            for ver in ["pecoff-dwarf-on-git-20171117", "pecoff-dwarf-on-git-20171117-fetch-externals-on-win"]:
                self.svnTargets[ver] = f"[git]https://github.com/dschmidt/google-breakpad|{ver}|"
                self.patchToApply[ver] = [("0001-Add-CMake-script-to-build-dump_syms.patch", 1),
                                        ("Fix-mac-build.patch", 1)]

            for ver in ["cmake"]:
                self.svnTargets[ver] = f"[git]https://github.com/theonering/google-breakpad|{ver}|"
                self.targetSrcSuffix[ver] = "theonering"

            self.svnTargets["master"] = "https://github.com/google/breakpad.git"
            self.targetSrcSuffix["master"] = "upstream"
            self.defaultTarget = 'cmake'
        else:
            # not actually used as we use depot-tools
            for ver in ["v2022.07.12"]:
                self.svnTargets[ver] = f"https://chromium.googlesource.com/breakpad/breakpad||{ver}"
                self.targetSrcSuffix[ver] = "upstream"
                self.targetInstSrc[ver] = "src"
                self.defaultTarget = ver

        self.description = "The tools part of the breakpad crash-reporting system."
        self.webpage = "https://github.com/jon-turney/google-breakpad"

    def setDependencies(self):
        if  CraftCore.compiler.isMSVC():
            self.buildDependencies["dev-utils/python2"] = None
        else:
            self.buildDependencies["dev-utils/depot-tools"] = None
        self.buildDependencies["virtual/base"] = None

if CraftCore.compiler.isLinux:
    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            AutoToolsPackageBase.__init__(self)

        def fetch(self):
            depot_tools = CraftPackageObject.get("dev-utils/depot-tools").instance.sourceDir()
            srcParent = self.sourceDir().parent
            if not srcParent.exists():
                return utils.createDir(srcParent) and utils.system([ depot_tools/ "fetch", "--no-history", "breakpad"], cwd=srcParent)
            return utils.system([ depot_tools/ "gclient", "sync"], cwd=srcParent)

else:
    class Package(CMakePackageBase):
        def fetch(self):
            if not super().fetch():
                return False
            return utils.system(["python2", "fetch-externals"], cwd=self.sourceDir())
