#    mild: build system in python3
#    Copyright (C) 2020 Mark Hargreaves
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import termcolor
from threading import Thread
import time
# Common class for CC errors
class MildError:
    def __init__(self, Error):
        termcolor.cprint("mild: fatal error: "+Error, "red")
        termcolor.cprint("mild: can't recover, exiting", "red")
        exit(1)
# Common class for compilers
class Compiler:
    # Compilers take ONE positional argument. No more than that.
    def __init__(self, *ccargs):
        self.ccomm = ccargs[:-1]
        self.extension = ccargs[len(ccargs)-1]
    def compile(self, argument):
        # if no positional arguments, just execute it
        ccline = ""
        for n in self.ccomm:
            ccline = ccline+" "+n
        ccline = ccline.replace("argument", argument)
        ccline = ccline.replace(".extension", "."+self.extension)
        os.system(ccline)
class MildCC:
    def __init__(self, mildlist, multithreading, asyncthreads):
        # Base cli args from console
        self.cliargs = sys.argv[1:]
        # Common name for mild file, mild.mildlist(like Makefile or smth)
        self.mildfile = mildlist
        # Prefix for all mild files: mildlist(usually one mildlist means one target, no more than that)
        self.mildprefix = ".mildlist"
        # Basic compiler settings: have gcc and g++ by default

        # A list for known file extensions, can be appended
        self.knownextensions = ["c", "cpp"]
        gcc = Compiler("gcc", "-O3", "argument.extension", "-o", "argument.o", "c")
        gpp = Compiler("g++", "-O3", "argument.extension", "-o", "argument.o", "cpp")
        self.outextensions = [".o", ".mildlist"]
        # A list with compilers for the extensions above, must be strictly tied to knownext, e.g. "c" entry index is 0 in knownext, so gcc must have index 0 in compilerforext
        self.compilerforext = [gcc, gpp]
        # Is the multithreading asynchronous?
        self.multithreading_async = asyncthreads
        # Multithreading state, 1 or 0
        self.multithreading = multithreading
        # Variable for threads, used for listing them to wait for threads to end
        self.multithreading_threads = []
    def generate(self, *targets):
        for target in targets:
            print("mild: generating {} for target {}".format(target, self.mildfile)) 
            if target[-2:] == ".o":
                #print("mild: assume {} is an file".format(target))
                files = [f for f in os.listdir('.') if os.path.isfile(f)]
                for f in files:
                    ft = os.path.splitext(f)[0]
                    if ft == target[:-2]:
                        ext = os.path.splitext(f)[1]
                        exty = ext[1:]
                        if exty in self.knownextensions:
                            extindex = self.knownextensions.index(exty)
                            CC = self.compilerforext[extindex]
                            CC.compile(target[:-2])
                        else:
                            if ext in self.outextensions:
                                pass
                            else:
                                raise MildError("no compiler for extension {} for target {}".format(ext, target))
            else:
                termcolor.cprint("mild: dependency building, dependency {} for target {}".format(target, self.mildfile), "blue")
                mcc = MildCC(target, self.multithreading, self.multithreading_async)
                mcc.parsemildlist()
    def generatequeue(self, *targets):
        for target in targets:
            # Skip files, since we need dependencies to build first
            if target[-2:] == ".o":
                continue
            else:
                process = Thread(target=self.generate, args=[target])
                process.start()
                self.multithreading_threads.append(process)
        for thr in self.multithreading_threads:
        # Wait for threads to end
            if self.multithreading_async:
                break
            thr.join()
        for target in targets:
            # Now generating files
            if target[-2:] == ".o":
                process = Thread(target=self.generate, args=[target])
                process.start()
                self.multithreading_threads.append(process)
    # Common set compiler for MildCC class
    def setcompiler(self, compiler, extension):
        # Compiler needs to be updated
        if extension in self.knownextensions:
            extindex = self.knownextensions.index(extension)
            self.compilerforext[extindex] = compiler
        # New compiler for new extension
        else:
            self.knownextensions.append(extension)
            self.compilerforext.append(compiler)
    def sync(self):
        # synchronise all threads
        for thread in self.multithreading_threads:
            thread.join()
    def parsemildlist(self):
        if self.multithreading:
            # Use queued method to multithread
            Generate = self.generatequeue
        else:
            # Use common way to build, in order, but the order still presents if you execute Generate multiple times
            Generate = self.generate
        Sync = self.sync
        SetCompiler = self.setcompiler
        try:
            mildlist = open(self.mildfile+self.mildprefix, "r")
        except:
            print("mild: no mildlists found")
            print("mild: no targets")
            exit(1)
        starttime = time.time()
        for line in mildlist:
            exec(line)
        if self.multithreading:
            # Wait for all threads to end
            for process in self.multithreading_threads:
                process.join()
        endtime = time.time()
        termcolor.cprint("mild: done processing target {} in {} seconds".format(self.mildfile, str(round(endtime-starttime, 2))), "green")
if __name__ == "__main__":
    print("mild Copyright (C) 2020  Mark Hargreaves\nThis program comes with ABSOLUTELY NO WARRANTY;\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; see LICENSE.txt for details")
    args = sys.argv[1:]
    multithreadstate = 0
    asyncthreads = 0
    if "-M" in args:
        multithreadstate = 1
    if "--async" in args:
        asyncthreads = 1
    mild = MildCC("mild", multithreadstate, asyncthreads)
    mild.parsemildlist()
    exit(0)
