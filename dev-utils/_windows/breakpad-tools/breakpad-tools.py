import info
import os
import shutil

from Package.MSBuildPackageBase import *

class subinfo(info.infoclass):
    """We use Jon Turney's fork which adds support for MinGW and a python script to fetch deps"""
    def setTargets(self):
        for ver in ["pecoff-dwarf-on-git-20171117-fetch-externals-on-win"]:
            self.svnTargets[ver] = f"[git]https://github.com/dschmidt/google-breakpad|{ver}|"

        self.defaultTarget = 'pecoff-dwarf-on-git-20171117-fetch-externals-on-win'
        self.description = "The tools part of the breakpad crash-reporting system."
        self.webpage = "https://github.com/dschmidt/google-breakpad"

    def setDependencies(self):
        self.buildDependencies["dev-utils/python2"] = "default"

class Package(MSBuildPackageBase):
    def __init__(self):
        MSBuildPackageBase.__init__(self)
        self.useShadowBuild = True
        self.subinfo.options.configure.projectFile = os.path.join('src', 'tools', 'windows', "build_all.vcxproj")

    def fetch(self):
        if not super().fetch():
            return False

        utils.system(["python2", "fetch-externals"], cwd=self.sourceDir())

        # Remove binaries that are shipped in source
        binariesPath = os.path.join(self.sourceDir(), 'src', 'tools', 'windows', 'binaries')
        if os.path.isdir(binariesPath):
            shutil.rmtree(binariesPath)

        return True

    def configure(self):
        gypMain = os.path.join(self.sourceDir(), 'src', 'tools', 'gyp', 'gyp_main.py')
        gypFile = os.path.join(self.sourceDir(), 'src', 'tools', 'windows', 'tools_windows.gyp')

        # Out of source generation seems broken in gyp with msvs generator, ninja generator failed to generate the project files
        # There should be no reason to use the one or the other, if ninja works one day and msvs still does not - feel free to switch
        depth = os.path.join(self.sourceDir(), 'src')
        cwd = depth

        # WORKAROUND: Visual Studio Detection is broken in containers
        env = os.environ.copy()
        msvcString = CraftCore.compiler.abi.split("_")[0]
        msvcVersion = msvcString[4:]
        env["GYP_MSVS_VERSION"] = msvcVersion

        utils.system(['python2', gypMain, '--no-circular-check', gypFile, '-f', 'msvs', '--generator-output=%s' % self.buildDir(), '--depth=%s' % depth], cwd=cwd, env=env)

        MSBuildPackageBase.configure(self)
        return True

    # def unittest(self):
        # buildType = 'Release'
        # dumpSymsUnitTestFile = os.path.join(self.sourceDir(), 'src', 'tools', 'windows', 'dump_syms', 'Release', 'dump_syms_unittest.exe')
        # utils.system(dumpSymsUnitTestFile)

    def install(self):
        # 1) symbol testdata is contained in folders named .pdb which causes issues with craft
        # Should we modify craft to glob only for .pdb files and no folders?
        # 2) dump_syms testdata contains files that we can't but don't want to install
        testdataPaths = [os.path.join('src', 'processor', 'testdata'), os.path.join('src', 'tools', 'windows', 'dump_syms', 'testdata')]

        for path in testdataPaths:
            testSymbolsPath = os.path.join(self.sourceDir(), path)
            if os.path.isdir(testSymbolsPath):
                shutil.rmtree(testSymbolsPath)

        return MSBuildPackageBase.install(self, installHeaders=False)
