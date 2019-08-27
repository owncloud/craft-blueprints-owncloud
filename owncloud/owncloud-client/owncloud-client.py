import info
import os

import io
import re

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
        self.buildDependencies["craft/craft-blueprints-owncloud"] = "default"
        self.buildDependencies["dev-utils/cmake"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["dev-utils/breakpad-tools"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtmacextras"] = "default"
        self.runtimeDependencies["libs/qt5/qttranslations"] = "default"
        self.runtimeDependencies["libs/qt5/qtsvg"] = "default"
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebkit"] = "default"
        self.runtimeDependencies["qt-libs/qtkeychain"] = "default"

        if self.options.dynamic.buildVfsWin:
            self.runtimeDependencies["owncloud/client-plugin-vfs-win"] = None



from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True

        self.subinfo.options.configure.args += "-DUNIT_TESTING=1 "

        if 'OWNCLOUD_CMAKE_PARAMETERS' in os.environ:
                self.subinfo.options.configure.args += os.environ['OWNCLOUD_CMAKE_PARAMETERS']
        if self.subinfo.options.dynamic.buildVfsWin:
            self.win_vfs_plugin = CraftPackageObject.get("owncloud/client-plugin-vfs-win")
            self.subinfo.options.configure.args += f" -DVIRTUAL_FILE_SYSTEM_PLUGINS={self.win_vfs_plugin.instance.sourceDir()}"

    def fetch(self):
        if self.subinfo.options.dynamic.buildVfsWin:
            if not self.win_vfs_plugin.instance.fetch():
                return False
        return super().fetch()

    def symbolsDir(self):
        return os.path.join(self.imageDir(), 'symbols')

    # Loosely based on https://chromium.googlesource.com/chromium/chromium/+/34599b0bf7a14ab21a04483c46ecd9b5eaf86704/components/breakpad/tools/generate_breakpad_symbols.py#92
    def dumpSymbols(self, binaryFile):
        CraftCore.log.info('Dump symbols for: %s' % binaryFile)

        out = io.BytesIO()
        utils.system(['dump_syms', binaryFile], stdout=out)

        outBytes = out.getvalue()
        firstLine = str(outBytes.splitlines()[0], 'utf-8')
        CraftCore.log.info('Module line: %s' % firstLine)
        regex = "^MODULE [^ ]+ [^ ]+ ([0-9aA-fF]+) (.*)"
        CraftCore.log.debug('regex: %s' % regex)
        moduleLine = re.match(regex, firstLine)
        CraftCore.log.debug('regex: %s' % moduleLine)
        outputPath = os.path.join(self.symbolsDir(), moduleLine.group(2),
                             moduleLine.group(1))

        if (not os.path.exists(outputPath)):
            os.makedirs(outputPath, exist_ok=True)

        symbolFileBasename = moduleLine.group(2).replace(".pdb", "")
        symbolFile = os.path.join(outputPath, "%s.sym" % symbolFileBasename)
        outputFile = open(symbolFile, 'wb')
        outputFile.write(outBytes)

        CraftCore.log.info('Writing symbols to: %s' % symbolFile)

    def install(self):
        if not CMakePackageBase.install(self):
            return False

        if CraftCore.compiler.isWindows:
            patterns = ['**/*.dll', '**/*.exe']
            for pattern in patterns:
                for f in glob.glob(os.path.join(self.imageDir(), pattern), recursive=True):
                    self.dumpSymbols(f)

        return True

    def createPackage(self):
        self.defines["appname"] = "owncloud"
        if CraftCore.compiler.isWindows:
            sep = '\\%s' % os.sep
            regex = r"symbols%s.*" % sep
            self.whitelist.append(re.compile(regex))

        self.defines["shortcuts"] = [{"name" : self.subinfo.displayName , "target" : f"bin/{self.defines['appname']}{CraftCore.compiler.executableSuffix}", "description" : self.subinfo.description}]
        self.defines["icon"] = Path(self.buildDir()) / "src/gui/owncloud.ico"

        self.ignoredPackages += ["binary/mysql"]
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages += ["libs/dbus"]
        return TypePackager.createPackage(self)
