from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
import json
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .forms import AddStudentForm, EditStudentForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


def admin_home(request):
    return render(request,'hod_template/home_content.html')


def add_staff(request):
    return render(request,'hod_template/add_staff.html')


def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        try:
            user = CustomUser.objects.create_user(username=username, password=password,email=email, last_name=last_name, first_name=first_name, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, 'Successfully added staff')
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, 'Failed to add staff')
            return HttpResponseRedirect(reverse("add_staff"))


def add_course(request):
    return render(request,'hod_template/add_course.html')


def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course = request.POST.get("course")
        print(course)
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))


def add_student(request):
    form = AddStudentForm()
    return render(request,'hod_template/add_student.html',{'form':form})


def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            session_year_id = form.cleaned_data['session_year_id']
            course_id = form.cleaned_data['course']
            sex = form.cleaned_data['sex']

            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(username=username, password=password,email=email, last_name=last_name, first_name=first_name, user_type=3)
                user.students.address = address
                user.students.gender = sex
                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj
                session_year = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, 'Successfully added student')
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request,"Failed To Add student")
                return HttpResponseRedirect(reverse("add_student"))
        
        else:
            form = AddStudentForm(request.POST)
            return render(request,'hod_template/add_student.html',{'form':form})



def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request,'hod_template/add_subject.html',{'courses':courses, 'staffs':staffs})


def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)
        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, 'Successfully added subject')
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed To Add subject")
            return HttpResponseRedirect(reverse("add_subject"))


def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request,'hod_template/manage_staff.html',{'staffs':staffs})


def manage_student(request):
    students = Students.objects.all()
    return render(request,'hod_template/manage_student.html',{'students':students})


def manage_course(request):
    courses = Courses.objects.all()
    return render(request,'hod_template/manage_course.html',{'courses':courses})


def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request,'hod_template/manage_subject.html',{'subjects':subjects})
        

def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request,'hod_template/edit_staff.html',{'staff':staff,'id':staff_id})


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        staff_id = request.POST.get('staff_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request, 'Successfully edited staff')
            return HttpResponseRedirect(reverse("edit_staff", kwargs={'staff_id':staff_id}))
        except:
            messages.error(request,"Failed To edit Staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={'staff_id':staff_id}))


def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.course_id.id
    form.fields['sex'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id
    return render(request,'hod_template/edit_student.html',{'form':form, 'id':student_id, 'username':student.admin.username})


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return HttpResponseRedirect(reverse("manage_student"))
        
        form = EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            session_year_id = form.cleaned_data['session_year_id']
            course_id = form.cleaned_data['course']
            sex = form.cleaned_data['sex']

            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                student = Students.objects.get(admin=student_id)
                student.address = address
                student.gender = sex
                session_year = SessionYearModel.objects.get(id=session_year_id)
                student.session_year_id = session_year
                student.save()
                course = Courses.objects.get(id=course_id)
                student.course_id=course
                if profile_pic_url != None:
                    student.profile_pic = profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request, 'Successfully edited student')
                return HttpResponseRedirect(reverse("edit_student", kwargs={'student_id':student_id}))
            except:
                messages.error(request,"Failed To edit Student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={'student_id':student_id}))
        
        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin=student_id)
            return render(request,'hod_template/edit_student.html',{'form':form, 'id':student_id, 'username':student.admin.username})


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request,'hod_template/edit_subject.html',{'subject':subject, 'courses':courses, 'staffs':staffs,'id':subject_id})


def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        staff_id = request.POST.get('staff')
        course_id = request.POST.get('course')
        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            subject.save()
            messages.success(request, 'Successfully edited subject')
            return HttpResponseRedirect(reverse("edit_subject", kwargs={'subject_id':subject_id}))
        except:
            messages.error(request,"Failed To edit subject")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={'subject_id':subject_id}))


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(request,'hod_template/edit_course.html',{'course':course,'id':course_id})


def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course')
        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, 'Successfully edited course')
            return HttpResponseRedirect(reverse("edit_course", kwargs={'course_id':course_id}))
        except:
            messages.error(request,"Failed To edit course")
            return HttpResponseRedirect(reverse("edit_course", kwargs={'course_id':course_id}))


def manage_session(request):
    return render(request,'hod_template/manage_session.html')

def add_session_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year = request.POST.get('session_start')
        session_end_year = request.POST.get('session_end')
        try:
            session_year = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            session_year.save()
            messages.success(request, 'Successfully added session')
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request,"Failed To add session")
            return HttpResponseRedirect(reverse("manage_session"))

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get('email')
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get('username')
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def staff_feedback_message(request):
    feedbacks = FeedBackStaff.objects.all()
    return render(request,'hod_template/staff_feedback_template.html',{'feedbacks':feedbacks})


@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id = request.POST.get('id')
    feedback_message = request.POST.get('message')
    try:
        feedback = FeedBackStaff.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    return render(request,'hod_template/student_feedback_template.html',{'feedbacks':feedbacks})


@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id = request.POST.get('id')
    feedback_message = request.POST.get('message')
    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False") 


def staff_leave_view(request):
    return render(request,'hod_template/staff_leave_view.html')


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    return render(request,'hod_template/student_leave_view.html',{'leaves':leaves})


def student_approve_leave(request,leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse('student_leave_view'))


def student_disapprove_leave(request,leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse('student_leave_view'))


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    return render(request,'hod_template/staff_leave_view.html',{'leaves':leaves})


def staff_approve_leave(request,leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse('staff_leave_view'))


def staff_disapprove_leave(request,leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse('student_leave_view'))


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_year_id = SessionYearModel.objects.all()
    return render(request,'hod_template/admin_view_attendance.html',{'subjects':subjects, 'session_year_id':session_year_id})


@csrf_exempt
def admin_get_attendance_dates(request):
    subject = request.POST.get('subject')
    session_year_id = request.POST.get('session_year_id')
    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {'id':attendance_single.id, 'attendance_date':str(attendance_single.attendance_date), 'session_year_id':attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request,'hod_template/admin_profile.html',{'user':user})


def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse('admin_profile'))
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password!=None and password!='':
                customuser.set_password(password)
            customuser.save()
            messages.success(request, 'Successfully updated profile')
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request,"Failed to update profile")
            return HttpResponseRedirect(reverse("admin_profile"))

