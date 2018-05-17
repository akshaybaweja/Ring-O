import applescript
import urllib2

script=''' 
on volumeUp()
   set curVolume to output volume of (get volume settings)
   
    if curVolume < 75 then
       set newVolume to curVolume + 25
    else
       set newVolume to 100
    end if

   set volume output volume newVolume
end volumeUp

on volumeDown()

   set curVolume to output volume of (get volume settings)
   
    if curVolume > 25 then
       set newVolume to curVolume - 25
    else

       set newVolume to 1
    end if

   set volume output volume newVolume
end volumeDown

on volumeMute()
  
   set isMuted to output muted of (get volume settings)
   
   set newMuted to not isMuted
   
   set volume output muted newMuted
end volumeMute 

on nextSlide()

    tell application "Keynote"
        show next
    end tell
end nextSlide

on play()

    if application "iTunes" is running then
	    tell application "iTunes"
		    playpause
	    end tell
    end if
end play

on skip()

    if application "iTunes" is running then
	    tell application "iTunes"
		    next track
	    end tell
    end if
end skip
'''

scpt = applescript.AppleScript(script)

def gesture_callback(gesture):
    returntext = ""
    if gesture == "a":
        scpt.call('volumeMute')
        returntext = "Mute/Unmute"
    elif gesture == "b":
        scpt.call('volumeUp')
        returntext = "Volume Up"
    elif gesture == "c":
        scpt.call('volumeDown')
        returntext = "Volume Down"
    elif gesture == "d":
        scpt.call('skip')
        returntext = "Skip Song"
    elif gesture == "e":
        togglebulb()
        returntext = "Toggle Bulb"
    return returntext

def togglebulb():
    tplink_bulb = "https://maker.ifttt.com/trigger/tplink/with/key/eKnKGaJb-sA33WzfgucqzxT-j0nyZDTPXPllo52S2Bh"
    content = urllib2.urlopen(tplink_bulb).read()
