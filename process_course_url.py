import sys
import urllib
from tt_parser import *
from tt_generator import *
from tt_prettyprinter import *

course_id = int(sys.argv[1])
url = urllib.unquote(sys.argv[2])

parser = HTMLCourseParser(url)
course = parser.parse()

html_result = "<div id='coursediv" + str(course_id) + "' >"
html_result += "<img src='line.png' />"
html_result += "<h1 class='mtop0 mbottom03 cnone' style='font-size: 14px'>%s" % (course.long_name)
html_result += "<span class='greytxt' style='font-size: 10px;'> (%s)</span>" % (course.name)
html_result += "&nbsp&nbsp<img src='remove.png' onclick='removeCourse(coursediv" + str(course_id) + ")' />"
html_result += "</h1>"
html_result += "<input type='hidden' name='course%i' value='%s'>" \
               % (course_id, url)

block_id = 0
sorted_blocks = sorted(course.lesson_blocks, key=lambda x: x.category, reverse=True)
for block in sorted_blocks:
    block_id += 1
    html_result += "<input type='checkbox' name='course%itype%i' value='%s' checked>%s&nbsp;" \
                   % (course_id, block_id, block.category, block.category)

html_result += "</div>"

print html_result
