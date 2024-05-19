# response_constants.py

class ResponseConstants:
    @staticmethod
    def ok(data=None):
        return {"status": "OK", "message": "Operation completed successfully", "data": data}

    @staticmethod
    def internal_error():
        return {"status": "ERROR", "message": "Internal server error"}

    @staticmethod
    def not_found():
        return {"status": "ERROR", "message": "Resource not found"}

    @staticmethod
    def bad_request():
        return {"status": "ERROR", "message": "Bad request"}

    @staticmethod
    def unauthorized():
        return {"status": "ERROR", "message": "Unauthorized access"}
