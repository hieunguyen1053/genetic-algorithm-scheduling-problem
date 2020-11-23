from genetic_algorithm import GeneticAlgorithm, Population
import random

from flask import Flask, redirect, render_template, request

from schedule import Class, Course, Lecturer, Room, Schedule

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/schedule')


@app.route('/course')
def course():
    courses = Course.load()
    return render_template('course.html', courses=courses)


@app.route('/schedule')
def schedule():
    classes = Schedule.load()
    num_conflict = 0
    for i in range(len(classes)):
        classes[i].time = Class.DAYS[classes[i].day] + " " + classes[i].shift.time
        if classes[i].conflict:
            num_conflict += 1
    return render_template('schedule.html', classes=classes, num_conflict=num_conflict)


@app.route('/lecturer')
def lecturer():
    lecturers = Lecturer.load()
    return render_template('lecturer.html', lecturers=lecturers)


@app.route('/room')
def room():
    rooms = Room.load()
    return render_template('room.html', rooms=rooms)


@app.route('/schedule-table')
def schedule_table():
    classes = Schedule.load()
    if request.args.get("lecturer"):
        arg = request.args.get("lecturer")
        classes = filter(lambda x: x.lecturer.id == arg, classes)
        classes = list(classes)
    elif request.args.get("course"):
        arg = request.args.get("course")
        classes = filter(lambda x: x.course.id == arg, classes)
        classes = list(classes)
    elif request.args.get("room"):
        arg = request.args.get("room")
        classes = filter(lambda x: x.room.name == arg, classes)
        classes = list(classes)

    colors = ["#"+''.join([random.choice('0123456789ABCDEF')
                           for j in range(6)]) for i in range(len(classes))]
    count = 0
    rows = []
    for i in range(0, 15):
        cols = []
        for j in range(0, 7):
            _classes = [clas for clas in classes if clas.day == j and clas.shift.id - 1 == i // 3]

            if len(_classes) != 0:
                if i % 3 == 0:
                    for k in range(len(_classes)):
                        _classes[k].color = colors[count]
                        count += 1
                    cols.append(_classes)
            else:
                cols.append(None)
        rows.append(cols)

    for i in range(len(classes)):
        classes[i].time = Class.DAYS[classes[i].day] + \
            " " + classes[i].shift.time
    return render_template('schedule-table.html', classes=classes, rows=rows)

@app.route('/api/process')
def process():
    population = Population(size=10)
    population.chromosomes.sort(key=lambda x: x.get_fitness(), reverse=True)
    genetic_algorithm = GeneticAlgorithm()
    for _ in range(50):
        population = genetic_algorithm.evolve(population)
        if population.chromosomes[0].get_fitness() == 1.0:
            break
    population.chromosomes[0].save()
    return {"message": "Successfully"}

if __name__ == "__main__":
    app.run(use_reloader=True)
