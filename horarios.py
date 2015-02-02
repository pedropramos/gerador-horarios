import sys
import urllib
from tt_parser import *
from tt_generator import *
from tt_prettyprinter import *
from tt_errorprinter import *

def is_url(arg):
    return arg[0:4] == "http"

lesson_blocks = []
for arg_encoded in sys.argv[1:]:
    arg = urllib.unquote(arg_encoded)
    if is_url(arg):
        current_course = HTMLCourseParser(arg).parse()
    else:
        lesson_blocks.append(current_course.get_block_by_category(arg))

generator = TimetableGenerator()
generator.generate_timetables(lesson_blocks)

generator.generated.sort(key=Timetable.total_time)

if generator.generated:
    printer = HTMLPrettyPrinter()
    printer.print_timetables(generator.generated, generator.total_combinations)
else:
    printer = HTMLErrorPrinter()
    print printer.no_timetables()