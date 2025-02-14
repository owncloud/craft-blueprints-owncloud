# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *
from Utils import CraftHash

class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None
        self.runtimeDependencies["perl-modules/module-build"] = None

    def setTargets(self):
        for ver in ["1.54"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/T/TH/THESEAL/Config-File-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Config-File-{ver}"
        self.targetDigests["1.54"] = (["03c8ca8fe02cbedbdb09f4d944e8bb469ef3b0b38d1bb14f82549978aab9b75d"], CraftHash.HashAlgorithm.SHA256)

        self.tags = "Config-File"
        self.defaultTarget = "1.54"


class Package(PerlPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def configure(self):
        self.enterBuildDir()
        env = {
            "PERL5LIB": None,
            "PERL_MM_OPT": None,
            "PERL_LOCAL_LIB_ROOT": None,
            "PERL_MM_USE_DEFAULT": "1",
            "PERL_AUTOINSTALL": "--skipdeps",
        }
        with utils.ScopedEnv(env):
            return utils.system(Arguments.formatCommand(["perl", "Build.PL"], self.subinfo.options.configure.args))

#        self.enterSourceDir()
#        Path("Makefile.PL").symlink_to("Build.PL")
#        return super().configure()

    def make(self):
        self.enterBuildDir()
        env = {
            "PERL5LIB": None,
            "PERL_MM_OPT": None,
            "PERL_LOCAL_LIB_ROOT": None,
            "PERL_MM_USE_DEFAULT": "1",
            "PERL_AUTOINSTALL": "--skipdeps",
        }
        with utils.ScopedEnv(env):
            return utils.system(["./Build"])

    def install(self):
        env = {"PERL5LIB": None, "PERL_MM_OPT": None, "PERL_LOCAL_LIB_ROOT": None}
        with utils.ScopedEnv(env):
            return utils.system(["./Build", "install", f"--destdir={self.installDir()}"]) and self._fixInstallPrefix()
