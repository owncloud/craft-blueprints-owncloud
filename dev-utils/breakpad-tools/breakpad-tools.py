import info
import os
import shutil

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def registerOptions(self):
        if CraftCore.compiler.isMinGW():
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        for ver in ["pecoff-dwarf-on-git-20171117", "pecoff-dwarf-on-git-20171117-fetch-externals-on-win"]:
            self.svnTargets[ver] = f"[git]https://github.com/dschmidt/google-breakpad|{ver}|"
            self.patchToApply[ver] = [("0001-Add-CMake-script-to-build-dump_syms.patch", 1),
                                       ("Fix-mac-build.patch", 1)]

        for ver in ["cmake"]:
            self.svnTargets[ver] = f"[git]https://github.com/theonering/google-breakpad|{ver}|"
            self.targetSrcSuffix[ver] = "theonering"

        self.svnTargets["master"] = "https://github.com/google/breakpad.git"
        self.targetSrcSuffix["master"] = "upstream"
        self.patchToApply["master"] = [("breakpad-tools-20191106.patch", 1)]

        self.description = "The tools part of the breakpad crash-reporting system."
        self.webpage = "https://github.com/jon-turney/google-breakpad"
        self.defaultTarget = 'cmake'

    def setDependencies(self):
        self.buildDependencies["dev-utils/python2"] = None
        self.buildDependencies["virtual/base"] = None

class Package(CMakePackageBase):
    def fetch(self):
        if not super().fetch():
            return False
        return utils.system(["python2", "fetch-externals"], cwd=self.sourceDir())