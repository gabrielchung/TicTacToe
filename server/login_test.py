import login

l = login.Login_Sys(5)
t1 = l.register()
t2 = l.register()
t3 = '123456'
assert l.login(t1) == 0
assert l.login(t2) == 1
assert l.login(t3) == -1