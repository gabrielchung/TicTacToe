import secrets as sec

class Login_Sys:
  def __gen_token(self, token_bytes=128):
    return sec.token_urlsafe(token_bytes)

  def __init__(self, num_of_users):
    users_token = []
    for x in range(num_of_users):
      users_token.append(self.__gen_token())
    self.users_token = users_token
    self.users_register = users_token.copy()

  def login(self, token):
    user_index = 0
    for t in self.users_token:
      if t == token:
        return user_index
      else:
        user_index += 1
    return -1
  
  def register(self):
    if len(self.users_register) == 0:
      return False
    token = self.users_register[0]
    self.users_register.remove(token)
    return token