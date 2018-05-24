import info
import os

import io
import re

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["master"]:
            self.svnTargets[ver] = f"[git]https://github.com/owncloud/client|{ver}|"

        self.defaultTarget = 'master'
        self.description = "ownCloud Desktop Client"
        self.webpage = "https://owncloud.org"

    def setDependencies(self):
        self.buildDependencies["craft/craft-blueprints-owncloud"] = "default"
        self.buildDependencies["dev-utils/cmake"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["dev-utils/breakpad-tools"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtsvg"] = "default"
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebkit"] = "default"
        self.runtimeDependencies["qt-libs/qtkeychain"] = "default"


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True

        self.subinfo.options.configure.args = "-DUNIT_TESTING=1 -DWITH_TESTING=1"

        if 'ENABLE_CRASHREPORTS' in os.environ:
            if os.environ['ENABLE_CRASHREPORTS'] == 'true':
                self.subinfo.options.configure.args += " -DWITH_CRASHREPORTER=1"

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

        patterns = ['**/*.dll', '**/*.exe']
        for pattern in patterns:
            for f in glob.glob(os.path.join(self.imageDir(), pattern), recursive=True):
                self.dumpSymbols(f)

        return True

    def createPackage(self):
        sep = '\\%s' % os.sep
        regex = r"symbols%s.*" % sep
        self.whitelist.append(re.compile(regex))

        return TypePackager.createPackage(self)
