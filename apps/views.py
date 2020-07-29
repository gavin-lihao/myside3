from django.shortcuts import render, HttpResponse, redirect
import pymysql
from utils import sqlhelper
import json
import time


def index(request):
    return render(request, "index.html")


def classes(request):
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root1234', db='db_mysite')
    #
    # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # cursor.execute("select class_id,class_name from classes")
    # classes_list = cursor.fetchall()
    # cursor.close()
    # conn.close()

    classes_list = sqlhelper.get_list("select class_id,class_name from class_info", [])
    return render(request, 'classes.html', {'classes_list': classes_list})


def add_class(request):
    if request.method == "GET":
        return render(request, 'add_class.html')
    else:
        v = request.POST.get('title')
        if len(v) > 0:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root1234', db='db_mysite')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute("insert into classes(class_name) values(%s)", [v, ])
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/classes/')
        else:
            return render(request, 'add_class.html', {'message': '班级列表不能为空'})


def del_class(request):
    nid = request.GET.get('nid')
    sqlhelper.delete("delete from class_info where class_id=%s", [nid, ])
    return redirect('/classes')


def edit_class(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root1234', db='db_mysite')

        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select class_id,class_name from classes where id=(%s)", [nid, ])
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return render(request, 'edit_class.html', {'result': result})
    else:
        nid = request.GET.get('nid')
        title = request.POST.get('title')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root1234', db='db_mysite')

        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update classes set class_name=(%s) where class_id=(%s)", [title, nid, ])
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/classes/')


def students(request):
    '''
    student's list
    :param request: 封装请求相关的所有信息
    :return:
    '''
    # 获取学生列表
    students_list = sqlhelper.get_list(
        'select stu_info.stu_id,stu_info.stu_name,stu_info.stu_class_id,class_info.class_name FROM stu_info LEFT JOIN class_info ON stu_info.stu_class_id = class_info.class_id',
        [])
    # 获取班级列表
    classes_list = sqlhelper.get_list(
        'select class_id,class_name from class_info',
        [])

    return render(request, 'students.html', {'students_list': students_list, 'classes_list': classes_list})


def add_student(request):
    if request.method == "GET":

        classes_list = sqlhelper.get_list(
            'select class_id,class_name from class_info', []
        )
        return render(request, 'add_student.html', {'classes_list': classes_list})
    else:
        stu_name = request.POST.get('stu_name')
        class_id = request.POST.get('classId')
        sqlhelper.add("insert into stu_info(stu_name,stu_class_id) values(%s,%s)", [stu_name, class_id])
        return redirect('/students/')


def del_student(request):
    nid = request.GET.get('nid')
    sqlhelper.delete('delete from stu_info where stu_id=(%s)', [nid, ])
    return redirect('/students/')


def edit_student(request):
    nid = request.GET.get('nid')
    if request.method == 'GET':
        class_list = sqlhelper.get_list('select class_id,class_name from class_info', [])
        stu_name = sqlhelper.get_one('select stu_id,stu_name,stu_class_id from stu_info where stu_id=%s', [nid, ])
        return render(request, 'edit_student.html', {'class_list': class_list, 'stu_name': stu_name})
    else:
        stu_name = request.POST.get('stu_name')
        class_id = request.POST.get('classId')
        sqlhelper.modify('update stu_info set stu_name = %s,stu_class_id=%s where stu_id = %s',
                         [stu_name, class_id, nid])
        return redirect('/students/')


def modal_add_class(request):
    class_name = request.POST.get('className')
    if len(class_name) > 0:

        sqlhelper.add("insert into class_info(class_name) values(%s)", [class_name, ])
        return HttpResponse('ok')
    else:
        return HttpResponse('班级列表不能为空')


def modal_edit_class(request):
    res = {'state': True, 'message': None}
    try:
        class_name = request.POST.get('editClassName')
        class_id = request.POST.get('editClassId')
        sqlhelper.modify("update class_info set class_name=%s where class_id=%s", [class_name, class_id, ])
    except Exception as e:
        res['state'] = False
        res['message'] = '处理异常'

    return HttpResponse(json.dumps(res))


def modal_add_student(request):
    res = {'state': True, 'message': None}
    try:
        stu_name = request.POST.get('stu_name')
        class_id = request.POST.get('class_id')
        sqlhelper.add("insert into stu_info(stu_name,stu_class_id) values(%s,%s)", [stu_name, class_id])
        # sqlhelper.add("insert into stu_info(stu_name,stu_class_id) values(%s,%s)", [stu_name,class_id])
    except Exception as e:
        res['state'] = False
        res['message'] = str(e)

    return HttpResponse(json.dumps(res))


def modal_edit_student(request):
    res = {'state': True, 'message': None}
    try:
        stu_id = request.POST.get('stu_id')
        stu_name = request.POST.get('stu_name')
        stu_class_id = request.POST.get('class_id')
        sqlhelper.modify('update stu_info set stu_name=%s,stu_class_id=%s where stu_id=%s',
                         [stu_name, stu_class_id, stu_id])

    except Exception as e:
        res['state'] = False
        res['message'] = str(e)
    return HttpResponse(json.dumps(res))


def teachers(request):
    # teas_list = sqlhelper.get_list('select tea_id,tea_name from tea_info',[])

    teas_list = sqlhelper.get_list("""
        SELECT tea_info.tea_id as tea_id,tea_info.tea_name as tea_name,class_info.class_id as class_id,class_info.class_name as class_name from tea_info
            LEFT JOIN teatocla on tea_info.tea_id = teatocla.teatocla_tea_id
            LEFT JOIN class_info ON class_info.class_id = teatocla.teatocla_class_id
    """, [])
    result = {

    }
    for row in teas_list:
        tea_id = row['tea_id']
        if tea_id in result:
            result[tea_id]['class_name'].append(row['class_name'])
            result[tea_id]['class_id'].append(row['class_id'])
        else:
            result[tea_id] = {'tea_id': row['tea_id'], 'tea_name': row['tea_name'], 'class_id': [row['class_id'], ],
                              'class_name': [row['class_name'], ]}
    # print(result)
    return render(request, 'teachers.html', {'teas_list': result.values()})


# 新url增加老师
def add_teacher(request):
    if request.method == "GET":
        classes_list = sqlhelper.get_list('select class_id,class_name from class_info', [])
        return render(request, 'add_teacher.html', {"classes_list": classes_list})
    else:
        tea_name = request.POST.get('tea_name')
        lastrowid = sqlhelper.create('insert into tea_info(tea_name) values(%s)', [tea_name, ])
        class_list = request.POST.getlist('class_ids')

        # for row in class_list:
        #     sqlhelper.modify('insert into teatocla(teatocla_tea_id,teatocla_class_id) values(%s,%s)',
        #                      [lastrowid, row, ])

        # 连接一次,提交多次
        # obj = sqlhelper.SqlHelper()
        # for row in class_list:
        #     sqlhelper.modify('insert into teatocla(teatocla_tea_id,teatocla_class_id) values(%s,%s)',
        #                      [lastrowid, row, ])
        # obj.close()

        # 连接一次，提交一次
        data_list = []
        for row in class_list:
            temp = (lastrowid, row)
            data_list.append(temp)
        # print(data_list)
        obj = sqlhelper.SqlHelper()
        obj.multiple_modify('insert into teatocla(teatocla_tea_id,teatocla_class_id) values(%s,%s)',
                            data_list)
        obj.close()

        return redirect('/teachers/')


def del_teacher(request):
    nid = request.GET.get('nid')
    sqlhelper.delete('delete from tea_info where tea_id=%s', [nid, ])
    return redirect('/teachers/')


def edit_teacher(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        obj = sqlhelper.SqlHelper()
        teacher = obj.get_one('select tea_id,tea_name from tea_info where tea_id=%s', [nid, ])
        teatocla_list = obj.get_list('select teatocla_class_id from teatocla where teatocla_tea_id =%s', [nid, ])
        classes_list = obj.get_list('select class_id,class_name from class_info', [])
        obj.close()
        temp = []
        for row in teatocla_list:
            temp.append(row['teatocla_class_id'])
        return render(request, "edit_teacher.html", {
            'teacher': teacher,
            'teatocla_list': temp,
            'classes_list': classes_list,
        })

    else:
        tea_id = request.GET.get('nid')
        tea_name = request.POST.get('tea_name')
        class_id = request.POST.getlist('class_ids')

        data_list = []
        for row in class_id:
            temp = (tea_id, row)
            data_list.append(temp)
        print(data_list)

        obj = sqlhelper.SqlHelper()
        obj.modify('update tea_info set tea_name = %s where tea_id = %s', [tea_name, tea_id])
        obj.modify('delete from teatocla where teatocla_tea_id = %s', [tea_id, ])
        obj.multiple_modify('insert into teatocla(teatocla_tea_id,teatocla_class_id) values(%s,%s)', data_list)
        obj.close()
        return redirect('/teachers/')


# 加载老师列表，对话框添加老师方式的班级列表
def get_all_classes(request):
    # time.sleep(1)
    obj = sqlhelper.SqlHelper()
    classes_list = obj.get_list('select class_id,class_name from class_info', [])
    # print(classes_list)
    obj.close()
    return HttpResponse(json.dumps(classes_list))


def modal_add_teachers(request):
    res = {'state': True, 'message': None}
    try:
        tea_name = request.POST.get('tea_name')
        class_list = request.POST.getlist('add_class_list')
        obj = sqlhelper.SqlHelper()
        tea_id = obj.create('insert into tea_info(tea_name) values(%s)', [tea_name, ])
        result = []
        for row in class_list:
            temp = (tea_id, row)
            result.append(temp)
        obj.multiple_modify('insert into teatocla(teatocla_tea_id,teatocla_class_id) values(%s,%s)', result)
    except Exception as e:
        res['state'] = False
        res['message'] = str(e)
    return HttpResponse(json.dumps(res))


def get_tea_class_list(request):
    obj = sqlhelper.SqlHelper()
    classes_list = obj.get_list('select class_id,class_name from class_info', [])
    datalist = {'classes_list': classes_list}
    obj.close()

    return HttpResponse(json.dumps(classes_list))


def modal_edit_teacher(request):
    res = {'state': True, 'message': None}
    try:
        tea_name = request.POST.get('tea_name')
        tea_id = request.POST.get('tea_id')
        classes_list = request.POST.getlist('classes_list')

        obj = sqlhelper.SqlHelper()
        obj.modify('update tea_info set tea_name = (%s) where tea_id= %s', [tea_name, tea_id, ])
        obj.modify('delete from teatocla where teatocla_tea_id = %s', [tea_id, ])

        result = []
        for row in classes_list:
            temp = (tea_id, row)
            result.append(temp)

        # print(result)
        obj.multiple_modify('insert into teatocla(teatocla_tea_id,teatocla_class_id) values (%s,%s)', result)
        obj.close()
    except Exception as e:
        res['state'] = False
        res['message'] = str(e)

    return HttpResponse(json.dumps(res))
