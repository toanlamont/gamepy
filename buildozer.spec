[app]

# (str) Title of your application
title = YourPygameApp

# (str) Package name
package.name = yourpygameapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.yourdomain

# (str) Source code where the main.py live
source.dir = .

# (list) List of source files
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
requirements = kivy,pygame,pyjnius,requests

# (str) Supported orientations (landscape, portrait or all)
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
# fullscreen = 0

# (list) Permissions
# android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
android.permissions = INTERNET

[build]

# (int) The number of parallel jobs to build
parallel = 1

# (str) Path to the directory where the application will be stored
directory = build

# (str) Temp directory to store the requirements
# build_dir = /tmp/build

# (list) List of inclusions using pattern matching
# build_include_patterns = assets/*,images/*.png

# (list) List of exclusions using pattern matching
# build_exclude_patterns = license,images/*/*.jpg

# (list) List of directory to preserve (relative to the build_dir, directory path is used if nothing is specified)
# build_preserve_dir = src/customcode src/mypdfs

# (list) List of shared libraries to copy (name without extension)
# source.shared_libraries = mylib1,mylib2

# (list) List of Android assets to copy (leaving out .svn directories)
# source.android_assets = media/icon.png, media/myfile.wav:media/somefile.wav

# (list) List of application meta-data (key=value format)
# android.meta_data = android.app.multitouch

# (list) List of Java classes to add to the compilation. They must be in source.<extension>
# android.add_src = AndroidManifest.xml
# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, all
# android.arch = armeabi-v7a

# (bool) Run p4a after build
# p4a = false

# (str) The URL of the p4a repository
# p4a.source_dir = ../android

# (str) Path to a custom distribution
# dist_name = mydist

# (str) FTP/HTTP server credentials (should also specify a mirror)
# hostpython = python-for-android
# username = my-username
# password = my-password

# (str) Mirrors
# hostpython = https://your.mirror.com/path

# (str) Default recipe to use for builds
# default.recipe = pygame

# (str) macOS developer certificate (used to sign app on macOS only)
# macos.code_signing.identity = 

# (str) iOS distribution certificate (used to sign app on iOS only)
# ios.distribution.p12 = /path/to/your/distribution/certificate.p12

# (str) iOS development certificate (used to sign app on iOS only)
# ios.development.p12 = /path/to/your/development/certificate.p12

# (str) iOS development provisioning profile (used to sign app on iOS only)
# ios.development.provisioning_profile = /path/to/your/provisioning/profile

# (list) iOS frameworks to link against (this flag is used to add linker flags)
# ios.frameworks = UIKit CoreGraphics

# (str) Android entry point, default is ok for Kivy-based application
# android.entrypoint = org.renpy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based application
# android.app_theme = "@android:style/Theme.NoTitleBar"

# (str) Android app numeric version, default is auto incremented
# android.numeric_version = 1

# (str) Android AAPT2 executable, default is `aapt2`
# android.aapt2 = aapt2

# (list) Configurations to include in the final apk
# android.conf.include_patterns = *

# (list) Additional Java classpaths
# android.add_javac_libraries = libs/foo.jar:libs/bar.jar

# (list) Java classes to add to the build. They must be in the form <module.submodule.Class>
# android.add_classes = com.android.mystuff.Foo

# (list) Java jar libraries to add to the dist build
# android.add_jars = foo.jar:bar.jar

# (list) Java sources to add to the dist build
# android.add_java_src = src/foo.java:src/bar.java

# (list) Android AAR archives to add (currently works only with sdl2_gradle
# build tool)
# android.add_aars = path/to/my.aar

# (list) Gradle dependencies to add (currently works only with sdl2_gradle
# build tool)
# android.gradle_dependencies = foo:bar:baz

# (list) add python objects (e.g. for pyjnius)
# android.add_objects = mypython, mypython2

# (list) Gradle repositories to add {can be necessary for android gradle dependencies}
# android.gradle_repositories = maven {url "https://url.to.repo"}
