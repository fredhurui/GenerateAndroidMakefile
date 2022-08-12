import os
import sys
import glob
import fnmatch
import zipfile
import re

path = os.getcwd() + '/'
#needHanldeArm64 = True
needHanldeArm64 = False

#file is the apk name with suffix, it should like my.apk
def unzipfileAndGenerateMakefile(file):
    uzfile = zipfile.ZipFile(path + file)
    apk_name = file.split('.')[0]
    print(apk_name)
    print "unzip apk file to " + apk_name
    unzipedFilePath = path + apk_name + "/"
    #apkFolder = Path(unzipedFilePath)
    if os.path.exists(unzipedFilePath):
        print unzipedFilePath + " folder is exist"
    else:
        print "do unzip"
        uzfile.extractall(unzipedFilePath)
    generateSharedLibraryPrebuildMakefile(unzipedFilePath + "lib/")
    
def generateSharedLibraryPrebuildMakefile(file):
    #create xxx/lib/Android.bp
    #makefilePath = Path(file + 'Android.bp')
    if os.path.exists(file + 'Android.bp'):
        print file + 'Android.bp' + " is exist, remove it first"
        os.remove(file + 'Android.bp')
        
    out = open(file + 'Android.bp', 'a')
    lib_dirs = os.listdir(file)
    #lib_dirs = glob.glob(file)
    #Only handle arm64-v8a and armeabi-v7a
    for dirname in lib_dirs:
        print "lib sub dir : " + dirname
        if cmp("armeabi-v7a", dirname) == 0:
            print "Handle armeabi-v7a libs"
            print "list " + file + dirname + "/*.so"
            #libs = os.listdir(file + dirname + "/*.so")
            libs = fnmatch.filter(os.listdir(file + dirname), "*.so")
            for shareLibName in libs:
                print shareLibName
                content = generatearmeabiv7aMakefile(shareLibName)
                out.write(content)
                out.write("\n")
        if cmp("arm64-v8a", dirname) == 0 and needHanldeArm64:
            print "Handle arm64-v8a libs"
            #libs = glob.glob(file + dirname + "/*.so")
            libs = fnmatch.filter(os.listdir(file + dirname), "*.so")
            for shareLibName in libs:
                print shareLibName
                ins = open(file + 'Android.bp', 'r')
                file_content = ins.read()
                print "old content:" + file_content
                findResult = re.findall(shareLibName, content)
                count = len(findResult)
                print findResult
                print "found count:%d" %count
                if count == 1:
                    #should merge conent
                    print "find it and do merge"
                    print "old content:" + file_content
                else:
                    content = generatearm64v8aMakefile(shareLibName)
                    out.write(content)
                    out.write("\n")
    #out.write()
    out.close()

def generatearmeabiv7aMakefile(shareLibName):
    #lib_name = shareLibName.split('.')[0]
    #lib_name = os.path.basename(shareLibName)
    #suffixIndex = shareLibName.find(".so")
    #print  suffixIndex
    lib_name = shareLibName[0 : -3]
    print  lib_name
    AndroidBpContent = """
cc_prebuilt_library_shared {{
    name: \"{}\",
    target: {{
        android_arm: {{
            srcs: [\"armeabi-v7a/{}.so\"],
        }},
    }},
    strip: {{
        none: true,
    }},
}}"""
    result = AndroidBpContent.format(lib_name, lib_name)
    #print("AndroidBpContent:\n" + result)
    return result

def generatearm64v8aMakefile(shareLibName):
    #lib_name = shareLibName.split('.')[0]
    #lib_name = os.path.basename(shareLibName)
    #suffixIndex = shareLibName.find(".so")
    #print  suffixIndex
    lib_name = shareLibName[0 : -3]
    print  lib_name
    #first check if already generated makefile for armeabi-v7a for current lib
    
    AndroidBpContent = """
cc_prebuilt_library_shared {{
    name: \"{}\",
    target: {{
        android_arm64: {{
            srcs: [\"arm64-v8a/{}.so\"],
        }},
    }},
    strip: {{
        none: true,
    }},
}}"""
    result = AndroidBpContent.format(lib_name, lib_name)
    #print("AndroidBpContent:\n" + result)
    return result



if __name__ == '__main__':
    #print ("argv len: %d" %len(sys.argv))
    if len(sys.argv) == 2:
        unzipfileAndGenerateMakefile(sys.argv[1])
    else:
        print "Bad input parameters"
        print 'Usage: python %s xxx.apk' %sys.argv[0]