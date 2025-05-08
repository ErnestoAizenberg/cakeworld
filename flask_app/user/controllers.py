



class UserController:  # UnMock NEEDED!
    """Not implemented, shale be solved with the question about controllers reusing"""

    def __init__(self, user_service):
        self.user_service = user_service

    def list_users(self):
        return self.user_service.get_all_users()
