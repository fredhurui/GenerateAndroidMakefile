# GenerateAndroidMakefile
Generate Android.bp for the shared library in the apk, which is used to integrated apk to Android ROM

前置条件：
安装python2.7

功能说明：
将apk解压到同名的目录，然后在lib目录下生成Android.bp, Android.bp用于对lib/armeabi-v7a目录下面的所有so进行prebuild

待完善：
对lib/arm64-v8a目录下面的所有so进行prebuild

用法：
python generatePrebuildMakefile.py  test.apk

