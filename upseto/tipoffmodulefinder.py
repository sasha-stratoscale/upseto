import modulefinder
import sys
import os
from upseto import pythonnamespacejoin


def fileIsUpsetoPythonNamespaceJoinInit(filename):
    if os.path.basename(filename) != "__init__.py":
        return False
    with open(filename) as f:
        condensedContents = f.read().replace(" ", "").replace("\t", "")
    if '__path__.extend(upseto.pythonnamespacejoin.join(' not in condensedContents:
        return False
    return True


class TipOffModuleFinder:
    def __init__(self):
        self._todo = []
        self._visited = set()
        for path in sys.path:
            if not path.startswith("/usr/lib"):
                self._todo.append((path, []))
        while not len(self._todo) == 0:
            path, relativeModule = self._todo.pop(0)
            self._scan(path, relativeModule)

    def _scan(self, path, relativeModule):
        if relativeModule and str(relativeModule) in self._visited:
            return
        self._visited.add(str(relativeModule))
        if path == "":
            path = "."
        for root, dirs, files in os.walk(path):
            for directory in list(dirs):
                fullPath = os.path.join(root, directory)
                initFile = os.path.join(fullPath, "__init__.py")
                if not os.path.isfile(initFile):
                    dirs.remove(directory)
            for filename in files:
                fullPath = os.path.join(root, filename)
                if not fileIsUpsetoPythonNamespaceJoinInit(fullPath):
                    continue
                submodule = root[len(path) + len(os.path.sep):].split(os.path.sep)
                absoluteModuleNameSplit = relativeModule
                if submodule != ['']:
                    absoluteModuleNameSplit = submodule
                absoluteModuleName = ".".join(absoluteModuleNameSplit)
                joinPaths = pythonnamespacejoin.Joiner(fullPath, absoluteModuleName).found()
                for joinPath in joinPaths:
                    modulefinder.AddPackagePath(absoluteModuleName, joinPath)
                    self._todo.append((joinPath, absoluteModuleNameSplit))
