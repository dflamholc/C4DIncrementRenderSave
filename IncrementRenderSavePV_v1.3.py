
"""
Name-US: IncrementRenderSavePV_v1.2 29-10-2016
Description-US: Saves the current document and renders it to Picture Viewer, 
then incrementing the document name and opening it.
Author: David Flamholc
"""
# IncrementRenderSave version Variable
irs_v = "IncrementRenderSavePV_v1.2"

"""
LICENSE
-------
    Copyright (c) 2016, David Flamholc, VFXVoodoo.com
    Programming: David Flamholc <dflamholc@gmail.com>

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
    WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
    COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


CHANGE LOG
----------
    v0.01
    Inital version. Files increment then save a new version which is sent to render.

    v0.02
    Change so that the current state of the file is saved first and then incremented and send to picture viewer.

    v1.1
    Current document now closes as soon as rendering starts.
    And the cloned new document gets assigned path and a name and is inserted into the C4D document list.

    v1.2
    When the script runs the first itme it creates a "___RenderWIP" folder where it stores a specified amount of files.
    
    v1.3
    When the script runs the first time it creates .NFO files in the original directory which lets the user control
    the amount of incremets in the "___RenderWIP" folder. Once the file amount number is reached the oldest file by date is deleted.
    If the number is changed, more files can be allowed, but a number lower than the current amount of files in the folder, will NOT 
    delete those previously saved files. Only 1 (the oldest file) at a time will be deleted when the script runs.


INSTRUCTIONS & DEV NOTES
------------------------
Mainly intended for render test and optimisation purposes where small changes are made and the need to backtrack to a specific scenefile could be crucial.

TO DO -- FEATURE IDEAS
-----------------------
    [x] Write script comments
    [x] Create Icon
    [x] Write Usage Instructions
    [] Create interface on first run
        [] alternative "___RenderWIP" name
        [] set amount of saved files
    [] Convert to Plugin
        [] Get Unique ID


Threads that helped:
--------------------
http://www.plugincafe.com/forum/forum_posts.asp?TID=10796
https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d.documents/index.html#c4d.documents.SaveDocument
http://forums.cgsociety.org/archive/index.php?t-921256.html
Thanks to Niklas Rosenstein & Michael Auerswald for parts of their freely available scripts that I've found online.
"""

import c4d, os, datetime
from c4d import gui

######################################################################################
currentTime = datetime.datetime.strftime(datetime.datetime.now(), '%m/%d/%Y %H:%M:%S')
# FUNCTIONS ############################################################

def findDigits(path):
    if os.path.isdir(path):
        tokenText = path
        ext = None
    else:
        tokenText, ext = os.path.splitext(path)
        print tokenText
        print ext

    tokenReverse = tokenText[::-1]

    tokenString = ""
    tokenNumber = 0
    beginTokenString = False

    for letter in tokenReverse:
        if letter.isdigit() is True:
            beginTokenString = True
            tokenString += letter
        else:
            if beginTokenString is True:
                tokenString = tokenString[::-1]
                tokenNumber = int(tokenString)
                break

    return tokenReverse, tokenNumber, tokenString, ext


def createNewDir(currPath, currName, folderToken):
    # create directory name based on the current file name split at "_v"
    newDirName = currName.split('_v', 1)
    newDir = newDirName[0] + folderToken
    newDirPath = currPath + os.sep + newDir

    if not os.path.isdir(newDirPath):
        os.makedirs(newDirPath)

    print ("The new save directory is: {0}").format(newDirPath)
    
    return newDirPath


def addTexPath(currPath):
    found = False
    for i in range(10):
        path = c4d.GetGlobalTexturePath(i)

        if currPath in path:
            print "Tex Path Found"
            found = True

    if (not found):
        freeslot = -1

        for i in range(10):
            path = c4d.GetGlobalTexturePath(i)
            if (path == ""):
                print "first free slot is: ", i
                freeslot = i
                break

        if (freeslot == -1):
            gui.MessageDialog('No texture slots available.')
        else:
            globalTexturePath = currPath + os.sep + "tex"
            print "Global Texture Path: " + globalTexturePath

            c4d.SetGlobalTexturePath(freeslot, globalTexturePath)
            c4d.EventAdd()


def addfileAmountNFO(fileAmount, currPath, currName):
    nfoNameOnly = currName.split('_v', 1)
    nfoName = nfoNameOnly[0] + ".nfo"
    nfoPath = currPath + os.sep + nfoName 
    #check if the .nfo exists or not
    if not os.path.exists(nfoPath):
        n = open(nfoPath, "a")
    else:
        n = open(nfoPath, "w")

    n.write("="*75 + "\n"
            + "IncrementRenderSave Script by vfxvoodoo.com\n"
            + "Scene file amount control for document: " + nfoNameOnly[0] + "\n"
            + "\nThis .NFO file is saved here:\n"
            + currPath + "\n"
            + "at: %s\n" %currentTime
            + "="*75 + "\n" + "\n"
            + "\n" + "Here you can change the amount of increments that are saved before the oldest copy gets deleted."
            + "\n" + "Make sure you enter a two digit number and no trailing spaces! "
            + "\n" + "Max file increment amount: " + str(fileAmount))

    n.close()


def saveRenderClone(currDoc, fullPathCurr, currPath, currName, fileAmount, folderToken):
    if currPath.endswith(folderToken): # then our current folder is our save folder
        savePath = currPath
        fullPathSave = fullPathCurr
        nfoNameOnly = currName.split('_v', 1)
        nfoName = nfoNameOnly[0] + ".nfo"
        nfoPath = os.path.dirname(savePath) + os.sep + nfoName 
        with open(nfoPath, 'r') as f:
            f.seek(-2, 2)
            fileAmountNew = f.read()
        fileAmount = fileAmountNew
    else:
        gui.MessageDialog(
            "IncremenRenderSave by vfxvoodoo.com \\\(c)2016// David Flamholc\n"
            + "\nWELCOME! This is the first time you're running this script ;)\n"
            + "\nINSTRUCTIONS: \n"
            + "The first time you run this script on a document, it will create a new folder \n"
            + "in your current directory and start saving new incremented versions of this \n"
            + "current file there."
            + "\nYour original file will be left where it is and next to it a .NFO file will be saved,\n"
            + "inside which you can decide how many increments are allowed to be saved \n"
            + "before the oldest one is deleted.\n"
            + "\nThe way this script works: \n"
            + "When you press render the current file is sent to render, then saved and closed. \n"
            + "After this a clone of the document is opened and incremented, \n"
            + "resulting in that the file rendering is the closed file and that file name with \n"
            + " corresponding version number can be found in the picture viewer image list."
            + "\n" + "\n" + "IMPORTANT:  The original file name must have a '_v0#' somewhere in the name.")
        # if we can't find the token in the path name then create the new render folder
        addTexPath(currPath) # we are moving into a new directory so we we add a global tex path
        savePath = createNewDir(currPath, currName, folderToken)
        fullPathSave = savePath + os.sep + currName
        # add the text file, containing the desired fileAmount, to the new directory
        addfileAmountNFO(fileAmount, currPath, currName)

        print ("The new full path to the document is: {0}").format(fullPathSave)

    # Now we save the CURRENT doc with a conditional statement to check for errors
    if c4d.documents.SaveDocument(doc, fullPathSave, saveflags=c4d.SAVEDOCUMENTFLAGS_0, format=c4d.FORMAT_C4DEXPORT):
        # and start the RENDER
        c4d.CallCommand(12099)
        # or start Render Region
        #c4d.CallCommand(12165, 12165)

        # because we have saved into a new directory we have to set the NEW path and CURRENT name for the CURRENT doc 
        doc.SetDocumentPath(savePath)
        doc.SetDocumentName(currName)
        print ("Saved and Rendered as document: {0}").format(fullPathSave)
    else:
        print "Error whilst saving document: " + currPath
        gui.MessageDialog('Error whilst saving document: ' + currPath)
        doc.SetDocumentPath(currPath)
        doc.SetDocumentName(currName)

    # create a clone of the current doc before we close it - this clone will be incremented
    cloneDoc = currDoc.GetClone()
    # then kill the current doc and free up that memory
    c4d.documents.KillDocument(currDoc)
    print ("The rendered document: {0}, has been closed.").format(currName)
    
    return savePath, cloneDoc, fileAmount


def incrementVersion(savePath, cloneDoc, tokenReverse, tokenNumber, tokenString, ext):
    tokenNumber += 1
    tokenStringNew = str(tokenNumber).zfill(len(tokenString))
    tokenReverse = tokenReverse.replace(tokenString[::-1], tokenStringNew[::-1], 1)
    cloneVersionPath = tokenReverse[::-1] + ext
    # split the new full path
    oldPath, newVersionName = os.path.split(cloneVersionPath)
    # set the path for the cloned doc
    cloneDoc.SetDocumentPath(savePath)
    # rename the cloned doc with the incremented name 
    cloneDoc.SetDocumentName(newVersionName)
    # insert the cloned doc in c4d document list
    c4d.documents.InsertBaseDocument(cloneDoc)


def limitVersions(fileAmount, savePath):
    mtime = lambda f: os.stat(os.path.join(savePath, f)).st_mtime
    savedFileList = list(sorted(os.listdir(savePath), key=mtime))
    fileAmountNr = int(fileAmount)

    if len(savedFileList) > fileAmountNr:
        os.remove(savePath + os.sep + savedFileList[0])


# MAIN C4D PYTHON FUNCTION ############################################################

def main():
    # return the current document, path and filename.ext
    currDoc = c4d.documents.GetActiveDocument()
    currPath = currDoc.GetDocumentPath()
    currName = currDoc.GetDocumentName()

    # create the full filepath including extension 
    fullPathCurr = currPath + os.sep + currName

    # create initial variable for the max file version amount
    fileAmount = 10
    folderToken = "___RenderWIP"

    if not currPath: #check if we've saved the document scene file
        gui.MessageDialog("Please save your scene before running this script.")
        return False   
    else:
        # run the save - render - clone function and unpack return tuples
        savePath, cloneDoc, fileAmount = saveRenderClone(currDoc, fullPathCurr, currPath, currName, fileAmount, folderToken)

        # run the find digits function and unpack the return tuples
        tokenReverse, tokenNumber, tokenString, ext = findDigits(fullPathCurr)

        # run the increment version function
        incrementVersion(savePath, cloneDoc, tokenReverse, tokenNumber, tokenString, ext)
        
        print "outside limit version :", fileAmount
        # reading the token last in the file folder path
        limitVersions(fileAmount, savePath)

if __name__=='__main__':
    main()
