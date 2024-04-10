import configparser
import glob
import io
import os
import re
import subprocess
import sys

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "git@github.com:owncloud/client-desktop-owap.git"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["craft/craft-blueprints-owncloud"] = None
        self.buildDependencies["dev-utils/cmake"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None

        # actually a runtime dep but for now we only wan't to deploy the binary
        self.buildDependencies["owncloud/owncloud-client"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.addExecutableFilter(r"bin/(?!(owap)).*")
        return super().createPackage()
