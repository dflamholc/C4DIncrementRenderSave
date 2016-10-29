**# C4DIncrementRenderSave**
Script for Cinema 4D that saves and renders current doc, then closes it and opens an incremented clone.

 
_author:_ __vfxvoodoo.com // David Flamholc__

_email:_ __dflamholc@gmail.com__

 
__Version LOG__

_Initial release 22-10-2016_

-- IncrementRenderSavePV_v1.1

-- IncrementRenderSaveRgn_v1.1

-- IcrementRenderSavePV_v1.3
	- Implemented creation of a subfolder which all incremented versions are saved into.
	- Implemented creation of a .nfo file where the user can set the desired number of incremented files to be kept in the subfolder,
	before the oldest one by date/time will be deleted.

 
__DESCRIPTIOIN & INTENDED USE__

A script for Cinema 4D that will save the current doc and render it in the Picture Viewer or preparing for a Region Render. After render starts the doc will be closed, and a clone of the document will be incremented and made ready for edit.

This way the current render file-name in the picture viewer will correspond to recenlty saved file.

The idea of this script is to facilitate render tests, where its easy to backtrack to a previous image stored in the Picture Viewer, as there will be a c4d document saved with that exact name.

__TODO LIST:__

[x] Create subfolder to saved docs as the amount increments can grow out of comfort zone

[] Create GUI with options to keep only a defined number of copies

[] Option to delete those copies once render tests are done


 

ends...
