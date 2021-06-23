# fMRI visual presentations utility functions 

def fliptiming(mriparams: dict =None) -> dict:
    pass
    #return mri

def cleanup(mriparams: dict =None) -> dict: 
    # clean up function after presentation all data
    pass
    #return mri
    

def presetup(mriparams: dict =None) -> dict:
    # setup before stimulus presentation
    pass
    # return mri



def setupeyelinkmri(winsize, eyeLinkAddress='100.0.0.1', filename='test.edf'):
    '''
    Eyelink setup before stimulus presentation in fMRI exp

    <winsize>: (width, height) window size
    <tk>: pylink object
    '''

    import pylink as pl
    width, height = winsize
    # connect to machine
    try:
        tk = pl.EyeLink(eyeLinkAddress) # connect to eyelink
    except:
        ConnectionError('Cannot link to Eyelink')
    
    tk.sendCommand("add_file_preamble_text 'Recorded by EyelinkToolbox Visual_tracking task'")
    
    print(f'Pixel size of window is width: {width}, height: {height} \n')
    tk.sendCommand(f'screen_pixel_coords = 0 0 {width-1} {height-1}')
    tk.sendMessage(f'DISPLAY_COORDS 0 0 {width-1} {height-1}')
    tk.sendCommand('calibration_type = HV9')
    tk.sendCommand('active_eye = LEFT')
    tk.sendCommand('automatic_calibration_pacing = 1500')
    
    # setup data formate
    tk.sendCommand('file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON')
    tk.sendCommand('file_sample_data  = LEFT,RIGHT,GAZE,HREF,AREA,GAZERES,STATUS')
    tk.sendCommand('link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON')
    tk.sendCommand('link_event_data  =  LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT')
    
    # open eye data
    tk.openDataFile(filename+'edf') # open data file

    checkcalib = input('Do you want to do a calibration (0=no, 1=yes)? ','s');
    if checkcalib:
        print('Please perform calibration. When done, the subject should press a button') 
        pl.openGraphics() #??
        tk.doTrackerSetup() # do eye calibration
        #  EyelinkDoDriftCorrection(el);
    print('Button detected from subject. Starting recording of eyetracking data. Proceeding to stimulus setup.\n')
    tk.startRecording(1, 1, 1, 1)  # 1,1,1,1是什么意思？？
    
    return tk


def closeupeyelinkmri(tk, outputfile=None):
    '''
    <tk>: pylink object created in setupeyelink
    <outputfile>
    '''
    import pylink as pl
    tk.stopRecording()
    tk.closeDataFile()
    tk.receiveDataFile(outputfile, outputfile)
    tk.close()
    pl.closeGraphics()
    


