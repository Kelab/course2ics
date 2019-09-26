class INFO:
    # 校历 http://www.dean.swust.edu.cn/type/2c9fd0b8655589e50165558a19a9000e/page/2c9fd0b8655589e50165558a19a9000f
    semester_name = '2019-2020-1'
    semester_start_day = "2019-08-26"


class API:
    jwc_course_table = "https://matrix.dean.swust.edu.cn/acadmicManager/index.cfm?event=studentPortal:courseTable"
    # 实验课的一些 信息 和 数据
    syk_base_url = "http://202.115.175.177"
    syk_verify_url = "http://202.115.175.177/swust/"
    syk_course_table = "http://202.115.175.177/StuExpbook/book/bookResult.jsp"
    captcha_url = 'http://cas.swust.edu.cn/authserver/captcha.html'
    login_url = 'http://cas.swust.edu.cn/authserver/login?service=http://my.swust.edu.cn/mht_shall/a/service/serviceFrontManage/cas'
    studentInfo = 'http://my.swust.edu.cn/mht_shall/a/service/studentInfo'
    studentMark = 'http://my.swust.edu.cn/mht_shall/a/service/studentMark'
