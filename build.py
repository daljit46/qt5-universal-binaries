import os
import subprocess
import argparse

qt_version = "5.15.10"
current_dir = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(
    description="Build Qt 5 universal binaries for Mac OS X."
)

parser.add_argument(
    "--prefix",
    type=str,
    default=os.path.join(current_dir, qt_version),
    help="The prefix path to install Qt to.",
)
parser.add_argument(
    "--modules",
    type=str,
    default="qtbase qtsvg",
    help="The modules to build.",
)
parser.add_argument(
    "--parallel",
    type=int,
    default=2,
    help="The number of threads.",
)

args = parser.parse_args()

prefix_path = args.prefix
modules = args.modules.split(" ")


# Print the arguments
print("\n")
print("Installation path configured to: " + prefix_path)
print("List of modules to build: " + str(modules))
print("Number of threads: " + str(args.parallel))
print("\n")


def exec_cmd(cmd):
    print(cmd + "\n")
    subprocess.check_call(cmd, shell=True)


# Download and extract the tarball.
download_link = "https://download.qt.io/official_releases/qt/5.15/5.15.10/single/qt-everywhere-opensource-src-{}.tar.xz".format(
    qt_version
)

exec_cmd(
    "curl -L -o qt-everywhere-opensource-src-{}.tar.xz ".format(qt_version)
    + download_link
)
exec_cmd("tar -xvf qt-everywhere-opensource-src-{}.tar.xz".format(qt_version))

# Configure the build
os.chdir("qt-everywhere-src-{}".format(qt_version))

configure_args = [
    "-opensource",
    "-confirm-license",
    "-release",
    "-nomake examples",
    "-nomake tests",
    '-device-option QMAKE_APPLE_DEVICE_ARCHS="x86_64 arm64"',
]

all_modules = [
    "qt3d",
    "qtactiveqt",
    "qtandroidextras",
    "qtbase",
    "qtcharts",
    "qtconnectivity",
    "qtdatavis3d",
    "qtdeclarative",
    "qtdoc",
    "qtgamepad",
    "qtgraphicaleffects",
    "qtimageformats",
    "qtlocation",
    "qtlottie",
    "qtmacextras",
    "qtmultimedia",
    "qtnetworkauth",
    "qtpurchasing",
    "qtquick3d",
    "qtquickcontrols",
    "qtquickcontrols2",
    "qtquicktimeline",
    "qtremoteobjects",
    "qtscript",
    "qtscxml",
    "qtsensors",
    "qtserialbus",
    "qtserialport",
    "qtspeech",
    "qtsvg",
    "qttools",
    "qttranslations",
    "qtvirtualkeyboard",
    "qtwayland",
    "qtwebchannel",
    "qtwebengine",
    "qtwebglplugin",
    "qtwebsockets",
    "qtwebview",
    "qtwinextras",
    "qtx11extras",
    "qtxmlpatterns",
]

# Only add the modules that are requested
for m in all_modules:
    if m not in modules:
        configure_args.append("-skip " + m)

# Run configure
exec_cmd("./configure " + " ".join(configure_args))

# Build and install the libraries
exec_cmd("make -j" + str(args.parallel))
exec_cmd("make install")
