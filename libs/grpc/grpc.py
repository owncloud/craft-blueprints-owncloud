import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/grpc/grpc.git'
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["libs/zlib"] = None
        self.buildDependencies["libs/openssl"] = None
        self.buildDependencies["libs/c-ares"] = None
        self.buildDependencies["libs/protobuf"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DgRPC_PROTOBUF_PROVIDER=package -DgRPC_CARES_PROVIDER=package -DgRPC_SSL_PROVIDER=package -DgRPC_ZLIB_PROVIDER=package -DgRPC_BUILD_TESTS=OFF"
        if not CraftCore.compiler.isWindows:
            self.subinfo.options.configure.args += " -DBUILD_SHARED_LIBS=ON"
