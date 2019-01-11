import uuid


class Generics:
    """
    Generic class helper for all the Apps in the project.
    """

    @staticmethod
    def generate_cookie():
        """
        :return: Unique identifier using uuid.
        """
        return uuid.uuid4()
