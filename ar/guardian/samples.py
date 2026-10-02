"""Demo messages (fictional: example.invalid, no real brands). Used by the Simulate button and scripts/simulate_inbox.py."""
SAMPLES = {
 "sms_pin": dict(label="SMS — PIN scam", source="sms", sender="Unknown number", subject="", text="URGENT: Your payment has failed. Send your PIN within 30 minutes so that our agent can reverse the transaction."),
 "phish_mail": dict(label="Email — fake bank (link mismatch)", source="email", sender="security@bank-alerts.example.invalid", subject="Action required: your online banking profile is locked",
    text="Dear customer, your online banking profile has been locked. Re-activate it now to avoid permanent closure.",
    links=[("www.mybank.example/reactivate", "http://secure-login.example.invalid/x")], reply_to="help@helpdesk.example", auth="dmarc=fail spf=fail"),
 "exe_mail": dict(label="Email — fake invoice with hidden .exe", source="email", sender="accounts@supplier.example.invalid", subject="Invoice", text="Hi, please find the attached invoice for this month. Regards.", atts=["invoice.pdf.exe"]),
 "voice": dict(label="Voice note — manager impersonation", source="whatsapp-export", sender="Unknown number", subject="", text="This voice message from your manager asks you to urgently transfer money to a new account."),
 "benign": dict(label="Email — normal reminder (no alert)", source="email", sender="office@company.example.invalid", subject="Team meeting", text="Reminder: the team meeting is at 14:00 tomorrow in the boardroom. Please bring your reports."),
}
