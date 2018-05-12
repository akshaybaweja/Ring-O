import applescript

script=''' 
on volumeUp()
   set curVolume to output volume of (get volume settings)
   
    if curVolume < 90 then
       set newVolume to curVolume + 10
    else
       set newVolume to 100
    end if

   set volume output volume newVolume
end volumeUp

on volumeDown()

   set curVolume to output volume of (get volume settings)
   
    if curVolume > 10 then
       set newVolume to curVolume - 10
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
'''

scpt = applescript.AppleScript(script)

def gesture_callback(gesture):
    returntext = ""
    if gesture == "a":
        scpt.call('volumeMute')
        returntext = "Muted."
    elif gesture == "b":
        scpt.call('volumeUp')
        returntext = "Volume Up by 10"
    elif gesture == "c":
        scpt.call('volumeDown')
        returntext = "Volume Down by 10"
    elif gesture == "d":
        scpt.call('nextSlide')
        returntext = "Next Slide"
    
    return returntext
