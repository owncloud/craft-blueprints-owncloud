import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/protocolbuffers/protobuf.git'
        self.targetConfigurePath["master"] = "cmake"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["libs/zlib"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_MSVC_STATIC_RUNTIME=OFF"
        if not CraftCore.compiler.isWindows:
            self.subinfo.options.configure.args += " -DBUILD_SHARED_LIBS=ON"