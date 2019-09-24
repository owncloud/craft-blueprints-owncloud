import info
import os

import io
import re
import sys
import subprocess

class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.registerOption("buildVfsWin", False)

    def setTargets(self):
        self.versionInfo.setDefaultValues(tarballUrl="https://download.owncloud.com/desktop/stable/owncloudclient-${VERSION}.tar.xz",
                                          tarballInstallSrc="owncloudclient-${VERSION}",
                                          gitUrl="[git]https://github.com/owncloud/client")

        self.description = "ownCloud Desktop Client"
        self.displayName = "ownCloud"
        self.webpage = "https://owncloud.org"

    def setDependencies(self):
        self.buildDependencies["craft/craft-blueprints-owncloud"] = None
        self.buildDependencies["dev-utils/cmake"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/breakpad-tools"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtmacextras"] = None
        self.runtimeDependencies["libs/qt5/qttranslations"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = None
        self.runtimeDependencies["libs/qt5/qtwebkit"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None
        if self.options.dynamic.buildVfsWin:
            self.runtimeDependencies["owncloud/client-plugin-vfs-win"] = None



from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True
        # Pending PR to move to standard BUILD_TESTING: https://github.com/owncloud/client/pull/6917#issuecomment-444845521
        self.subinfo.options.configure.args = "-DUNIT_TESTING={testing} ".format(testing="ON" if self.buildTests else "OFF")

        if 'OWNCLOUD_CMAKE_PARAMETERS' in os.environ:
                self.subinfo.options.configure.args += os.environ['OWNCLOUD_CMAKE_PARAMETERS']
        if self.subinfo.options.dynamic.buildVfsWin:
            self.win_vfs_plugin = CraftPackageObject.get("owncloud/client-plugin-vfs-win")
            self.subinfo.options.configure.args += f" -DVIRTUAL_FILE_SYSTEM_PLUGINS={self.win_vfs_plugin.instance.sourceDir()}"

    @property
    def applicationExecutable(self):
        return os.environ.get('ApplicationExecutable', 'owncloud')

    def fetch(self):
        if self.subinfo.options.dynamic.buildVfsWin:
            if not self.win_vfs_plugin.instance.fetch():
                return False
        return super().fetch()

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isWindows:
            # ensure we can find the sync-exclude.lst
            configDir = Path(self.installDir()) / "config" / self.applicationExecutable
            if configDir.exists():
                if not utils.mergeTree(configDir, Path(self.installDir()) / "bin"):
                    return False
        return True

    def symbolsDir(self):
        return os.path.join(self.imageDir(), 'symbols')

    # Loosely based on https://chromium.googlesource.com/chromium/chromium/+/34599b0bf7a14ab21a04483c46ecd9b5eaf86704/components/breakpad/tools/generate_breakpad_symbols.py#92
    def dumpSymbols(self, binaryFile) -> bool:
        if re.match(r"icudt\d\d.dll", os.path.basename(binaryFile)):
            CraftCore.log.warning(f'dump_symbols: {binaryFile} is blacklisted because it has no symbols')
            return False

        CraftCore.log.info('Dump symbols for: %s' % binaryFile)

        realpath = os.path.realpath(binaryFile)
        with io.BytesIO() as out:
            utils.system(['dump_syms', realpath], stdout=out)
            outBytes = out.getvalue()

        firstLine = str(outBytes.splitlines()[0], 'utf-8')
        CraftCore.log.info('Module line: %s' % firstLine)

        if firstLine.startswith("loadDataForPdb and loadDataFromExe failed for"):
            CraftCore.log.warning(f"Module does not contain debug symbols: {binaryFile}")
            return False

        regex = "^MODULE [^ ]+ [^ ]+ ([0-9aA-fF]+) (.*)"
        CraftCore.log.debug('regex: %s' % regex)
        moduleLine = re.match(regex, firstLine)
        CraftCore.log.debug('regex: %s' % moduleLine)
        outputPath = os.path.join(self.symbolsDir(), moduleLine.group(2),
                             moduleLine.group(1))

        os.makedirs(outputPath, exist_ok=True)

        symbolFileBasename = moduleLine.group(2).replace(".pdb", "")
        symbolFile = os.path.join(outputPath, "%s.sym" % symbolFileBasename)
        with open(symbolFile, 'wb') as outputFile:
            outputFile.write(outBytes)
        CraftCore.log.info('Writing symbols to: %s' % symbolFile)
        return True

    def createPackage(self):
        self.defines["appname"] = self.applicationExecutable
        self.defines["shortcuts"] = [{"name" : self.subinfo.displayName , "target" : f"bin/{self.defines['appname']}{CraftCore.compiler.executableSuffix}", "description" : self.subinfo.description}]
        self.defines["icon"] = Path(self.buildDir()) / "src/gui/owncloud.ico"


        self.blacklist.append(re.compile(r"bin[/|\\](?!" + self.applicationExecutable + r").*\.exe"))

        self.ignoredPackages += ["binary/mysql"]
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages += ["libs/dbus"]

        if os.environ.get('ENABLE_CRASHREPORTS', "False") == 'True':
            sep = '\\%s' % os.sep
            regex = r"symbols%s.*" % sep
            self.whitelist.append(re.compile(regex))
        else:
            CraftCore.log.info('ENABLE_CRASHREPORTS is not active. Not dumping symbols.')

        return super().createPackage()

    def preArchive(self):
        if os.environ.get('ENABLE_CRASHREPORTS', "False") == 'True':
            for f in utils.filterDirectoryContent(self.archiveDir(),
                                                  whitelist=lambda x, root: utils.isBinary(os.path.join(root, x)),
                                                  blacklist=lambda x, root: True):
                self.dumpSymbols(f)
        return super().preArchive()

    # Forked from CMakeBuildSystem.py to add exclusion regex
    def unittest(self):
        """running cmake based unittests"""
        # TODO: add options.unittest.args

        self.enterBuildDir()

        command = ["ctest", "--output-on-failure", "--timeout", "300"]

        command += ["--exclude-regex", "WinVfsTest"]

        if CraftCore.debug.verbose() == 1:
            command += ["-V"]
        elif CraftCore.debug.verbose() > 1:
            command += ["-VV"]
        return utils.system(command)

