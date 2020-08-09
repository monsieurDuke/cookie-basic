import json

with open('gmail_account.json','r') as f:
	gm_acc = json.load(f)

for gmail in gm_acc:
	gm_addr = gmail['email_addr_sender']
	gm_pass = gmail['email_pass_sender']

print(gm_addr+' : '+gm_pass)
#"email_addr_sender": "icatmuhammad3@gmail.com",
#"email_pass_sender": "wuooppacgpugsups"
