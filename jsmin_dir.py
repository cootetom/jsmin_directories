
# Author: Tom Coote (www.tomcoote.co.uk)
# Date: 10th Dec 2008

# This code is a wrapper for the jsmin code originally written by Douglas Crockford
# and translated into Python by Baruch Even. It will look at all .js files in the
# current directory and run jsmin on them. It can also be told to look recursively
# in all child directories by passing in -r as a parameter. To remove all -dev versions
# and revert back to the none -dev filenames as un-minified files call the script
# and pass in -u as a parameter. To call the original jsmin which accepts an input file
# and an output file pass in the parameter -o before specifying files.
#
# All .js files will be copied to two versions, file-dev.js and file.js, The -dev file
# is the un-minified version and the file without -dev suffix is the minified version.
# Any filename that already has the -dev suffix will be minified to it's none -dev
# version, overwriting if already there or creating if not.

# Example usage;
#   To run jsmin on all .js files in a directory, navigate to that directory and run
#   python jsmin_dir.py
#
#   To run jsmin on all .js files in a directory including all sub directories
#   navigate to that directory and run
#   python jsmin_dir.py -r
#
#   To undo jsmin_dir
#   python jsmin_dir.py -u
#   or recursively
#   python jsmin_dir.py -u -r
#   NOTE:   undo is expected dev files to have a -dev suffix and a matching file without
#           the suffix to be the minified version.
#
#   To call original jsmin on a file
#   python jsmin_dir.py -o <file.js > outFile.js

# This code is licenced in the same way jsmin was originally licenced as below;
#
#
# /* jsmin.c
#    2007-05-22
#
# Copyright (c) 2002 Douglas Crockford  (www.crockford.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# The Software shall be used for Good, not Evil.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# */

from jsmin import JavascriptMinify
import os, re

class JavaScriptDirMinify(JavascriptMinify):

    def _getFiles(self):
        '''
            Get the list of file names to minify. Either all files in the
            current directory or if the -r parameter was passed in all files
            in the current plus all child directories recursively.
        '''
        allFiles = []
        
        if not self.recurse:
            allFiles = os.listdir(os.getcwd())
        else:
            for root, dirs, files in os.walk(os.getcwd()):
                for name in files:
                    allFiles.append(os.path.join(root, name))

        return allFiles

    def _deleteMinified(self):
        '''
            Remove all files that have been minified by this script before. This
            is done by copying all files with the -dev suffix to a file with the
            same name but without the -dev suffix and then deleting the dev version.
            This leaves you back with all none -dev files as un-minified files.
        '''
        for name in self._getFiles():
            if re.search(r'-dev\.js$', name):
                minName = re.sub(r'-dev\.js$', '.js', name)
                os.system('copy %s %s >nul' % (name, minName))
                os.system('del %s >nul' % name)

    def dirMinify(self, *args):
        '''
            Create two versions of each .js file to minify. A file with a -dev suffix
            and a file without a -dev suffix. The -dev file is the original development
            version of the file and the file without -dev is the minified version of
            the file.
        '''
        self.recurse = '-r' in args

        self._deleteMinified()
        if '-u' not in args:
            for name in self._getFiles():
                if re.search(r'\.js$', name) and not re.search(r'-dev\.js$', name):
                    devName = re.sub(r'\.js$', '-dev.js', name)
                    os.system('copy %s %s >nul' % (name, devName))

                    inputStream = open(devName, 'rb')
                    outputStream = open(name, 'wb')
                    self.minify(inputStream, outputStream)

if __name__ == '__main__':
    import sys
    jsdm = JavaScriptDirMinify()
    
    if '-o' in sys.argv:
        jsdm.minify(sys.stdin, sys.stdout)
    else:
        jsdm.dirMinify(*sys.argv)
