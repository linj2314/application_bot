class CustomErrors(Exception):
    pass

class ExpiredApplicationError(CustomErrors):
    def __init__(self, message="Application has expired"):
        self.message = message

class RequiredWorkExperienceError(CustomErrors):
    def __init__(self, message="Application requires previous work experience"):
        self.message = message