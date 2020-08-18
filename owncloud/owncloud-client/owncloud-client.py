import info

import configparser
import os
import io
import re
import sys
import subprocess
import glob

class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.registerOption("buildVfsWin", False)
        self.options.dynamic.registerOption("enableCrashReporter", False)

    def setTargets(self):
        self.versionInfo.setDefaultValues(tarballUrl="https://download.owncloud.com/desktop/stable/owncloudclient-${VERSION}.tar.xz",
                                          tarballInstallSrc="owncloudclient-${VERSION}",
                                          gitUrl="[git]https://github.com/owncloud/client")

        # we don't have that branche yet
        self.svnTargets["2.8"] = self.svnTargets["master"]

        self.description = "ownCloud Desktop Client"
        self.displayName = "ownCloud"
        self.webpage = "https://owncloud.org"

    def setDependencies(self):
        self.buildDependencies["craft/craft-blueprints-owncloud"] = None
        self.buildDependencies["dev-utils/cmake"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/breakpad-tools"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtmacextras"] = None
        self.runtimeDependencies["libs/qt5/qttranslations"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None
        if self.options.dynamic.buildVfsWin:
            self.runtimeDependencies["owncloud/client-plugin-vfs-win"] = None

        if self.buildTarget != "master" and self.buildTarget < CraftVersion("2.6"):
            self.runtimeDependencies["libs/qt5/qtwebkit"] = None

        if not CraftCore.compiler.isWindows:
            # the unit tests first need to get ported to Windows
            if self.options.dynamic.buildTests:
                self.buildDependencies["dev-utils/cmocka"] = None



from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True
        # Pending PR to move to standard BUILD_TESTING: https://github.com/owncloud/client/pull/6917#issuecomment-444845521
        self.subinfo.options.configure.args += " -DUNIT_TESTING={testing} ".format(testing="ON" if self.buildTests else "OFF")

        if 'OWNCLOUD_CMAKE_PARAMETERS' in os.environ:
                self.subinfo.options.configure.args += os.environ['OWNCLOUD_CMAKE_PARAMETERS']
        if self.subinfo.options.dynamic.buildVfsWin:
            self.win_vfs_plugin = CraftPackageObject.get("owncloud/client-plugin-vfs-win")
            self.subinfo.options.configure.args += f" -DVIRTUAL_FILE_SYSTEM_PLUGINS={self.win_vfs_plugin.instance.sourceDir()}"

        if "ENABLE_CRASHREPORTS" in os.environ:
            self.subinfo.options.dynamic.enableCrashReporter = configparser.RawConfigParser.BOOLEAN_STATES.get(os.environ.get("ENABLE_CRASHREPORTS").lower())
        if self.subinfo.options.dynamic.enableCrashReporter:
            self.subinfo.options.configure.args += " -DWITH_CRASHREPORTER=ON"


    @property
    def applicationExecutable(self):
        return os.environ.get('ApplicationExecutable', 'owncloud')

    def fetch(self):
        if self.subinfo.options.dynamic.buildVfsWin:
            if not self.win_vfs_plugin.instance.fetch(noop=False):
                return False
        return super().fetch()

    def unpack(self):
        if self.subinfo.options.dynamic.buildVfsWin:
            if not self.win_vfs_plugin.instance.unpack(noop=False):
                return False
        return super().unpack()

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isWindows:
            # ensure we can find the sync-exclude.lst
            configDir = Path(self.installDir()) / "config" / os.environ.get('ApplicationShortname', self.applicationExecutable)
            if not configDir.exists():
                configDir = Path(self.installDir()) / "etc" / os.environ.get('ApplicationShortname', self.applicationExecutable)
            if configDir.exists():
                if not utils.mergeTree(configDir, Path(self.installDir()) / "bin"):
                    return False
        return True

    # Loosely based on https://chromium.googlesource.com/chromium/chromium/+/34599b0bf7a14ab21a04483c46ecd9b5eaf86704/components/breakpad/tools/generate_breakpad_symbols.py#92
    def dumpSymbols(self, binaryFiles : [], dest : str) -> bool:
        dest = Path(dest) / "symbols"
        utils.cleanDirectory(dest)
        moduleRe = re.compile("^MODULE [^ ]+ [^ ]+ ([0-9aA-fF]+) (.*)")
        icuRe = re.compile(r"icudt\d\d.dll")
        finderSyncExtRe = re.compile(r"FinderSyncExt")
        cmdRe = re.compile(r".*cmd")
        crashReporterRe = re.compile(r".*_crash_reporter")

        appDsymDir = Path(CraftCore.standardDirs.craftRoot()) / "Applications/KDE/*.app.dSYM/Contents/Resources/DWARF"
        hack = []
        for exp in ["FinderSyncExt", "*cmd", "*_crash_reporter"]:
            hack += glob.glob(str(appDsymDir / exp))

        for f in hack:
            CraftCore.log.warning(f'dump_symbols: {f} is removed')
            os.remove(f)
        print(hack)

        for binaryFile in binaryFiles:
            binaryFile = Path(binaryFile)
            if CraftCore.compiler.isWindows and icuRe.match(binaryFile.name):
                CraftCore.log.warning(f'dump_symbols: {binaryFile} is blacklisted because it has no symbols')
                continue

            if CraftCore.compiler.isMacOS and (finderSyncExtRe.match(binaryFile.name) or cmdRe.match(binaryFile.name) or crashReporterRe.match(binaryFile.name)):
                CraftCore.log.warning(f'dump_symbols: {binaryFile} is blacklisted because we have no crash reporter for the finder extension, the cmdline client or the crash reporter itself')
                continue

            CraftCore.log.info(f"Dump symbols for: {binaryFile}")

            command = ['dump_syms']
            if CraftCore.compiler.isMacOS:
                relPath = binaryFile.relative_to(self.archiveDir())
                dSym = Path(CraftCore.standardDirs.craftRoot()) / relPath
                bundleDir = list(filter(lambda x: x.name.endswith(".framework") or x.name.endswith(".app"), dSym.parents))
                if bundleDir:
                    dSym = bundleDir[-1]
                dSym = Path(f"{dSym}.dSYM")
                if dSym.exists():
                    command += ["-g", dSym]
            command.append(binaryFile)
            with io.BytesIO() as out:
                utils.system(command, stdout=out, stderr=subprocess.DEVNULL)
                outBytes = out.getvalue()

            if not outBytes:
                CraftCore.log.warning(f"Found no valid output for {binaryFile}: {outBytes}")
                continue

            firstLine = str(outBytes.splitlines(1)[0], 'utf-8').strip()
            CraftCore.log.info(f"Module line: {firstLine}")

            if CraftCore.compiler.isWindows:
                if firstLine.startswith("loadDataForPdb and loadDataFromExe failed for"):
                    CraftCore.log.warning(f"Module does not contain debug symbols: {binaryFile}")
                    return False

            CraftCore.log.debug('regex: %s' % moduleRe)
            moduleLine = moduleRe.match(firstLine)
            if not moduleLine:
                CraftCore.log.warning("Failed to parse dump_symbols output")
                return False
            CraftCore.log.debug('regex: %s' % moduleLine)
            outputPath = dest / moduleLine.group(2) / moduleLine.group(1)

            utils.createDir(outputPath)
            symbolFile = (outputPath / moduleLine.group(2))
            if CraftCore.compiler.isWindows:
                symbolFile = symbolFile.with_suffix(".sym")
            else:
                symbolFile = f"{symbolFile}.sym"
            with open(symbolFile, 'wb') as outputFile:
                outputFile.write(outBytes)
            CraftCore.log.info('Writing symbols to: %s' % symbolFile)
        return True

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        self.defines["appname"] = self.applicationExecutable
        self.defines["apppath"] = "Applications/KDE/" + self.applicationExecutable + ".app"
        self.defines["company"] = "ownCloud GmbH"
        self.defines["shortcuts"] = [{"name" : self.subinfo.displayName , "target" : f"{self.defines['appname']}{CraftCore.compiler.executableSuffix}", "description" : self.subinfo.description}]
        self.defines["icon"] = Path(self.buildDir()) / "src/gui/owncloud.ico"
        self.defines["pkgproj"] = Path(self.buildDir()) / "admin/osx/macosx.pkgproj"


        self.blacklist.append(re.compile(r"bin[/|\\](?!" + self.applicationExecutable + r").*" + re.escape(CraftCore.compiler.executableSuffix)))

        self.ignoredPackages += ["binary/mysql"]
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages += ["libs/dbus"]

        if self.subinfo.options.dynamic.enableCrashReporter:
            sep = '\\%s' % os.sep
            regex = r"symbols%s.*" % sep
            self.whitelist.append(re.compile(regex))
        return super().createPackage()

    def preArchive(self):
        if isinstance(self, NullsoftInstallerPackager):
            archiveDir = Path(self.archiveDir())
            # TODO: install translations to the correct location in the first place
            for src, dest in [("bin",  ""), ("share/owncloud/i18n",  "")]:
                if not utils.mergeTree(archiveDir / src, archiveDir / dest):
                    return True
        else:
            if self.subinfo.options.dynamic.enableCrashReporter:
                binaries = utils.filterDirectoryContent(self.archiveDir(),
                                                    whitelist=lambda x, root: utils.isBinary(os.path.join(root, x)),
                                                    blacklist=lambda x, root: True)
                if not self.dumpSymbols(binaries, self.archiveDebugDir()):
                    return False
        return super().preArchive()
