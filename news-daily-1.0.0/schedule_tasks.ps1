
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\Users\MyPC\.openclaw\workspace\skills\news-daily-1.0.0\news_daily.py push"
$trigger1 = New-ScheduledTaskTrigger -Daily -At "09:30"
$trigger2 = New-ScheduledTaskTrigger -Daily -At "20:00"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "DailyAINews_Morning" -Action $action -Trigger $trigger1 -Settings $settings -Description "每日AI新闻推送 - 早上09:30" -Force
Register-ScheduledTask -TaskName "DailyAINews_Evening" -Action $action -Trigger $trigger2 -Settings $settings -Description "每日AI新闻推送 - 晚上20:00" -Force

Write-Host "定时任务已创建!"
Write-Host "早上 09:30 - DailyAINews_Morning"
Write-Host "晚上 20:00 - DailyAINews_Evening"
