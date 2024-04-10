import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "FUSE filesystem to mount squashfs archives"

        for ver in ["0.1.104"]:
            self.targets[ver] = f"https://github.com/vasi/squashfuse/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"squashfuse-{ver}"

        self.targetDigests["0.1.104"] = (
            ["9e6f4fb65bb3e5de60c8714bb7f5cbb08b5534f7915d6a4aeea008e1c669bd35"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "0.1.104"

    def setDependencies(self):
        self.buildDependencies["dev-utils/automake"] = None
        self.buildDependencies["dev-utils/autoconf"] = None
        self.buildDependencies["dev-utils/libtool"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/libzstd"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # run autogen.sh
        self.subinfo.options.configure.bootstrap = True

        self.subinfo.options.configure.args += [
            "--without-lzo",
            "--without-lz4",
        ]
