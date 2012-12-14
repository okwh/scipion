#!/usr/bin/env xmipp_python
#------------------------------------------------------------------------------------------------
# Protocol for random conical tilt reconstruction
#
# Example use:
# ./xmipp_protocol_rct.py
#
# Author: Sjors Scheres, March 2007
#
from os.path import join, exists
from xmipp import MetaData, getBlocksInMetaDataFile, MDL_IMAGE, MDL_IMAGE_TILTED, MDL_REF,\
MDL_MICROGRAPH, MDL_MICROGRAPH_TILTED, LEFT_JOIN, MD_APPEND

from protlib_base import *
from protlib_utils import getListFromRangeString, runJob, runShowJ

class ProtRCT(XmippProtocol):
    def __init__(self, scriptname, project):
        XmippProtocol.__init__(self, protDict.rct.name, scriptname, project)
        self.Import = 'from protocol_rct import *'
        self.ExtractDir = getWorkingDirFromRunName(self.ExtractionRun)        

    def defineSteps(self):
        pickingDir = getWorkingDirFromRunName(self.ExtractionRun)
        self.insertStep("createLink2",filename="acquisition_info.xmd",dirSrc=pickingDir,dirDest=self.WorkingDir)

        classSelection = getListFromRangeString(self.SelectedClasses)
        self.insertStep('gatherPairs',verifyfiles=[self.getFilename('classes')],
                               WorkingDir=self.WorkingDir,ClassSelection=classSelection,
                               ClassFile=self.ClassifMd, ExtractDir=self.ExtractDir,
                               PickingDir=pickingDir)
        
        mdClasses = MetaData("classes@" + self.ClassifMd)
        hasImage = mdClasses.containsLabel(MDL_IMAGE)
        
        for classId in mdClasses:
            classNo = mdClasses.getValue(MDL_REF, classId)
            if classNo in classSelection:
                # Locate class representative
                classImage = ""
                if hasImage:
                    classImage = mdClasses.getValue(MDL_IMAGE, classId)                    
                classNameIn = "class%06d_images@%s" % (classNo, self.workingDirPath("classes.xmd"))
                classNameOut = self.workingDirPath("rct_%06d.xmd" % classNo)
                classVolumeOut = self.workingDirPath("rct_%06d.vol" % classNo)
                self.insertParallelStep('reconstructClass',verifyfiles=[classNameOut, classVolumeOut],
                                   WorkingDir=self.WorkingDir,
                                   ClassNameIn=classNameIn, ClassNameOut=classNameOut,
                                   ClassImage=classImage,
                                   CenterMaxShift=self.CenterMaxShift,
                                   ThinObject=self.ThinObject,
                                   SkipTiltedTranslations=self.SkipTiltedTranslations,
                                   ClassVolumeOut=classVolumeOut,
                                   ReconstructAdditionalParams=self.ReconstructAdditionalParams,
                                   DoLowPassFilter=self.DoLowPassFilter,LowPassFilter=self.LowPassFilter)
#                else:
#                    self.Log.error("Cannot find representative for class %d"%classNo)
                
    def summary(self):
        message = []
        classSelection = getListFromRangeString(self.SelectedClasses)
        message.append("Random conical tilt reconstruction of %d classes of %s" % (len(classSelection), self.ClassifMd))
        import glob
        reconstructedFiles=glob.glob(self.WorkingDir+"/rct_??????.vol")
        if not reconstructedFiles:
            message.append("No reconstruction has been generated")
        else:
            message.append(str(len(reconstructedFiles))+" reconstructions have finished")
        return message
    
    def validate(self):
        errors = []
        classSelection = getListFromRangeString(self.SelectedClasses)
        blocks = getBlocksInMetaDataFile(self.ClassifMd)
        print "extraction run: ", self.ExtractionRun
        self.ExtractDir = getWorkingDirFromRunName(self.ExtractionRun)
        
        for classNo in classSelection:
            blockName = "class%06d_images" % classNo
            if not blockName in blocks:
                errors.append("%s cannot be found at %s" % (blockName, self.ClassifMd))
        if self.CenterMaxShift > 100 or self.CenterMaxShift < 0:
            errors.append("Maximum shift must be in the range 0-100")
        if self.LowPassFilter > 0.5 or self.LowPassFilter < 0:
            errors.append("Low pass filter must be in the range 0-0.5")
        
        print "extract dir: ", self.ExtractDir
        files = [getImagesFilename(self.ExtractDir, s) for s in ['', 'untilted', 'tilted']]
        files.append(getProtocolFilename('tilted_pairs', WorkingDir=self.ExtractDir))
        
        for f in files:
            if not exists(f):
                errors.append("Cannot find file: %s" % f)
        
        return errors    

    def visualize(self):
        classSelection = getListFromRangeString(self.SelectedClasses)
        for classNo in classSelection:
            fnVol=self.workingDirPath("rct_%06d.vol"%classNo)
            if exists(fnVol):
                runShowJ(fnVol)

def gatherPairs(log,WorkingDir,ClassSelection,ClassFile,ExtractDir,PickingDir):

    mdImages = getImagesMd(ExtractDir)    
    mdTiltAngles = MetaData(getProtocolFilename("tilted_pairs", WorkingDir=PickingDir))

    mdU = getImagesMd(ExtractDir, "untilted")
    mdUAux = MetaData()
    mdUAux.setColumnValues(MDL_IMAGE,mdU.getColumnValues(MDL_IMAGE))
    mdUAux.setColumnValues(MDL_MICROGRAPH,mdU.getColumnValues(MDL_MICROGRAPH))

    mdT = getImagesMd(ExtractDir, "tilted")
    mdTAux = MetaData()
    mdTAux.setColumnValues(MDL_IMAGE_TILTED,mdT.getColumnValues(MDL_IMAGE))
    mdTAux.setColumnValues(MDL_MICROGRAPH_TILTED,mdT.getColumnValues(MDL_MICROGRAPH))

    mdJoin1 = MetaData()
    mdJoin2 = MetaData()
    mdJoin3 = MetaData()
    mdJoin4 = MetaData()
    fnOut = getProtocolFilename('classes', WorkingDir=WorkingDir)
    for classNo in ClassSelection:
        MDclass = MetaData(getClassBlock(classNo, ClassFile))
        mdJoin1.join(MDclass,mdImages,MDL_IMAGE,MDL_IMAGE,LEFT_JOIN)
        mdJoin2.join(mdJoin1,mdUAux, MDL_IMAGE,MDL_IMAGE,LEFT_JOIN)
        mdJoin3.join(mdJoin2,mdTAux, MDL_IMAGE_TILTED,MDL_IMAGE_TILTED,LEFT_JOIN)
        mdJoin4.join(mdJoin3,mdTiltAngles,MDL_MICROGRAPH,MDL_MICROGRAPH,LEFT_JOIN)
        mdJoin4.write(getClassBlock(classNo, fnOut), MD_APPEND)

def reconstructClass(log,WorkingDir,ClassNameIn,ClassNameOut,ClassImage,
                     CenterMaxShift,ThinObject,SkipTiltedTranslations,ClassVolumeOut,
                     ReconstructAdditionalParams,DoLowPassFilter,LowPassFilter):
    # If class image doesn't exists, generate it by averaging
    if len(ClassImage) == 0:
        classRootOut = ClassNameOut.replace(".xmd", "") + "_"
        params = "-i %(ClassNameIn)s --save_image_stats %(classRootOut)s -o %(WorkingDir)s/stats.xmd" % locals()
        runJob(log, "xmipp_image_statistics", params)
        ClassImage = classRootOut + "average.xmp"
        
    params = "-i %(ClassNameIn)s -o %(ClassNameOut)s --ref %(ClassImage)s --max_shift %(CenterMaxShift)d" % locals()
    
    if ThinObject:
        params += " --do_stretch"
    
    if SkipTiltedTranslations:
        params += " --do_not_align_tilted"
    
    runJob(log, "xmipp_image_align_tilt_pairs", params)
    
    params = "-i %(ClassNameOut)s -o %(ClassVolumeOut)s %(ReconstructAdditionalParams)s" % locals()
    runJob(log, "xmipp_reconstruct_fourier", params)
    
    if DoLowPassFilter and exists(ClassVolumeOut):
            filteredVolume = ClassVolumeOut.replace('.vol','_filtered.vol')
            params = "-i %(ClassVolumeOut)s -o %(filteredVolume)s --fourier low_pass %(LowPassFilter)f" % locals()
            runJob(log,"xmipp_transform_filter", params)
