"""Best-effort native desktop notification. Titles/bodies contain attacker-controlled text, so they are passed as ARGUMENTS/ENV, never interpolated into code."""
import os, subprocess, sys

_PS = r"""
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
$x = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
$t = $x.GetElementsByTagName('text')
$t.Item(0).AppendChild($x.CreateTextNode($env:AR_T)) | Out-Null
$t.Item(1).AppendChild($x.CreateTextNode($env:AR_B)) | Out-Null
$n = [Windows.UI.Notifications.ToastNotification]::new($x)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe').Show($n)
"""


def notify(title: str, body: str) -> bool:
    title, body = " ".join(title.split())[:80], " ".join(body.split())[:220]
    print(f"[ALERT] {title} — {body}", flush=True)
    try:
        if sys.platform.startswith("win"):
            subprocess.Popen(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", _PS], env={**os.environ, "AR_T": title, "AR_B": body}, creationflags=0x08000000)
        elif sys.platform == "darwin":
            subprocess.Popen(["osascript", "-e", "on run argv", "-e", "display notification (item 2 of argv) with title (item 1 of argv)", "-e", "end run", title, body])
        else:
            subprocess.Popen(["notify-send", "--", title, body])
        return True
    except Exception:
        return False
