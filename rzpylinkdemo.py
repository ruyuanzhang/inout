# 

from psychopy import visual, core
import pylink as pl

wantEyetrack = True
filename = 'test.edf'

win = visual.Window([1074, 768])

stim = visual.GratingStim(win=win, units='norm', size=5)

width, height = win.size

#------- setup -----------------
if wantEyetrack:
    try:
        tk = pl.EyeLink('100.1.1.1') # connect to eyelink
    except:
        raise ConnectionError('Cannot link to Eyelink')
        core.quit()
    
    tk.openDataFile(filename) # open data file
    # initial setup
    tk.sendCommand("add_file_preamble_text 'Recorded by EyelinkToolbox Visual_tracking task'") # error 1
    tk.sendCommand("sample_rate 1000")
    tk.sendCommand(f'screen_pixel_coords = 0 0 {width-1} {height-1}')
    tk.sendMessage(f'DISPLAY_COORDS 0 0 {width-1} {height-1}')
    tk.sendCommand('calibration_type = HV9')
    
    # setup data format
    tk.sendCommand('file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON')
    tk.sendCommand('file_sample_data  = LEFT,RIGHT,GAZE,HREF,AREA,GAZERES,STATUS')
    tk.sendCommand('link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON')
    tk.sendCommand('link_event_data  =  LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT')
    
    # calibration
    pl.openGraphics() #??
    tk.doTrackerSetup() # do eye calibration


if wantEyetrack:
    tk.startRecording(1, 1, 1, 1)

stim.draw()
win.flip()
core.wait(10)


if wantEyetrack:
    tk.stopRecording()
    tk.closeDataFile()
    tk.receiveDataFile(filename, filename)
    tk.close()
    pl.closeGraphics()