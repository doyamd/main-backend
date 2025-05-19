class BaseResponse():
    def __init__(self, status_code=400, data=None, message=None, success=False, Error=[]):
        self.status_code = status_code
        self.data = data
        self.message = message
        self.success = success
        self.error = Error
        
    def to_dict(self):
        return {
            'success': self.success,
            'message': self.message,
            'data': self.data,
            'error': self.error,
            'statuscode': self.status_code,
        }
    
    def update(self, status_code=None, success=None, message=None, data=None):
        if status_code is not None:
            self.status_code = status_code
        if success is not None:
            self.success = success
        if message is not None:
            self.message = message
        if data is not None:
            self.data = data