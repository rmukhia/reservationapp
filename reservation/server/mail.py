import smtplib

s = smtplib.SMTP()
s.connect('smtp.office365.com', 587)
#s.connect('ixiacom.com', 587)
s.ehlo()
s.starttls()
s.ehlo()
s.login('rsingh@ixiacom.com','@Streetboys1')
msg = "it is working"
recipient_list = ['rmukhia@ixiacom.com']
s.sendmail('rsingh@ixiacom.com',recipient_list,msg)
s.quit()
