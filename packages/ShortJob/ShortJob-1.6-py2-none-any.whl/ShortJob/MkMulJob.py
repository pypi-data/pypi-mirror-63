#!/usr/bin/env python
# ====================================================
#   Copyright (C)2019 All rights reserved.
#
#   Author        : Xin-Xin MA
#   Email         : xxmawhu@163.com
#   File Name     : MkMulJob.py
#   Created Time  : 2019-10-30 18:29
#   Last Modified : 2019-12-30 20:16
#   Describe      :
#
# ====================================================
import os
from ShortJob import command

class MkMulJob(object):
    def __init__(self, cppList=["fit.cxx"]):
        self._cppList = cppList
        self._cwd = os.getcwd()

    def Make(self, indx, varList=[], logName=[]):
        if len(logName) != len(self._cppList) and len(logName) > 0:
            print("check the length")
            return
        if len(logName) == 0:
            for i in self._cppList:
                logName.append(i.split('.')[0])

        f = open("job_%d.sh" % (indx), 'w')
        f.write("cd %s\n" % (self._cwd))
        f.write("cd .. \n")
        for i in range(len(varList)):
            f.write(self.GetCommands(indx, self._cppList[i], varList[i],
                                     logName[i])+"\n")
        f.close()

    def GetCommands(self, index, cpp, var=[], logName="txt"):
        fileType = cpp.split('.')[-1]
        log = "log" + str(index) + "." + logName
        if fileType in command.rootType and fileType != "":
            if len(var) == 0: 
                commands = "{exe} {file} > {jobpath}/{Log}".format(
                           exe = command.exe[fileType],
                           file = cpp,
                           jobpath = self._cwd.split("/")[-1],
                           Log = log)
                return commands
            else:
                commands = "{exe} '{file}({Var})' > {jobpath}/{Log}".format(exe = command.exe[fileType],
                           file = cpp,
                           jobpath = self._cwd.split("/")[-1],
                           Log = log,
                           Var = ",".join(self._getVarList(var)))
                return commands
        commands = "{exe} {file} {Var} > {jobpath}/{Log}".format(exe = command.exe[fileType],
                           file = cpp,
                           jobpath = self._cwd.split("/")[-1],
                           Log = log,
                           Var = " ".join(var)
                            )
        return commands

    def _getVarList(self, varList):
        vList = []
        for i in varList:
            if isinstance(i, int) or isinstance(i, float):
                vList.append(str(i))
            else:
                vList.append('"{}"'.format(i))
        return vList

    def Str(self, s):
        return s
        st = ""
        for i in s:
            print(i)
            if i == "<" or i == ">" or i == "|":
                st += '\\' + i
            else:
                st += i
        return st
