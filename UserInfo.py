class SecretSetting:
    def __init__(self, username, password):
        self.username = username
        self.password = password


secret = SecretSetting("username", "passwd")
