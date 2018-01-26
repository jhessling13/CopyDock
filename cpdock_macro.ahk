; AutoHotkey script for CopyDock integration
;
; Hotkeys:
;
;  Control+Shift+c -> Send "copy" single to currently active window, focus CopyDock window and move to mouse cursor, add copied item to CopyDock
;  Control+Shift+x -> Focus CopyDock window, move to mouse cursor.  Each "x" key scrolls through the Dock, highlighted item added when Control or Shift is released.
;  Control+Shift+Space -> Focus CopyDock window and move to mouse cursor if not already focused.  If CopyDock window focused, minimize it.
;  Control+Shift+MouseWheel -> Focus CopyDock window and move to mouse cursor, scroll through Docked items
;  Control+Shift+v -> If CopyDock window in focus, "pick" currently highlighted Dock item and add to system clipboard, minimize CopyDock


#InstallKeybdHook
SetKeyDelay, 50, 1
^+c::
   SetTitleMatchMode, 1
   IfWinExist, ahk_exe cpd_launch.exe
   {
      Send, ^c
      IfWinNotActive, ahk_exe cpd_launch.exe
      {
         CoordMode, Mouse, Screen
         MouseGetPos, xMousePos, yMousePos
         WinGetPos,,, cpdWidth, cpdHeight, ahk_exe cpd_launch.exe
         ControlGetPos, cListX, cListY, cListWidth, cListHeight, TkChild20, ahk_exe cpd_launch.exe
         winactivate, ahk_exe cpd_launch.exe
         WinWaitActive, ahk_exe cpd_launch.exe
         BlockInput, On
         WinMove, ahk_exe cpd_launch.exe,, (xMousePos - cListX - (cListWidth/2)), (yMousePos - cListY - (cListHeight/2))
         ;Sleep, 20
         BlockInput, Off
         Send, ^m
         WinMinimize, ahk_exe cpd_launch.exe
      }
      Else
      {
         Send, ^m
         ;WinMinimize, ahk_exe cpd_launch.exe
      }

      ;Removed the interaction loop below.  too much lag, is very interruptive.
      ;Loop
      ;{
         ;controlIsDown := GetKeyState("Control")
         ;shiftIsDown := GetKeyState("Shift")
         ;xIsDown := GetKeyState("x")
         ;if xIsDown
         ;{
            ;Send, ^u
         ;}
         ;Sleep, 50
      ;}
      ;Until !controlIsDown or !shiftIsDown

      ;WinMinimize, ahk_exe cpd_launch.exe
      Return
   }
   Return

#InstallKeybdHook
SetKeyDelay, 50, 1
^+d::
   SetTitleMatchMode, 1
   IfWinExist, ahk_exe cpd_launch.exe
   {
      Send, ^c
      IfWinNotActive, ahk_exe cpd_launch.exe
      {
         CoordMode, Mouse, Screen
         MouseGetPos, xMousePos, yMousePos
         WinGetPos,,, cpdWidth, cpdHeight, ahk_exe cpd_launch.exe
         ControlGetPos, cListX, cListY, cListWidth, cListHeight, TkChild20, ahk_exe cpd_launch.exe
         winactivate, ahk_exe cpd_launch.exe
         WinWaitActive, ahk_exe cpd_launch.exe
         BlockInput, On
         WinMove, ahk_exe cpd_launch.exe,, (xMousePos - cListX - (cListWidth/2)), (yMousePos - cListY - (cListHeight/2))
         ;Sleep, 20
         BlockInput, Off
         Send, ^m
         WinMinimize, ahk_exe cpd_launch.exe
      }
      Else
      {
         Send, ^m
         ;WinMinimize, ahk_exe cpd_launch.exe
      }

      ;Removed the interaction loop below.  too much lag, is very interruptive.
      ;Loop
      ;{
         ;controlIsDown := GetKeyState("Control")
         ;shiftIsDown := GetKeyState("Shift")
         ;xIsDown := GetKeyState("x")
         ;if xIsDown
         ;{
            ;Send, ^u
         ;}
         ;Sleep, 50
      ;}
      ;Until !controlIsDown or !shiftIsDown

      ;WinMinimize, ahk_exe cpd_launch.exe
      Return
   }
   Return

^+x::
   SetTitleMatchMode, 1
   IfWinExist, ahk_exe cpd_launch.exe
   {
      IfWinNotActive, ahk_exe cpd_launch.exe
      {
         CoordMode, Mouse, Screen
         MouseGetPos, xMousePos, yMousePos
         WinGetPos,,, cpdWidth, cpdHeight, ahk_exe cpd_launch.exe
         ControlGetPos, cListX, cListY, cListWidth, cListHeight, TkChild20, ahk_exe cpd_launch.exe
         winactivate, ahk_exe cpd_launch.exe
         WinWaitActive, ahk_exe cpd_launch.exe
         BlockInput, On
         WinMove, ahk_exe cpd_launch.exe,, (xMousePos - cListX - (cListWidth/2)), (yMousePos - cListY - (cListHeight/2))
         Sleep, 50
         BlockInput, Off
      }
      Loop
      {
         controlIsDown := GetKeyState("Control")
         shiftIsDown := GetKeyState("Shift")
         xIsDown := GetKeyState("x")
         if xIsDown
         {
            Send, ^u
            Sleep, 50
         }
         else if controlIsDown
         {
            Sleep, 50
         }
      }
      Until !controlIsDown or !shiftIsDown
      IfWinActive, ahk_exe cpd_launch.exe
      {
         Send, ^k
         Sleep, 50
         WinMinimize, ahk_exe cpd_launch.exe
      }
      Return
   }
   Return

^+Space::
   IfWinNotActive, ahk_exe cpd_launch.exe
   {
      CoordMode, Mouse, Screen
      MouseGetPos, xMousePos, yMousePos
      WinGetPos,,, cpdWidth, cpdHeight, ahk_exe cpd_launch.exe
      ControlGetPos, cListX, cListY, cListWidth, cListHeight, TkChild20, ahk_exe cpd_launch.exe
      winactivate, ahk_exe cpd_launch.exe
      WinWaitActive, ahk_exe cpd_launch.exe
      BlockInput, On
      WinMove, ahk_exe cpd_launch.exe,, (xMousePos - cListX - (cListWidth/2)), (yMousePos - cListY - (cListHeight/2))
      Sleep, 50
      BlockInput, Off
      Return
   }
   else
   {
      Sleep, 50
      WinMinimize, ahk_exe cpd_launch.exe
      Return
   }
   Return

^+WheelDown::
   SetTitleMatchMode, 1
   IfWinNotActive, ahk_exe cpd_launch.exe
   {
      CoordMode, Mouse, Screen
      MouseGetPos, xMousePos, yMousePos
      WinGetPos,,, cpdWidth, cpdHeight, ahk_exe cpd_launch.exe
      ControlGetPos, cListX, cListY, cListWidth, cListHeight, TkChild20, ahk_exe cpd_launch.exe
      winactivate, ahk_exe cpd_launch.exe
      WinWaitActive, ahk_exe cpd_launch.exe
      BlockInput, On
      WinMove, ahk_exe cpd_launch.exe,, (xMousePos - cListX - (cListWidth/2)), (yMousePos - cListY - (cListHeight/2))
      BlockInput, Off
      ;Sleep, 100
      Return
   }
   Else
   {
      ; Wheel up/down switched between touchpad scroll and mousewheel scroll
      ;Send, ^{WheelDown}
      Send, ^{WheelUp}
      ;Sleep, 50
      Return
   }

^+WheelUp::
   SetTitleMatchMode, 1
   IfWinNotActive, ahk_exe cpd_launch.exe
   {
      CoordMode, Mouse, Screen
      MouseGetPos, xMousePos, yMousePos
      WinGetPos,,, cpdWidth, cpdHeight, ahk_exe cpd_launch.exe
      ControlGetPos, cListX, cListY, cListWidth, cListHeight, TkChild20, ahk_exe cpd_launch.exe
      winactivate, ahk_exe cpd_launch.exe
      WinWaitActive, ahk_exe cpd_launch.exe
      BlockInput, On
      WinMove, ahk_exe cpd_launch.exe,, (xMousePos - cListX - (cListWidth/2)), (yMousePos - cListY - (cListHeight/2))
      BlockInput, Off
      ;Sleep, 100
      Return
   }
   Else
   {
      ; Wheel up/down switched between touchpad scroll and mousewheel scroll
      ;Send, ^{WheelUp}
      Send, ^{WheelDown}
      ;Sleep, 50
      Return
   }

^+v::
   SetTitleMatchMode, 1
   IfWinActive, ahk_exe cpd_launch.exe
   {
      Send, ^k
      Sleep, 100
      WinMinimize, ahk_exe cpd_launch.exe
      Return
   }
   Return

; Some key replacements for my Dell UB for home/end
PgUp::Home
PgDn::End