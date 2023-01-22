@echo off
echo %date% %time% Generate token for Energy API
CD "D:\openHABScripts\volvo"
CD 
C:\Windows\System32\taskkill.exe /f /im:chromedriver.exe 
D:\Python37\python.exe D:\openHABScripts\volvo\volvo.py -a energy 
echo %date% %time% Done!
