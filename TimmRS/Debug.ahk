#SingleInstance force
GetInfo() {
	BreakLoop := 0
	InputBox, MaxMin, MaxMin, Max/Min?
	InputBox, ToolTipAnswer, ToolTip, ToolTip?
	if(ToolTipAnswer = "y") {
		InputBox, MouseA, Mouse?, Mouse?
	}
	InputBox, Beep, Beep?, Beep?
	InputBox, MaxTime, Max Time?, Max Time?
	InputBox, Notifications, Notifications?, Notifications?
	InputBox, Night, Night?, Night?
	Array := Object()
	Array.MaxMin := MaxMin
	Array.ToolTipA := ToolTipAnswer
	Array.MouseA := MouseA
	;Run, cmd /k echo %Mouse%
	Array.Beep := Beep
	Array.MaxTime := MaxTime
	Array.Notifications := Notifications
	Array.Night := Night
	Return Array
}

ShowGUI() {
	Gui, add
}

GameLoop(Array) {
	MaxMin := Array.MaxMin
	ToolTipA := Array.ToolTipA
	MouseA = Array.MouseA
	Beep := Array.Beep
	MaxTime := Array.MaxTime
	Notifications := Array.Notifications
	Night := Array.Night
	if(MaxTime is not integer) {
		MaxTime := 999999
	}
	Loop % MaxTime {
		if(BreakLoop = 1) {
			break
		}
		;Get Window Data
		WinActivate, RuneScape
		WinGetPos, a, b, w, h

		;Initiate Random Values
		Random, randomX, 0, 1366
		Random, randomY, 0, 768
		Random, randomTime, 250, 290
		Random, randomTime2, 523, 1523
		Random, randomTime3, 523, 1523

		;Run
		Sleep, randomTime2
		mousemove, randomX, randomY
		Sleep, randomTime3
		if(MaxMin = "y") {
			WinMinimize, RuneScape
		}
		;Initiate Time values
		StartTime := A_TickCount
		EndTime := A_TickCount + (randomTime*1000)
		i = 1
		;Wait loop
		Loop
		{
			;CoordMode, ToolTip
			if(BreakLoop = 1) {
				break
			}
			CurrentTime := A_TickCount
			MouseGetPos, px, py

			tooltiptext := Floor((EndTime - CurrentTime)/1000)
			if(MaxTime < 999999) {
				displaytime := MaxTime - i
				tooltiptext := Floor((EndTime - CurrentTime)/1000) . " - " . displaytime
			}
			tooltipx := 0
			tooltipy := 0
			if(MouseA = "y") {
				tooltipx := px+10
				tooltipy := py+10
			}

			/*if (Array[ToolTipAnswer] = y) and Array[ToolTipAnswer2] = y) {
					ToolTip, %tooltiptext%
			}
			else if (Array[ToolTipAnswer] = y and Array[ToolTipAnswer2] != y) {
					ToolTip, %tooltiptext%, 1, 1
			}
			*/
			if(ToolTipA = "y")
			{
					ToolTip, %tooltiptext%, tooltipx, tooltipy, 1
			}
			if(Night = "y") {
				SendMessage,0x112,0xF170,2,,Program Manager
			}

			if(Beep = "y") {
				/*
				if(tooltiptext = 200) {
					SoundBeep
					SendNotification("200 seconds until reset.", "200 seconds until reset.", Notifications)
				}
				if(tooltiptext = 100) {
					SoundBeep, 523, 10
					SendNotification("100 seconds until reset.", "100 seconds until reset.", Notifications)
				}
				*/	
				if(tooltiptext = 150) {
					SoundBeep, 523, 500
					SendNotification("150 seconds until reset.", "150 seconds until reset.", Notifications)	
				}
				if(tooltiptext = 0) {
					SoundBeep
					SendNotification("Time has elapsed. Resetting afk...", "Time has elapsed. Resetting afk...", Notifications)
					break
				}
			}
			if(tooltiptext <= 0) {
					break
			}
		}
		i++
	}
	ExitApp
	Return
}

SendNotification(Title, Message, Notifications) {
	if (Notifications = "y") {
		PB_Token   := "o.vcV5s5tkYm6k6jEICB5ygNFkPTBoD3xi"
		PB_Title   := Title
		PB_Message := Message

	;MsgBox % PB_PushNote(PB_Token, PB_Title, PB_Message)
		WinHTTP := ComObjCreate("WinHTTP.WinHttpRequest.5.1")
		WinHTTP.SetProxy(0)
		WinHTTP.Open("POST", "https://api.pushbullet.com/v2/pushes", 0)
		WinHTTP.SetCredentials(PB_Token, "", 0)
		WinHTTP.SetRequestHeader("Content-Type", "application/json")
		PB_Body := "{""type"": ""note"", ""title"": """ PB_Title """, ""body"": """ PB_Message """}"
		WinHTTP.Send(PB_Body)
		Result := WinHTTP.ResponseText
		Status := WinHTTP.Status
		return Status
	}
	Return
}


Main() {
	Loop {
		Array := GetInfo()
		GameLoop(Array)
	}
}

Main()

Esc::
BreakLoop := 1
Return



/*GetInput() {
BreakLoop = 0
InputBox, MaxMin, MaxMin, Max/Min?
InputBox, ToolTipAnswer, ToolTip, ToolTip?
if (ToolTipAnswer == "y") {
	InputBox, ToolTipAnswer2, Mouse?, Mouse?
}
InputBox, Beep, Beep?, Beep?
Array := Object()
Array.Insert(MaxMin)
Array.Insert(ToolTipAnswer)
Array.Insert(ToolTipAnswer2)
Array.Insert(Beep)
Main_thing(Array)
}

GetInput()

Main_thing(Array) {
Loop {
IfWinExist, RuneScape
	if (BreakLoop == 1) {
		break
	}
	MouseGetPos mouseX, mouseY
	WinActivate, RuneScape
	WinGetPos, a, b, w, h
	Random, randomX, 0, w
	Random, randomY, 0, h
	Random, randomTime, 250, 290
	Random, randomTime2, 523, 1523
	Random, randomTime3, 523, 1523
	Sleep, randomTime2
	mousemove, randomX, randomY
	Sleep, randomTime3
	If (Array[0] == "y") {
		WinMinimize, RuneScape
	}
	Sleep, randomTime
	StartTime := A_TickCount
	EndTime := A_TickCount + (randomTime*1000)
	Loop {
		if (BreakLoop == 1) {
			break
		}
		CurrentTime := A_TickCount
		MouseGetPos, px, py
		tooltiptext := Floor((EndTime - CurrentTime)/1000)
		if (Array[1] == "y" and Array[2] == "y") {
				ToolTip, %tooltiptext%, px+20, py+20, 1
		}
		else if (Array[1] == "y" and Array[2] != "y") {
				ToolTip, %tooltiptext%, 0, 0, 1
		}
		if (Array[3] == "y") {
			if (tooltiptext == 100) {
				SoundBeep, 523, 500
			}			
			if (tooltiptext == 0) {
				SoundBeep, 523, 150
				break
			}
		}
		else {
			if (tooltiptext == 0) {
				break
			}
		}
	}
}
Return
}

Escape::
BreakLoop = 1
Sleep, 200
GetInput()
Return
*/