#!/usr/bin/python3
"""
program that contains the entry point of the command interpreter
"""

import cmd
import models
import re
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ This class to setup the command interpreter """
    __DCT_CLS = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }
    prompt = "(hbnb) "

    def do_quit(self, line):
        '''Exit the CMD program'''
        return True

    def do_EOF(self, line):
        '''Exit the CMD program'''
        return True

    def emptyline(self):
        '''Do nothing'''
        pass

    def do_create(self, line):
        '''Creates a new instance of BaseModel'''
        arg_line = line.split()

        if line == "":
            print("** class name missing **")
            return False
        elif arg_line[0] not in self.__DCT_CLS:
            print("** class doesn't exist **")
        else:
            new_instance = self.__DCT_CLS[arg_line[0]]()
            print(new_instance.id)
            new_instance.save()

    def do_show(self, line):
        '''Prints the string representation
        of an instance based on the class name and id'''
        if (type(line) == str):
            arg_line = line.split()
            len_args = len(arg_line)

            if (self.check_if_created(arg_line, len_args) != 1):

                get_inst = arg_line[0] + "." + arg_line[1]
                dict_classes = models.storage.all()

                if get_inst in dict_classes.keys():
                    print(dict_classes[get_inst])
                else:
                    print("** no instance found **")
        else:
            srch_id = line[0] + "." + line[1]
            dict_classes = models.storage.all()
            if srch_id in dict_classes.keys():
                print(dict_classes[srch_id])
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        '''Deletes an instance based on the class
        name and id (save the change into the JSON file).'''
        arg_line = line.split()
        len_args = len(arg_line)
        if (self.check_if_created(arg_line, len_args) != 1):

            get_inst = arg_line[0] + "." + arg_line[1]
            dict_classes = models.storage.all()

            if get_inst in dict_classes.keys():
                del dict_classes[get_inst]
                models.storage.save()
            else:
                print("** no instance found **")

    def do_all(self, line):
        '''Prints all string representation of all instances
        based or not on the class name. Ex: $ all BaseModel or $ all.'''
        arg_line = line.split()
        if line == "" or arg_line[0] in self.__DCT_CLS:
            dir_classes = models.storage.all()
            list_classes = []
            for key, value in dir_classes.items():
                if line in key:
                    list_classes.append(value.__str__())
            print(list_classes)
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        '''Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234
        email "aibnb@holbertonschool.com".'''
        arg_line = line.split()
        len_args = len(arg_line)

        if (self.check_if_created(arg_line, len_args) == 1):
            pass
        elif (len_args == 2):
            print("** attribute name missing **")
        elif (len_args == 3):
            print("** value missing **")
        else:
            get_inst = arg_line[0] + "." + arg_line[1]
            dict_classes = models.storage.all()
            if get_inst in dict_classes.keys():
                if arg_line[3]:
                    arg_line[3] = arg_line[3].replace('"', "")
                try:
                    arg_line[3] = int(arg_line[3])
                except ValueError:
                    try:
                        arg_line[3] = float(arg_line[3])
                    except ValueError:
                        arg_line[3] = arg_line[3]
                dict_classes[get_inst].__dict__[arg_line[2]] = arg_line[3]
                dict_classes[get_inst].save()
            else:
                print("** no instance found **")

    def default(self, line):
        '''Get's all method names that aren't defined'''
        args_line = line.split('.')
        if len(args_line) > 1:
            if args_line[1] == "all()":
                self.do_all(args_line[0])
            if args_line[1] == "count()":
                self.do_count(args_line[0])

            my_count = args_line[1].split('"')
            res = re.findall(r'\(.*?\)', args_line[1])
            my_count[0] = my_count[0] + line[-1]
            if my_count[0] == "show()":
                myNewList = [args_line[0], my_count[1]]
                self.do_show(myNewList)
        else:
            cmd.Cmd.default(self, line)

    def check_if_created(self, arg_line, len_args):
        '''Verifies if the class exists'''
        if len_args == 0:
            print("** class name missing **")
            return 1
        elif arg_line[0] not in self.__DCT_CLS:
            print("** class doesn't exist **")
            return 1
        elif (len_args == 1):
            print("** instance id missing **")
            return 1

    def do_count(self, line):
        '''Counts and retrive the number of existing instances'''
        arg_line = line.split()
        if line == "" or arg_line[0] in self.__DCT_CLS:
            dir_classes = models.storage.all()
            list_classes = []
            count = 0
            for key, value in dir_classes.items():
                if line in key:
                    list_classes.append(value.__str__())
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
