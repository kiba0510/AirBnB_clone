<p align="center">
    <img src="https://holbertonintranet.s3.amazonaws.com/uploads/medias/2018/6/65f4a1dd9c51265f49d0.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUWMNL5ANN%2F20210215%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210215T142924Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=225229c3fb7be9094c37649c30a556daac4d587f17b235d8256dec3d28963f7e" width="500">
        <h1 align="center">Holberton Airbnb Console</h1>
            <br>

<h2 align="center">Steps<h2>

<h3>The Console</h3>

* Create data model.
* Manage (Create, update, destroy, etc) objects via ```CLI```.
* Serialize and store objects to ```JSON``` file. 

This idea behind this first step is to create a ```CLI``` that lets you manage and store data. This storage engine will give us an abstraction between “My object” and “How they are stored and persisted”. This means: from your ```CLI``` ( the Command Line Interpreter ) and from the ```front-end``` and ```RestAPI``` you will build later. This abstraction will also allow you to change the type of storage easily without updating all of your codebase.

<hr>
<br>

<p align="center">
    <img src="https://holbertonintranet.s3.amazonaws.com/uploads/medias/2018/6/815046647d23428a14ca.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUWMNL5ANN%2F20210215%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210215T161958Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=92107d2c22a65e1cbf6efd62cc63c058386b993234452a5223a4ee77c9338a2c">

<h2>Files and Directories</h2>

* ```Models``` directory will contain all classes used for the entire project. A class, called “model” in a OOP project is the representation of an object/instance.
* ```Tests``` directory will contain all unit tests.
* ```console.py``` file is the entry point of our command interpreter.
* ```models/base_model.py``` file is the base class of all our models. It contains common elements:
    * attributes: ```id```, ```created_at``` and ```updated_at```
    * methods: ```save()``` and ```to_json()```
* ```models/engine``` directory will contain all storage classes (using the same prototype). For the moment you will have only one: ```file_storage.py```.

<h2>Storage</h2>

Persistency is really important for a web application. It means: every time your program is executed, it starts with all objects previously created from another execution. Without persistency, all the work done in a previous execution won’t be saved and will be gone.

In this project, you will manipulate 2 types of storage: file and database. For the moment, you will focus on file.

Why separate “storage management” from “model”? It’s to make your models modular and independent. With this architecture, you can easily replace your storage system without re-coding everything everywhere.

You will always use class attributes for any object. Why not instance attributes? For 3 reasons:

* Provide easy class description: everybody will be able to see quickly what a model should contain (which attributes, etc…)
* Provide default value of any attribute
* In the future, provide the same model behavior for file storage or database storage.

<h2>How can I store my instances?</h2>

That’s a good question. So let’s take a look at this code:
```
class Student():
    def __init__(self, name):
        self.name = name

students = []
s = Student("John")
students.append(s)
```

Here, I’m creating a student and store it in a list. But after this program execution, my Student instance doesn’t exist anymore.

```
class Student():
    def __init__(self, name):
        self.name = name

students = reload() # recreate the list of Student objects from a file
s = Student("John")
students.append(s)
save(students) # save all Student objects to a file
```
So, how does this work?

First, let’s look at ```save(students)```:

* Can I write each ```Student``` object to a file => NO, it will be the memory representation of the object. For another program execution, this memory representation can’t be reloaded.
* Can I write each ```Student.name``` to a file => YES, but imagine you have other attributes to describe ```Student```? It would start to be become too complex.

The best solution is to convert this list of ```Student``` objects to a JSON representation.

Why JSON? Because it’s a standard representation of object. It allows us to share this data with other developers, be human readable, but mainly to be understood by another language/program.

Example:

* My Python program creates ```Student``` objects and saves them to a JSON file
* Another Javascript program can read this JSON file and manipulate its own ```Student``` class/representation.
  
And the ```reload()```? now you know the file is a JSON file representing all ```Student``` objects. So ```reload()``` has to read the file, parse the JSON string, and re-create ```Student``` objects based on this data-structure.

<h2>File Storage == JSON Serialization</h2>

For this first step, you have to write in a file all your objects/instances created/updated in your command interpreter and restore them when you start it. You can’t store and restore a Python instance of a class as “Bytes”, the only way is to convert it to a serializable data structure:

* convert an instance to Python built in serializable data structure (list, dict, number and string) - for us it will be the method ```my_instance.to_json()``` to retrieve a dictionary.
* convert this data structure to a string (JSON format, but it can be YAML, XML, CSV…) - for us it will be a ```my_string = JSON.dumps(my_dict)```
write this string to a file on disk.

Ok, and now for deseralization.

The same but in the other way:

* read a string from a file on disk.
* convert this string to a data structure. This string is a JSON representation, so it’s easy to convert - for us it will be a my_dict = JSON.loads(my_string).
* convert this data structure to instance - for us it will be a my_instance = MyObject(my_dict).

<h2>How to Execute</h2>

Your shell should work like this in interactive mode:

```
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb) 
(hbnb) 
(hbnb) quit
$
```

But also in non-interactive mode:

```
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
```

<h2>How to use Commands</h2>

This an example of how to use the commands:
* ```create```
* ```update```
* ```all```
* ```show```
* ```destroy```

```
julian@julian-HP-Pavilion-x360-Convertible-14-ba0xx:~/Projects/Holberton Projects/AirBnB_clone$ ./console.py
(hbnb) all MyModel
** class doesn't exist **
(hbnb) show BaseModel
** instance id missing **
(hbnb) show BaseModel Holberton
** no instance found **
(hbnb) create BaseModel
49faff9a-6318-451f-87b6-910505c55907
(hbnb) all BaseModel
["[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) {'created_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903293), 'id': '49faff9a-6318-451f-87b6-910505c55907', 'updated_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903300)}"]
(hbnb) show BaseModel 49faff9a-6318-451f-87b6-910505c55907
[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) {'created_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903293), 'id': '49faff9a-6318-451f-87b6-910505c55907', 'updated_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903300)}
(hbnb) destroy
** class name missing **
(hbnb) update BaseModel 49faff9a-6318-451f-87b6-910505c55907 first_name "Betty"
(hbnb) show BaseModel 49faff9a-6318-451f-87b6-910505c55907
[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) {'first_name': 'Betty', 'id': '49faff9a-6318-451f-87b6-910505c55907', 'created_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903293), 'updated_at': datetime.datetime(2017, 10, 2, 3, 11, 3, 49401)}
(hbnb) create BaseModel
2dd6ef5c-467c-4f82-9521-a772ea7d84e9
(hbnb) all BaseModel
["[BaseModel] (2dd6ef5c-467c-4f82-9521-a772ea7d84e9) {'id': '2dd6ef5c-467c-4f82-9521-a772ea7d84e9', 'created_at': datetime.datetime(2017, 10, 2, 3, 11, 23, 639717), 'updated_at': datetime.datetime(2017, 10, 2, 3, 11, 23, 639724)}", "[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) {'first_name': 'Betty', 'id': '49faff9a-6318-451f-87b6-910505c55907', 'created_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903293), 'updated_at': datetime.datetime(2017, 10, 2, 3, 11, 3, 49401)}"]
(hbnb) destroy BaseModel 49faff9a-6318-451f-87b6-910505c55907
(hbnb) show BaseModel 49faff9a-6318-451f-87b6-910505c55907
** no instance found **
(hbnb)
```
