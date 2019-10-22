import time
from constants import INFO
from ical import Calendar, Event


def get_one_date(aweek, aday, atime):
    """
    参数：
        aweek: 某周
        aday:  该周某日
        atime: 该日某时(分)单位ms
    返回值：
        形如 '20181018T080000Z' 的表示时间的字符串
        T  "T" appears literally in the string, to indicate the beginning of the time element.
        Z  is the time zone offset specified as "Z" (for UTC) or either "+" or "-" followed by a time expression HH:mm
    """
    startDate = int(
        time.mktime(time.strptime(INFO.semester_start_day, "%Y-%m-%d"))) * 1000

    target_day = startDate + 86400 * (aweek - 1) * 7 * 1000 + 86400 * (
        aday - 1) * 1000 + atime
    time_local = time.localtime(target_day / 1000)
    return time.strftime("%Y%m%dT%H%M%S", time_local)


def process_class_time(class_time, first_week):
    """
    :param sk_time: api中的上课时间: 6@3_4
    :param first_week: 第一次开课的周数
    :return:
        weekday 数字 星期几的意思
        class_number 数字 第几讲上课
    """
    weekday_dict = {
        1: 'MO',
        2: 'TU',
        3: 'WE',
        4: 'TH',
        5: 'FR',
        6: 'SA',
        7: 'SU',
    }
    class_number_dict = {1: 8, 2: 10, 3: 14, 4: 16, 5: 19, 6: 21}

    dt = {}
    weekday = int(class_time[0])  # 星期几上课
    class_number = class_number_dict[int(class_time[2])]  # 第几讲课
    class_period = int(class_time[4])  # 上几节课

    # 因为不存在奇数节课 所以调整一下
    if class_period % 2 != 0:
        class_period = class_period - 1

    class_period_count = class_period / 2  # 算算有多少讲课

    # 讲间 休息时间
    big_break_time = (class_period_count - 1) * 20 * 60 * 1000

    # 开始上课的时间
    start_class_time = class_number * 60 * 60 * 1000  # 开始上课的时间

    # 一讲课要的时间
    break_time = 10  # 课件休息时间 单位分钟
    spend_time = (2 * 45 + break_time) * 60 * 1000  # 共耗时 单位毫秒

    # n讲课 需要的时间
    spend_time = spend_time * class_period_count + big_break_time
    complete_class_time = start_class_time + spend_time

    dt['sk'] = get_one_date(first_week, weekday, start_class_time)
    dt['xk'] = get_one_date(first_week, weekday, complete_class_time)
    return weekday_dict[weekday], dt


def generate_class_schedule(api: dict, username, path):
    # 本学期的名称
    semester_name = INFO.semester_name
    print('semester_name： ', semester_name)
    ics = Calendar(semester_name, username)
    course_lists = api['result']
    for course in course_lists:
        class_name = course['class_name']  # 课程名称
        class_time = course['class_time']  # 上课时间 type: list
        location = course['location']  # 教学地点 type: list
        teacher_name = course['teacher_name']  # 教师姓名

        for _time, _location in zip(class_time, location):
            print(class_name + '-' + _location)
            startWeek = int(course['qsz'])  # 该门课起始周
            endWeek = int(course['zzz'])  # 该门课结束周
            weeks_count = endWeek - startWeek + 1  # 该门课共上多少周
            weekday, dt = process_class_time(_time,
                                             startWeek)  # 获取上课的 年月日时分 周几
            print(weekday, dt)
            summary = class_name + f'({teacher_name})'  # 日历中的标题
            rrule = {
                'BYDAY': weekday,
                'COUNT': weeks_count,
            }

            ics.events.append(Event(dt, _location, summary, rrule))
    ics.write(path)
