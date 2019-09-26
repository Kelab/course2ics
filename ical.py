import uuid
import time


def get_now_time():
    """
    获取当前时间
    参数：
        isUTC 是否需要返回UTC时间
    """
    return time.strftime("%Y%m%dT%H%M%S", time.localtime())


class Calendar:
    def __init__(self, semester_name, user_id):
        self.user = user_id
        self.semester_name = semester_name
        self.front_matter = (f"BEGIN:VCALENDAR\n"
                             "PRODID:-//BuddingLab //西南科技大学 课程表 1.1//CN\n"
                             "VERSION:2.0\n"
                             "CALSCALE:GREGORIAN\n"
                             "METHOD:PUBLISH\n"
                             f"X-WR-CALNAME:{semester_name}\n"
                             "X-WR-TIMEZONE:Asia/Shanghai\n"
                             "BEGIN:VTIMEZONE\n"
                             "TZID:Asia/Shanghai\n"
                             "X-LIC-LOCATION:Asia/Shanghai\n"
                             "BEGIN:STANDARD\n"
                             "TZOFFSETFROM:+0800\n"
                             "TZOFFSETTO:+0800\n"
                             "TZNAME:CST\n"
                             "DTSTART:19700101T000000\n"
                             "END:STANDARD\n"
                             "END:VTIMEZONE\n")
        self.foot_matter = "END:VCALENDAR"
        self.events = []

    def write(self, path=''):
        # 会在当前目录生成一个当前学期的ics文件。
        with open(path + str(self.user) + "-" + self.semester_name + '.ics',
                  'w',
                  encoding='utf8') as f:
            f.write(self.front_matter)
            for event in self.events:
                f.write(str(event))
            f.write(self.foot_matter)
        print('Done')


class Event:
    def __str__(self):
        return self.event

    def __init__(self, dt: dict, location: str, summary: str,
                 rrule: dict = {}):
        """
        参数：
            dt 字典类型 有两个值， dt['sk']是上课时间 dt['xk']是下课时间
            location 上课地点
            summary 课程名 + 老师名 ： 离散数学 - 巫玲
            rrule 可选字典类型 如果指定的话说明课是需要重复的
                以下为字典字段的要求：
                FREQ：表示重复规则的类型, 是重复规则中必须定义的一条属性。
                    上课周期 一般都是一周一次
                    SECONDLY， MINUTELY， HOURLY， DAILY，WEEKLY，MONTHLY，YEARLY
                COUNT：数字 执行次数 按照FREQ的周期执行N次
                BYDAY：
                    取值范围： MO（周一）， TU（周二）， WE（周三）， TU（周四）， FR（周五）， SA（周六）， SU（周日）。可以有多个值，用逗号分隔。
                    每个值可以在前面加上一个正整数（+n）或者负整数（-n），用以在 MONTHLY 或者 YEARLY 的重复类型中表示第 n 个周几。 例如，在一个 MONTHLY 类型的重复规则中， +1MO（或者1MO）表示这个月的第1个周一，如果是 -1MO 则表示这个月的最后1个周一。
                    如果前面没有数字，则表示在这个重复类型中的所有的周几， 比如在一个 MONTHLY 的重复类型中， MO 表示这个月里所有的周一。

            如果重复规则中未包含 UNTIL 和 COUNT 属性， 则表示该重复规则无限重复。
                UNTIL：Date格式 直到某日为止
                    19971224T000000Z
                    这个日期-时间值表示这个重复规则的最后一次事件的发生时间。
                INTERVAL： 数字 表示重复规则的间隔 默认为1
                WKST： 默认为MO 取值范围 MO, TU, WE, TH, FR, SA, SU
                    当一个 WEEKLY 类型的重复规则， INTERVAL 大于 1， 且带有 BYDAY 属性时， 则必须带有 WKST 属性。 当一个 YEARLY 类型的重复规则带有 BYWEEKNO 属性时， 也必须带有 WKST 属性。
        """

        uid = str(uuid.uuid3(uuid.NAMESPACE_URL, location + summary +
                             dt['sk'])).replace('-', '') + '@SWUST'
        self.event = ("BEGIN:VEVENT\n"
                      f"DTSTAMP:{get_now_time()}\n"
                      f"UID:{uid}\n"
                      f"CREATED:{get_now_time()}\n"
                      f"LAST-MODIFIED:{get_now_time()}\n"
                      "SEQUENCE:0\n"
                      "STATUS:CONFIRMED\n"
                      "TRANSP:OPAQUE\n")
        self.add_info(dt, location, summary)
        self.add_rrule(rrule)
        self.add_alarm()
        self.event += "END:VEVENT\n"

    def add_rrule(self, rrule):
        if rrule.get('COUNT') > 1:
            self.event += ("RRULE:FREQ=WEEKLY;WKST=MO;"
                           f"COUNT={rrule['COUNT']};"
                           f"BYDAY={rrule['BYDAY']}\n")

    def add_info(self, dt: dict, location, summary):
        self.event += (f"DTSTART;TZID=Asia/Shanghai:{dt['sk']}\n"
                       f"DTEND;TZID=Asia/Shanghai:{dt['xk']}\n"
                       f"LOCATION:{location}\n"
                       f"SUMMARY:{summary}\n"
                       f"DESCRIPTION:{summary}\n")

    def add_alarm(self):
        self.event += ("BEGIN:VALARM\n"
                       "ACTION:DISPLAY\n"
                       "DESCRIPTION:This is an event reminder\n"
                       "TRIGGER:-P0DT0H30M0S\n"
                       "END:VALARM\n"
                       "BEGIN:VALARM\n"
                       "ACTION:DISPLAY\n"
                       "DESCRIPTION:This is an event reminder\n"
                       "TRIGGER:-P0DT0H10M0S\n"
                       "END:VALARM\n")
