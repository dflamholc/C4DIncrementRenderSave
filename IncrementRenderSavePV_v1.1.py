
"""
Name-US: IncrementRenderSavePV_v1.1 22-10-2016
Description-US: Saves the current document and renders it to Picture Viewer, 
then incrementing the document name and opening it.
Author: David Flamholc

USAGE:
Mainly intended for render test and optimisation purposes where small changes are made and the need to backtrack to a specific scenefile could be crucial.

CHANGE LOG:
    v0.01
    Inital version. Files increment then save a new version which is sent to render.

    v0.02
    Change so that the current state of the file is saved first and then incremented and send to picture viewer.

    v1.1
    Current document now closes as soon as rendering starts.
    And the cloned new document gets assigned path and a name and is inserted into the C4D document list.

Threads that helped:
http://www.plugincafe.com/forum/forum_posts.asp?TID=10796
https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d.documents/index.html#c4d.documents.SaveDocument
http://forums.cgsociety.org/archive/index.php?t-921256.html

Thanks to:
Niklas Rosenstein & michael@flipswitchingmonkey.com for parts of their freely available scripts that I've found online.
"""

import c4d, os

def incrementDoc(fullPathCurr):
    # get the full current path and split it on name and extension
    fn, ext = os.path.splitext(fullPathCurr)
    
    # reverse the name string
    fnreverse = fn[::-1]

    # initialise variables
    versionString = ""
    versionNumber = 0
    beginVersionString = False

    # loop through the reversed name string
    for letter in fnreverse:
        # check if the index is a digit
        if letter.isdigit() is True:
            # begin collecting letters into the predefined empty string
            beginVersionString = True
            versionString += letter
            # print the current digit
            print("Digit: {0}").format(letter)
        else:
            # if the current index is not a digit
            print("Non-Digit: {0}").format(letter)
            # check if versionString collecting has begun
            if beginVersionString is True:
                # reverse string
                versionString = versionString[::-1]
                # grab the version number
                versionNumber = int(versionString)
                # first non-digit ends version string
                break
            
    # incrment the version number variable
    versionNumber += 1
    # since leading zeros will be ignored by int() we now fill out the zeros again using zfill()
    versionStringNew = str(versionNumber).zfill(len(versionString))
    
    # take the orignally reversed name string and replace the old versionString-part in reverse with the new one
    fnreverse = fnreverse.replace(versionString[::-1], versionStringNew[::-1], 1)
    # create a new full path with extension
    fullPathNew = fnreverse[::-1] + ext

    # print out some useful messages
    print ("Increased version {0} to {1}").format(versionString, versionStringNew)
    print ("Changed path {0} to {1}").format(fullPathCurr, fullPathNew)

    # return the new full path
    return fullPathNew

# function that gets current path and current name of the document
def cloneDoc(currDoc):

    # get the current path
    currPath = currDoc.GetDocumentPath()
    # get the current document name
    currName = currDoc.GetDocumentName()
    
    fullPathCurr = currPath + os.sep + currName

    # conditional statement to save the CURRENT document and check for errors
    if c4d.documents.SaveDocument(doc, fullPathCurr, saveflags=c4d.SAVEDOCUMENTFLAGS_0, format=c4d.FORMAT_C4DEXPORT):
        # render to PV
        c4d.CallCommand(12099)
        # or start Render Region
        # c4d.CallCommand(12165, 12165)
        print("Saved and Rendered as document: {0}").format(fullPathCurr)
    else:
        print "Error whilst saving document: " + currPath
        gui.MessageDialog('Error whilst saving document: ' + currPath)
        doc.SetDocumentPath(currPath)
        doc.SetDocumentName(currName)

    # call the increment function and assign the return value to a variable
    fullPathNew = incrementDoc(currPath + os.sep + currName)
    
    # split the new full path
    newPath, newName = os.path.split(fullPathNew)
    
    # clone the current doc
    nextDoc = currDoc.GetClone()
    # then kill the current doc and free up that memory
    c4d.documents.KillDocument(currDoc)
    print "Current " + currName + " Document Closed."
    
    # set the path for the cloned doc
    nextDoc.SetDocumentPath(newPath)
    # rename the cloned doc with the incremented name 
    nextDoc.SetDocumentName(newName)
    # insert the cloned doc in c4d document list
    c4d.documents.InsertBaseDocument(nextDoc)

   
def main():
    # return the current document
    currDoc = c4d.documents.GetActiveDocument()
    
    # print str(currDoc)
    cloneDoc(currDoc)

    # force C4D update - not sure necessary
    c4d.EventAdd()

if __name__=='__main__':
    main()
