import json
import random
from abc import ABC, abstractmethod
from typing import List, Optional


class Lecturer:
    """Giảng viên

     Attributes:
        - minimum (int): Số ca học tối thiểu trong 1 tuần
        - maximum (int): Số ca học tối đa trong 1 tuần
        - name (str): Tên giảng viên
    """
    minimum = 2
    maximum = 20

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name

    def __str__(self):
        return "<Lecturer: {} {}>".format(self.id, self.name)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def read_json(cls, filepath: str) -> List["Lecturer"]:
        lecturers = []
        _lecturers = None
        with open(filepath) as file_json:
            _lecturers = json.load(file_json)
        for _lecturer in _lecturers:
            lecturer = Lecturer(
                id=_lecturer["id"],
                name=_lecturer["name"],
            )
            lecturers.append(lecturer)
        return lecturers

    @classmethod
    def load(cls) -> List["Lecturer"]:
        return cls.read_json("./data/lecturers.json")


class Room:
    """Phòng học

     Attributes:
        - num_shifts: Số ca học trong 1 ngày
        - name: Tên phòng học
    """
    num_shifts = 4

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def __str__(self) -> str:
        return "<Room: {}>".format(self.name)

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def read_json(cls, filepath: str) -> List["Room"]:
        """Đọc dữ liệu từ file json

         Args:
            filepath (str): file path

         Returns:
            List[Room]: danh sách lớp học
        """
        rooms = []
        _rooms = None
        with open(filepath) as file_json:
            _rooms = json.load(file_json)
        for _room in _rooms:
            room = Room(
                id=_room["id"],
                name=_room["name"],
            )
            rooms.append(room)
        return rooms

    @classmethod
    def write_json(cls, rooms: List["Room"], filepath: str) -> None:
        """Lưu dữ liệu vào file json

         Args:
            rooms (List["Room"]): danh sách phòng học
            filepath (str): file path
        """
        _rooms = []
        for room in rooms:
            _rooms.append({
                "id": room.id,
                "name": room.name
            })
        with open(filepath, "w") as jsonfile:
            jsonfile.write(json.dumps(_rooms, ensure_ascii=False))

    @classmethod
    def load(cls) -> List["Room"]:
        """Đọc dữ liệu từ file json "./data/rooms.json"

         Returns:
            List[Room]: danh sách lớp học
        """
        return cls.read_json("./data/rooms.json")

    @classmethod
    def save(cls, rooms: List["Room"]) -> None:
        """Lưu dữ liệu vào file json "./data/rooms.json"

         Returns:
            List[Room]: danh sách lớp học
        """
        cls.write_json(rooms, "./data/rooms.json")


class Shift:
    """Ca học

     Attributes:
        - id (int): Mã ca học
        - time (str): thời gian bắt đầu và kết thúc ca
    """

    def __init__(self, id: int, time: str) -> None:
        self.id = id
        self.time = time

    def __str__(self) -> str:
        return "<Shift: {} {}>".format(self.id, self.time)

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def read_json(cls, filepath: str) -> List["Shift"]:
        """Đọc dữ liệu từ file json

         Args:
            - filepath (str): file path.

         Returns:
            - List[Shift]: danh sách ca học
        """
        shifts = []
        _shifts = None
        with open(filepath) as file_json:
            _shifts = json.load(file_json)
        for _shift in _shifts:
            shift = Shift(
                id=_shift["id"],
                time=_shift["time"],
            )
            shifts.append(shift)
        return shifts

    @classmethod
    def load(cls) -> List["Shift"]:
        """Đọc dữ liệu từ file json "./data/shifts.json"

        Returns:
            List[Shift]: danh sách ca học
        """
        return cls.read_json("./data/shifts.json")


class Course:
    """Môn học

     Attributes:
        - id (str): Mã môn học.
        - name (str): Tên môn học.
        - lecturers (List[Lecturer]): Danh sách giảng viên dạy môn học.
        - num_classes (int): Số lớp môn học mở.
        - is_practice (bool): Là lớp thực hành.
    """

    def __init__(self, id: str, name: str, lecturers: List[Lecturer], num_classes: int, is_practice: bool):
        self.id = id
        self.name = name
        self.lecturers = lecturers
        self.num_classes = num_classes
        self.is_practice = is_practice

    def __str__(self):
        return "<Course: id: {} name: {} {}>".format(self.id, self.name, self.lecturers)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def read_json(cls, filepath: str) -> List["Course"]:
        courses = []
        _courses = None
        with open(filepath) as file_json:
            _courses = json.load(file_json)
        for _course in _courses:
            course = Course(
                id=_course["id"],
                name=_course["name"],
                lecturers=[
                    Lecturer(
                        id=lecturer["id"],
                        name=lecturer["name"],
                    ) for lecturer in _course["lecturers"]
                ],
                num_classes=_course["num_classes"],
                is_practice=_course["is_practice"],
            )
            courses.append(course)
        return courses

    @classmethod
    def load(cls) -> List["Course"]:
        return cls.read_json("./data/courses.json")


class Gene(ABC):
    pass


class Class(Gene):
    """Lớp học

     Attributes:
        - id (str): Mã môn học.
        - course (Course): Môn học của lớp.
        - lecturer (Lecturer): Giảng viên của lớp.
        - room (Room): Phòng học của lớp.
        - shift (Shift): Ca học của lớp.
    """
    DAYS = {
        0: "Thứ 2",
        1: "Thứ 3",
        2: "Thứ 4",
        3: "Thứ 5",
        4: "Thứ 6",
        5: "Thứ 7",
    }

    def __init__(self, id: int, course: Course, lecturer: Optional[Lecturer] = None, room: Optional[Room] = None, day: Optional[int] = None, shift: Optional[Shift] = None):
        self.id = id
        self.course = course
        self.lecturer = lecturer
        self.room = room
        self.day = day
        self.shift = shift
        self.conflict = False

    def __str__(self):
        return "<Class: {}, {}, {}, {}, {} {}>".format(self.id, self.course, self.lecturer, self.room, self.day, self.shift)

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return Class(
            self.id,
            self.course,
            self.lecturer,
            self.room,
            self.day,
            self.shift,
        )


class Chromosome:
    genes = []

    def __init__(self) -> None:
        pass

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def get_fitness(self):
        pass

    @abstractmethod
    def calculate_fitness(self):
        pass


class Schedule(Chromosome):
    """Lịch học

     Attributes:
        - __shifts: Danh sách các ca học
        - __rooms: Danh sách các phòng học

        - classes: Danh sách các lớp học
        - __num_conflicts: Số lần bị trùng
        - __fitness: Độ thích nghi

    """
    __shifts = Shift.load()
    __rooms = Room.load()  # type: List[Room]
    __lecturers = Lecturer.load()

    def __init__(self) -> None:
        self.classes = []  # type: List[Class]
        self.genes = self.classes
        self.__num_conflicts = 0
        self.__fitness = -1

    def copy(self) -> "Schedule":
        schedule = Schedule()
        for clas in self.classes: schedule.classes.append(clas.copy())
        return schedule

    def initialize(self) -> "Schedule":
        _rooms_practice = [
            room for room in self.__rooms if room.name.startswith("A")]
        _rooms_npractice = [
            room for room in self.__rooms if not room.name.startswith("A")]

        _class_id = 0
        courses = Course.load()
        for i in range(len(courses)):
            for _ in range(courses[i].num_classes):
                new_class = Class(_class_id, courses[i])
                _class_id += 1
                new_class.shift = self.__shifts[random.randrange(
                    0, len(self.__shifts))]
                if courses[i].is_practice:
                    new_class.room = _rooms_practice[random.randrange(
                        0, len(_rooms_practice))]
                else:
                    new_class.room = _rooms_npractice[random.randrange(
                        0, len(_rooms_npractice))]
                new_class.day = random.randrange(0, len(Class.DAYS))
                new_class.lecturer = courses[i].lecturers[random.randrange(
                    0, len(courses[i].lecturers))]
                self.classes.append(new_class)
        return self

    def get_fitness(self) -> float:
        return self.__fitness

    def get_num_conflicts(self) -> int:
        return self.__num_conflicts

    def calculate_fitness(self) -> float:
        self.__num_conflicts = 0
        classes = self.classes
        for i in range(len(classes)-1):
            for j in range(i+1, len(classes)):
                if classes[i].day == classes[j].day \
                        and classes[i].shift == classes[j].shift:
                    if classes[i].room.id == classes[j].room.id:
                        self.__num_conflicts += 1
                        classes[i].conflict = True
                    elif classes[i].lecturer.id == classes[j].lecturer.id:
                        classes[i].conflict = True

        loss = 0

        num_class_per_lecturer = {}
        for i in range(len(classes)):
            if classes[i].lecturer.id not in num_class_per_lecturer:
                num_class_per_lecturer[classes[i].lecturer.id] = 0
            else:
                num_class_per_lecturer[classes[i].lecturer.id] += 1

        for lecturer in num_class_per_lecturer:
            if num_class_per_lecturer[lecturer] > Lecturer.maximum:
                loss += num_class_per_lecturer[lecturer] - Lecturer.maximum
            if num_class_per_lecturer[lecturer] < Lecturer.minimum:
                loss += Lecturer.minimum - num_class_per_lecturer[lecturer]
        self.__fitness = 1 / (self.__num_conflicts * 0.1 + loss * 0.01 + 1)
        return self.__fitness

    def save(self):
        data = {}
        courses = {}
        lecturers = {}
        rooms = {}
        _classes = []
        for clas in self.classes:
            _classes.append({
                "id": clas.id,
                "course": {
                    "id": clas.course.id,
                    "name": clas.course.name,
                    "num_classes": clas.course.num_classes,
                    "is_practice": clas.course.is_practice,
                },
                "room": {
                    "id": clas.room.id,
                    "name": clas.room.name,
                },
                "lecturer": {
                    "id": clas.lecturer.id,
                    "name": clas.lecturer.name,
                },
                "day": clas.day,
                "shift": {
                    "id": clas.shift.id,
                    "time": clas.shift.time,
                }
            })

        for clas in self.classes:
            if clas.course.name not in courses:
                courses[clas.course.name] = [{
                    "id": clas.id,
                    "course": {
                        "id": clas.course.id,
                        "name": clas.course.name,
                        "num_classes": clas.course.num_classes,
                        "is_practice": clas.course.is_practice,
                    },
                    "room": {
                        "id": clas.room.id,
                        "name": clas.room.name,
                    },
                    "lecturer": {
                        "id": clas.lecturer.id,
                        "name": clas.lecturer.name,
                    },
                    "day": clas.day,
                    "shift": {
                        "id": clas.shift.id,
                        "time": clas.shift.time,
                    }
                }]
            else:
                courses[clas.course.name].append({
                    "id": clas.id,
                    "course": {
                        "id": clas.course.id,
                        "name": clas.course.name,
                        "num_classes": clas.course.num_classes,
                        "is_practice": clas.course.is_practice,
                    },
                    "room": {
                        "id": clas.room.id,
                        "name": clas.room.name,
                    },
                    "lecturer": {
                        "id": clas.lecturer.id,
                        "name": clas.lecturer.name,
                    },
                    "day": clas.day,
                    "shift": {
                        "id": clas.shift.id,
                        "time": clas.shift.time,
                    }
                })

            if clas.lecturer.name not in lecturers:
                lecturers[clas.lecturer.name] = [{
                    "id": clas.id,
                    "course": {
                        "id": clas.course.id,
                        "name": clas.course.name,
                        "num_classes": clas.course.num_classes,
                        "is_practice": clas.course.is_practice,
                    },
                    "room": {
                        "id": clas.room.id,
                        "name": clas.room.name,
                    },
                    "lecturer": {
                        "id": clas.lecturer.id,
                        "name": clas.lecturer.name,
                    },
                    "day": clas.day,
                    "shift": {
                        "id": clas.shift.id,
                        "time": clas.shift.time,
                    }
                }]
            else:
                lecturers[clas.lecturer.name].append({
                    "id": clas.id,
                    "course": {
                        "id": clas.course.id,
                        "name": clas.course.name,
                        "num_classes": clas.course.num_classes,
                        "is_practice": clas.course.is_practice,
                    },
                    "room": {
                        "id": clas.room.id,
                        "name": clas.room.name,
                    },
                    "lecturer": {
                        "id": clas.lecturer.id,
                        "name": clas.lecturer.name,
                    },
                    "day": clas.day,
                    "shift": {
                        "id": clas.shift.id,
                        "time": clas.shift.time,
                    }
                })

            if clas.room.name not in rooms:
                rooms[clas.room.name] = [{
                    "id": clas.id,
                    "course": {
                        "id": clas.course.id,
                        "name": clas.course.name,
                        "num_classes": clas.course.num_classes,
                        "is_practice": clas.course.is_practice,
                    },
                    "room": {
                        "id": clas.room.id,
                        "name": clas.room.name,
                    },
                    "lecturer": {
                        "id": clas.lecturer.id,
                        "name": clas.lecturer.name,
                    },
                    "day": clas.day,
                    "shift": {
                        "id": clas.shift.id,
                        "time": clas.shift.time,
                    }
                }]
            else:
                rooms[clas.room.name].append({
                    "id": clas.id,
                    "course": {
                        "id": clas.course.id,
                        "name": clas.course.name,
                        "num_classes": clas.course.num_classes,
                        "is_practice": clas.course.is_practice,
                    },
                    "room": {
                        "id": clas.room.id,
                        "name": clas.room.name,
                    },
                    "lecturer": {
                        "id": clas.lecturer.id,
                        "name": clas.lecturer.name,
                    },
                    "day": clas.day,
                    "shift": {
                        "id": clas.shift.id,
                        "time": clas.shift.time,
                    }
                })
        data = {
            "group_by_courses": courses,
            "group_by_lecturers": lecturers,
            "group_by_rooms": rooms,
            "classes": _classes
        }
        with open("data/results.json", "w") as jsonfile:
            jsonfile.write(json.dumps(data, ensure_ascii=False))

    @classmethod
    def load(cls):
        _result = None
        with open("./data/results.json") as file_json:
            _result = json.load(file_json)

        classes = []

        for clas in _result["classes"]:
            classes.append(Class(
                id=clas["id"],
                course=Course(
                    id=clas["course"]["id"],
                    name=clas["course"]["name"],
                    lecturers=None,
                    is_practice=clas["course"]["is_practice"],
                    num_classes=clas["course"]["num_classes"]
                ),
                lecturer=Lecturer(
                    id=clas["lecturer"]["id"],
                    name=clas["lecturer"]["name"],
                ),
                room=Room(
                    id=clas["room"]["id"],
                    name=clas["room"]["name"]
                ),
                day=clas["day"],
                shift=Shift(
                    id=clas["shift"]["id"],
                    time=clas["shift"]["time"]
                ),
            ))
        return classes


if __name__ == "__main__":
    classes = Schedule.load()
