class response_message:
  def __init__(self, status: int, message: str, data:dict=None):
    self.status = status
    self.message = message
    self.data = data

  def get_dict(self):
    return self.__dict__