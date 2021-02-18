#!/usr/bin/python3
'''
class that defines all common attributes/methods for other classes
'''
import uuid
import models
from datetime import datetime

date_format = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    '''
    Base model class
    '''

    def __init__(self, *args, **kwargs):
        '''
        Args:
            - id: Instance ID
            - created_at: Date of creation of file
            - updated_at. Date of update of file

        Base class constructor
        '''
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, date_format)
                else:
                    self.__dict__[key] = value
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def save(self):
        '''
        Updates the public instance
        attribute updated_at with the current datetime
        '''
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        '''
        Method to generate a dictionary representation of an instance
        '''
        dct = dict(self.__dict__)
        dct["__class__"] = self.__class__.__name__
        dct["created_at"] = self.created_at.isoformat()
        dct["updated_at"] = self.updated_at.isoformat()
        return dct

    def __str__(self):
        '''
        Prints: [<class name>] (<self.id>) <self.__dict__>
        '''
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)
