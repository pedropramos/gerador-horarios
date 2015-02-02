class TimetableGenerator:

    def __init__(self):
        self.generated = []
        self.total_combinations = 0

    def store_timetable(self, tt):
        self.total_combinations += 1
        tt.heuristic = tt.total_time()
        
        if len(self.generated) < 99:
            self.generated.append(tt)
        elif len(self.generated) == 99:
            self.generated.append(tt)
            self.move_worst_to_last()
        else:
            if tt.heuristic < self.generated[99].heuristic:  # tt is better
                self.generated.pop(99)
                self.generated.append(tt)
                self.move_worst_to_last()

    def move_worst_to_last(self):
        worst_heuristic = 0
        for timetable in self.generated:
            if timetable.heuristic > worst_heuristic:
                worst_heuristic = timetable.heuristic
                worst_tt = timetable
        self.generated.remove(worst_tt)
        self.generated.append(worst_tt)
    
    def generate_timetables(self, lesson_blocks):
        self.generate(Timetable(), lesson_blocks)

    def generate(self, timetable, lesson_blocks):
        if not lesson_blocks:
            self.store_timetable(timetable)
        else:
            next_lesson_block = lesson_blocks[0]
            for shift in next_lesson_block.shifts:
                if timetable.supports(shift):
                    self.generate(timetable.append_shift(shift), lesson_blocks[1:])

class Timetable:

    def __init__(self):
        self.lessons = []

    def append_shift(self, shift):
        new_timetable = Timetable()
        new_timetable.lessons.extend(self.lessons)
        new_timetable.lessons.extend(shift.slots)
        return new_timetable

    def supports(self, shift):
        for slot in shift.slots:
            for existing in self.lessons:
                if (slot.overlaps_with(existing)):
                    return False
        return True

    #def is_feasible(self):
    #    for slot in self.lessons:
    #        for other in self.lessons:
    #            if (slot is not other) and (slot.overlaps_with(other)):
    #                return False
    #    return True

    # heuristics for selecting timetables
    def total_time(self):
        result = 0
        for weekday in range(Weekday.MONDAY, Weekday.SUNDAY):
            daily_lessons = [slot for slot in self.lessons if slot.day == weekday]
            if daily_lessons:
                earliest_start = min([slot.start.minutes for slot in daily_lessons])
                latest_end = max([slot.end.minutes for slot in daily_lessons])
                interval = latest_end - earliest_start
                result += interval + 60
        return result
        

class Course(object):

    def __init__(self, name):
        self.name = name
        self.lesson_blocks = []

    def add_lesson_block(self, lesson_block):
        self.lesson_blocks.append(lesson_block)
        lesson_block.parent_course = self

    def get_block_by_category(self, category):
        for block in self.lesson_blocks:
            if block.category == category:
                return block

class LessonBlock:

    def __init__(self, category):
        self.category = category
        self.shifts = []

    def add_shift(self, shift):
        self.shifts.append(shift)
        shift.parent_lesson_block = self

class Shift:

    def __init__(self, name):
        self.name = name
        self.slots = []

    def add_lesson_slot(self, lesson_slot):
        self.slots.append(lesson_slot)
        lesson_slot.parent_shift = self

class LessonSlot:

    def __init__(self, day, start, end, room):
        self.day = day
        self.start = start
        self.end = end
        self.room = room

    def course_name(self):
        return self.parent_shift.parent_lesson_block.parent_course.name

    def lesson_category(self):
        return self.parent_shift.parent_lesson_block.category

    def overlaps_with(self, other):
        return self.day == other.day and \
               self.start.is_before(other.end) and \
               self.end.is_after(other.start)

class Weekday:
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class Time:

    def __init__(self, hour, minute):
        self.minutes = hour * 60 + minute

    def is_before(self, other):
        return self.minutes < other.minutes

    def is_after(self, other):
        return self.minutes > other.minutes

    def __str__(self):
        return "%d:%02d" % (self.minutes/60, self.minutes%60)
