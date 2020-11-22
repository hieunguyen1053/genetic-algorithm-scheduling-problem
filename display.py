from typing import List

from prettytable import PrettyTable

from genetic_algorithm import GeneticAlgorithm, Population
from schedule import Schedule, Shift, Room, Lecturer, Class, Course


class Display:
    i = 0

    def print_available_data(self) -> None:
        print("> All available data")
        self.print_courses(Course.load())
        self.print_lecturers(Lecturer.load())
        self.print_rooms(Room.load())
        self.print_shifts(Shift.load())

    def print_courses(self, courses: List[Course]) -> None:
        x = PrettyTable()
        x.field_names = ["id", "name", "lecturers"]
        for course in courses:
            x.add_row([course.id, course.name, ", ".join(
                lecturer.name for lecturer in course.lecturers)])
        print(x)

    def print_lecturers(self, lecturers: List[Lecturer]) -> None:
        x = PrettyTable()
        x.field_names = ["id", "name"]
        for lecturer in lecturers:
            x.add_row([lecturer.id, lecturer.name])
        print(x)

    def print_rooms(self, rooms: List[Room]) -> None:
        x = PrettyTable()
        x.field_names = ["id", "name"]
        for room in rooms:
            x.add_row([room.id, room.name])
        print(x)

    def print_shifts(self, shifts: List[Shift]) -> None:
        x = PrettyTable()
        x.field_names = ["id", "time"]
        for shift in shifts:
            x.add_row([shift.id, shift.time])
        print(x)

    def print_chromosomes(self, chromosomes: List[Schedule]) -> None:
        x = PrettyTable()
        x.field_names = ["#", "fitness", "conflicts"]
        for idx, schedule in enumerate(chromosomes):
            x.add_row([
                idx,
                schedule.get_fitness(),
                schedule.get_num_conflicts(),
            ])
        print("Generation {}".format(self.i))
        print(x)
        self.i += 1

    def print_classes(self, classes: List[Class]):
        x = PrettyTable()
        classes.sort(key=lambda x: (
            x.lecturer.name, x.course.id, x.day, x.shift.id))
        x.field_names = ["#", "course", "room", "lecturer", "time"]
        for idx, clas in enumerate(classes):
            x.add_row([
                idx,
                clas.course.name,
                clas.room.name,
                clas.lecturer.name,
                f"{Class.DAYS[clas.day]} {clas.shift.time}",
            ])
        print(x)


if __name__ == "__main__":
    display = Display()
    display.print_available_data()

    population = Population(size=10)
    population.chromosomes.sort(key=lambda x: x.get_fitness(), reverse=True)
    display.print_chromosomes(population.chromosomes)

    genetic_algorithm = GeneticAlgorithm()
    for i in range(50):
        population = genetic_algorithm.evolve(population)
        display.print_chromosomes(population.chromosomes)
        if population.chromosomes[0].get_fitness() == 1.0:
            break

    population.chromosomes[0].save()
    display.print_classes(population.chromosomes[0].classes)
