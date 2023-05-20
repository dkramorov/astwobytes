#!/usr/local/env python3
import os
import shutil

root_folder = '/Users/jocker/Library'

folders = (
    'Caches/JetBrains',
    'Logs/JetBrains',
    'Application Support/JetBrains',
    'Preferences/com.apple.java.util.prefs.plist', # тут ключ тачки
    'Saved Application State/com.jetbrains.intellij.savedState',
    'Preferences/*jetbrains*',
)

def change_settings():
    lib_path = '/Users/jocker/Library'
    app_support_path = os.path.join(lib_path, 'Application Support')
    jet_brains_path = os.path.join(app_support_path, 'JetBrains')
    idea_path = os.path.join(jet_brains_path, 'IntelliJIdea2020.3')
    for item in (app_support_path, jet_brains_path, idea_path):
        if not os.path.exists(item):
            os.mkdir(item)
    vmoptions = os.path.join(idea_path, 'idea.vmoptions')
    with open(vmoptions, 'w+', encoding='utf-8') as f:
        f.write('''-Xms128m
-Xmx2048m
-XX:ReservedCodeCacheSize=512m
-XX:+UseConcMarkSweepGC
-XX:SoftRefLRUPolicyMSPerMB=50
-XX:CICompilerCount=2
-XX:+HeapDumpOnOutOfMemoryError
-XX:-OmitStackTraceInFastThrow
-ea
-Dsun.io.useCanonCaches=false
-Djdk.http.auth.tunneling.disabledSchemes=""
-Djdk.attach.allowAttachSelf=true
-Djdk.module.illegalAccess.silent=true
-Dkotlinx.coroutines.debug=off

-XX:ErrorFile=$USER_HOME/java_error_in_idea_%p.log
-XX:HeapDumpPath=$USER_HOME/java_error_in_idea.hprof
''')

def main():
    for folder in folders:
        path = os.path.join(root_folder, folder)
        if os.path.exists(path):
            print('DROP: %s' % path)
            try:
                shutil.rmtree(path)
            except Exception:
                print('ERROR DROP %s' % path)
        elif '*' in path:
            print('DROP WILDCARD %s' % path)
            try:
                os.system('rm -r %s' % path)
            except Exception:
                print('ERROR DROP %s' % path)
        else:
            print('ERROR: path not found %s' % path)
    os.system('killall cfprefsd')
    change_settings()

if __name__ == '__main__':
    main()
