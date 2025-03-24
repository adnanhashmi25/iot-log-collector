import re
import pexpect
child = pexpect.spawn("ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no lteuser@2405:200:10a:2000:3:2:103:5e")
child.expect("password:")
child.sendline("samsunglte")
child.expect(re.escape("~$ "))
print child.before
child.sendline("ls /pkg/6.0.0/ENB/r-03/bin/")
child.expect(re.escape("~$ "))
print child.before
child.sendline("exit")
