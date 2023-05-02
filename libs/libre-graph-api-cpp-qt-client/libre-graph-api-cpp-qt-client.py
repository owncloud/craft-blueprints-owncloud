import io
import os
import re

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["v0.11.0", "v0.12.0", "v0.13.2", "v1.0.1"]:
            self.svnTargets[ver] = f"https://github.com/owncloud/libre-graph-api-cpp-qt-client.git||{ver}"
            self.targetConfigurePath[ver] = "client"

        for ver in ["1.0.3"]:
            self.targets[ver] = f"https://github.com/owncloud/libre-graph-api-cpp-qt-client/archive/refs/tags/v{ver}.tar.gz"
            self.targetConfigurePath[ver] = "client"
            self.targetInstSrc[ver] = f"libre-graph-api-cpp-qt-client-{ver}"
        self.targetDigests["1.0.3"] = (["17cd8b03f5fca97d9944701f183dfd44d88c3a00a01ed0395aa925768551d16c"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["main"] = f"https://github.com/owncloud/libre-graph-api-cpp-qt-client.git|main|"
        self.targetConfigurePath["main"] = "client"

        self.defaultTarget = "1.0.3"
        self.description = "Libre Graph Cloud Collaboration API - Qt bindings"
        self.webpage = "https://owncloud.dev/libre-graph-api/"

    def setDependencies(self):
        self.buildDependencies["craft/craft-blueprints-owncloud"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
