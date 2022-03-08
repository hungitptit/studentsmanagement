from os import name
#from turtle import color
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, request
from matplotlib.style import context

#from matplotlib.style import context
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.core.files.storage import FileSystemStorage
import datetime as dt
#Simport os
##import json


# Create your views here.
@login_required(login_url='/login') # Check login
def add_student(request):
    current_user = request.user
    CLASS_CHOICES = []
    classes = Class.objects.filter(user=current_user)
    for aclass in classes:
        CLASS_CHOICES.append((aclass.id,aclass.name))  
    if request.method == 'POST':
        form = AddStudentForm(request.POST, request.FILES, CLASS_CHOICES=CLASS_CHOICES)
        one_student_form = AddOneStudentForm(request.POST, request.FILES, CLASS_CHOICES=CLASS_CHOICES)
        if (one_student_form.is_valid() ) :
            if one_student_form.cleaned_data['name']!='':
                classid = Class.objects.filter(id=one_student_form.cleaned_data['classid'])
                student = Student()
                #current_user= request.user
                #studen.user=current_user
                student.classid = classid[0]
                student.name = one_student_form.cleaned_data['name']
               
                student.gender = one_student_form.cleaned_data['gender']
                student.address = one_student_form.cleaned_data['address']
                student.phone = one_student_form.cleaned_data['phone']
                student.dob = one_student_form.cleaned_data['dob']
                student.image =one_student_form.cleaned_data['image']
                student.save()
                #data.save()
                #form.save()
                #return redirect('success')
        if form.is_valid():
            try:
                if request.FILES.get('myfile') :
                    one_student_classid = Class.objects.filter(id=form.cleaned_data['classid'])
                    myfile = request.FILES.get('myfile')  
                    #document = Document()  
                    #document.upload = myfile
                    
                    #document.save()   
                    #print(document.upload.url)
                    #messages.warning(request,document.upload.url)
                    fs = FileSystemStorage()
                    
                    filename = fs.save(myfile.name, myfile)
                    uploaded_file_url = fs.url(filename)
                    excel_file = uploaded_file_url
                    exceldata = pd.read_excel("."+excel_file,names=['stt','name','gender','address','phone','dob'], converters={'phone':str})
                    #exceldata = pd.read_excel(document.upload.url,names=['stt','name','gender','address','phone','dob'], converters={'phone':str})
                    dbframe = exceldata
                    #messages.success(str(exceldata))
                    #print(dbframe)
                    
                    for index,row in dbframe.iterrows():
                        
                        student = Student()
                        student.classid = one_student_classid[0]
                        student.name = row['name']
                        student.gender = row['gender']
                        student.address = row['address']
                        student.phone = row['phone']
                        student.dob = row['dob']
                        student.save()
                        
                
                    messages.success(request,"Lưu thành công")
            except:
                messages.error(request,"Có lỗi xảy ra, xin vui lòng kiểm tra lại file excel. Lưu ý đặt tên file không chứa dấu cách và ký tự đặc biệt, nội dung file đúng với format như ví dụ trong phần hướng dẫn sử dụng!")       
            
    else:
        form = AddStudentForm(CLASS_CHOICES=CLASS_CHOICES)
        one_student_form = AddOneStudentForm(CLASS_CHOICES=CLASS_CHOICES)
    return render(request, 'add_student.html', {'form' : form, 'onestudentform':one_student_form})


def login_form(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user =request.user
            print(current_user.id)
            userprofile=UserProfile.objects.get(user_id=current_user.id)
           
            # Redirect to a success page.
            messages.success(request,'Đăng nhập thành công với tài khoản '+str(current_user))
            return HttpResponseRedirect('/')
        else:
            messages.error(request,"Đăng nhập không thành công !! Sai tên đăng nhập hoặc mật khẩu")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.

    #category = Category.objects.all()
    context = {#'category': category
    'form' : form
     }
    return render(request, 'login_form.html',context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()
            messages.success(request, 'Đăng ký tài khoản thành công!')
            return HttpResponseRedirect('/login/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup')


    form = SignUpForm()
    #category = Category.objects.all()
    context = {#'category': category,
               'form': form,
               }
    return render(request, 'signup_form.html', context)
@login_required (login_url='/login')
def get_classes(request):
    current_user= request.user
    class_list = Class.objects.filter(user=current_user)
    if class_list != None:
        return render(request, 'class_list.html', {'items': class_list, 'title':"Danh sách lớp học"})
    else:
        return render(request, 'class_list.html', {'items': []})

@login_required (login_url='/login')
def get_students(request):
    current_user = request.user
    user_profile = UserProfile.objects.get(user = current_user)
    class_id=request.GET['class_id']
    classid = Class.objects.get(id=class_id)
    student_list = Student.objects.filter(classid=classid)
    good_average = 0
    standard_average = 0
    bad_average = 0
    subjects = Subject.objects.all()
    current_datetime = dt.datetime.now()
    top_student = []
    birthday_in_month = []
    subject_number = len(subjects)
    #print(subject_number)
    for student in student_list:
        
        
        total_average = 0
        #subject_improvement=[]
        #subject_average = []
            #score_array = []
            #count = 0
        average_improvement = 0
        for subject in subjects:
            improvement = 0
            lenght = 0
            average = 0
            total = 0
        
            results = Result.objects.filter(student=student, subject=subject)
            
            for i,result in enumerate(results):
                #score_array.append(result.score)
                total += result.score*result.testid.weight
                lenght += result.testid.weight
                
                '''
                count +=1
                if(count > max):
                    max = count
                    line_labels.append(max)
                
                '''
                if (i>0):
                    improvement += (results[i].score-results[i-1].score)*(results[i].testid.weight/results[i-1].testid.weight)
            if (lenght>0):
                average = total/lenght
            total_average += average
            average_improvement+=improvement
        #subject_average.append(average)
        
        if (subject_number>0):
            total_average /= subject_number
            average_improvement /= subject_number
        if(total_average>= 9):
            good_average += 1
        elif (total_average <9 and average >=7):
            standard_average += 1
        else :
            bad_average +=1
        
        student_map = {}
        student_map['id'] = student.id
        student_map['name'] = student.name
        student_map['gender'] = student.gender
        student_map['score'] = round (total_average,2)
        student_map['improvement'] = round(average_improvement,3)
        top_student.append(student_map)
        month = int(str(student.dob).split('-')[1])
        if (month == current_datetime.month):
            birthday_in_month.append(student)
        #if student.dob = current_date:

    
    #top_student = sorted(top_student, key= lambda d: d['score'])
    top_best_student = sorted(top_student, key= lambda d: d['score'], reverse= True)
    top_worst_student = sorted(top_student, key= lambda d: d['score'])[:5]
    #top_best_student = sorted(top_best_student, key=operator.attrgetter('score'))[:5]
    top_hard_working = sorted(top_student, key= lambda d: d['improvement'], reverse= True)[:5]
    #print(student_list[0].image)
      
    
    context ={
        'items': student_list,
        'title':"Danh sách học sinh",
        'user': current_user,
        'userProfile': user_profile,
        'studentNumber': len(student_list),
        'class': classid,
        'doughnut_data': [good_average,standard_average,bad_average],
        'topBestStudent':top_best_student[:5],
        'topWorstStudent':top_worst_student,
        'topHardWorking':top_hard_working,
        'birthday':birthday_in_month,
        'topStudent':top_best_student
     
    }
    if student_list != None:
        return render(request, 'student_list.html', context=context)
    else:
        return render(request, 'student_list.html', {'items': []})


def show_student_detail(request):
    student_id=request.GET['student_id']
    student = Student.objects.get(id=student_id)
    subjects = Subject.objects.all()
    tests = Test.objects.all()
    labels = []
    average_score = []
    line_dataset =[]
    color = [
        'rgb(255, 99, 132)', #red
        'rgb(54, 162, 235)', #blue
        'rgb(255, 159, 64)', #orange
        'rgb(75, 192, 192)', #green
        'rgb(153, 102, 255)', #purpil
        'rgb(255, 205, 86)', #yellow
        'rgb(231,233,237)', #grey
        'rgb(97, 45, 45)', #brown
        'rgb(139, 245, 86)', #lime
        'rgb(86, 245, 213)', #light green
        'rgb(0, 3, 82)', #ocean
        'rgb(2, 71, 0)', #dark green 
        ] 
    i = 0
    line_labels = []
    max = 0
    good_score = 0
    standard_score = 0
    bad_score = 0
    table_data = []
    #table_subject = []
    table_test = []
    size={}
    for subject in subjects:
        #table_subject.append(subject.name)
        line_dataMap = {}
        table_dataMap = {}
        labels.append(subject.name)
        subject_results = Result.objects.filter(student=student,subject=subject)
        total = 0
        lenght = 0
        average = 0
        score_array = []
        result_array = []
        count = 0
        
        for result in subject_results:
            result_array.append(result)
            score_array.append(result.score)
            total += result.score*result.testid.weight
            lenght += result.testid.weight
            count +=1
            if(count > max):
                max = count
                line_labels.append(max)
            if(result.score >= 9):
                good_score += 1
            if (7<=result.score <9):
                standard_score += 1
            if (result.score <7):
                bad_score +=1
            
            if (not result.testid.id in table_dataMap):
                table_dataMap[result.testid.id] = []
            table_dataMap[result.testid.id].append(result.score)
          
        if (lenght>0):
            average = total/lenght
        average_score.append(average)
        line_dataMap["label"] = subject.name
        line_dataMap["data"] = score_array
        line_dataMap["backgroundColor"]= color[i]
        line_dataMap["borderColor"]=color[i%len(color)]
        line_dataMap["fill"]=0
        if (i>3):
            line_dataMap["hidden"]=1
        
        #line_dataMap["fill"]=json.dumps(False)
        i+=1
        
        #line_dataMap["fill"]="false"
        #line_dataMap[""]
        line_dataset.append(line_dataMap)
        table_dataMap['subject_name'] = subject.name
        result_array = sorted(result_array, key= lambda d: d.testid.id)
        table_dataMap['score'] = result_array 
        table_data.append(table_dataMap)
        for key in table_dataMap:
            if not key in size:
                size[key]= 0
            if size[key] < len(table_dataMap[key]):
                size[key]= len(table_dataMap[key])
    #print(line_dataset)
   # print(table_data)
    #print (size)
    
    for test in tests:
        table_testMap ={}
        if test.id in size:
            table_testMap['size'] = size[test.id]
        table_testMap['test']= test
        table_test.append(table_testMap)
   
    context = {
        'student': student, 
        'title':"Danh sách học sinh",
        'labels':labels,
        'average_score':average_score,
        'dataset':line_dataset,
        'lineLabels':line_labels,
        'doughnut_data': [good_score,standard_score,bad_score],
        'table_data': table_data,
        'table_test': table_test
        }
    
    if student != None:
        return render(request, 'student_detail.html', context=context)
    else:
        return render(request, 'student_list.html', {'student': []})

@login_required (login_url='/login')
def scoring(request):
    current_user= request.user
    CLASS_CHOICES = []
    TEST_CHOICES = []
    SUBJECT_CHOICES = []
    tests = Test.objects.all()
    for atest in tests:
        TEST_CHOICES.append((atest.id,atest.name))
    classes = Class.objects.filter(user=current_user)
    for aclass in classes:
        CLASS_CHOICES.append((aclass.id,aclass.name))
    subjects = Subject.objects.all()
    for subject in subjects:
        SUBJECT_CHOICES.append((subject.id,subject.name))
    
    form = ScoringForm(request.POST, request.FILES,CLASS_CHOICES = CLASS_CHOICES, TEST_CHOICES = TEST_CHOICES, SUBJECT_CHOICES = SUBJECT_CHOICES)  
    
    if request.method == 'POST':
      
        try:
            error = False
            if form.is_valid() and request.FILES['myfile']:
                classid = Class.objects.filter(id=form.cleaned_data['classid'])
                testid = Test.objects.filter(id=form.cleaned_data['test'])
                subject = Subject.objects.filter(id=form.cleaned_data['subject'])
                myfile = request.FILES['myfile']
                students = Student.objects.filter(classid=classid[0])
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                excel_file = uploaded_file_url
                exceldata = pd.read_excel("."+excel_file,names=['stt','name','score'], converters={'score':str})
                #print(type(empexceldata))
                dbframe =exceldata
                #print(dbframe['Họ và tên'])
                
                if len(dbframe)<len(students):
                    messages.warning(request,
                    mark_safe("Nhắc thầy/cô: Có vẻ như một vài học sinh chưa có điểm trong bài kiểm tra này ? <br/>"+ "Sĩ số lớp: " + str(len(students)) 
                    +"<br/>Số học sinh trong danh sách điểm đã nhập: "+ str(len(dbframe)))
                    )
                for index,row in dbframe.iterrows():
                    #print(row['name'])
                    
                    student = Student.objects.filter(name=row['name'],classid=classid[0])
                    #print(len(student))
                    if(len(student) >1):
                        messages.error(request,
                            "Học sinh "+row['name']+ " bị trùng tên, xin vui lòng đặt lại tên để phân biệt, ví dụ " +row['name'] +" A, "+ row['name'] +" B"+ " ...") 
                        error = True
                        pass
                    if(len(student) == 0):
                        messages.error(request,
                        "Học sinh "+row['name']+ " chưa có trong danh sách lớp")   
                        error = True
                    result = Result()
                    result.student = student[0]
                    result.subject = subject[0]
                    result.testid = testid[0]
                    result.score = row['score']
                    #print(result.score)
                    if(error is False):
                        result.save()
                if(error is False):        
                    messages.success(request,"Lưu thành công")
            else:
                form = ScoringForm()
        except Exception as identifier:            
            print(identifier)
            messages.error(request,
            "Có lỗi xảy ra, xin vui lòng kiểm tra lại file excel. Lưu ý đặt tên file không chứa dấu cách và ký tự đặc biệt, nội dung file đúng với format như ví dụ trong phần hướng dẫn sử dụng!")       

   
    return render(request, 'scoring.html', {'form' : form})
def logout_func(request):
    logout(request)
    messages.success(request,'Đã đăng xuất')
    return HttpResponseRedirect('/login')

def edit_student(request):
    context ={}
    current_user = request.user
    CLASS_CHOICES = []
    classes = Class.objects.filter(user=current_user)
    for aclass in classes:
        CLASS_CHOICES.append((aclass.id,aclass.name))  
    # fetch the object related to passed id
    student_id=request.GET['student_id']
    student = Student.objects.filter(id=student_id)
    # pass the object as instance in form
    form = UpdateStudentForm(request.POST or None, instance = student[0],CLASS_CHOICES = CLASS_CHOICES, initial={'classid':student[0].classid.id})
 
    # save the data from the form and
    # redirect to detail_view
    if request.method == "POST":
        if form.is_valid():
            classid = Class.objects.filter(id=form.cleaned_data['classid'])
            student = Student.objects.get(id=student_id)
            student.classid = classid[0]
            student.name = form.cleaned_data['name']
            if len(request.FILES) != 0:
                
                #if not student.image :
                   # os.remove(student.image.path)
                student.image = request.FILES['image']
                print(student.image)
            student.gender = form.cleaned_data['gender']
            student.address = form.cleaned_data['address']
            student.phone = form.cleaned_data['phone']
            student.dob = form.cleaned_data['dob']
           
            student.save()
        return HttpResponseRedirect('/studentdetail?student_id='+student_id)
        
    # add form dictionary to context
    context["form"] = form

    return render(request, "update_student.html", context)

def setting(request):
    return render(request,"settings.html")

def manage_class(request):
    current_user = request.user
    class_list = Class.objects.filter(user = current_user)
    context ={
        'classes' : class_list,

    }
    return render(request, "manage_class.html", context)

def add_class(request):
    current_user = request.user
     
    if request.method == 'POST':
        form = AddClassForm(request.POST)
       
        if (form.is_valid() ) :
            classid = Class()
            classid.user =current_user
            classid.name = form.cleaned_data['name']
            classid.save()
            return HttpResponseRedirect('/classes')
    else:
        form = AddClassForm()
    context = {'form' : form, 'title': 'Thêm lớp học'}
    return render(request, 'add_object.html', context )

def edit_class(request):
    context ={}
 
    # fetch the object related to passed id
    class_id=request.GET['class_id']
    classid = Class.objects.get(id=class_id)
 
    # pass the object as instance in form
    form = UpdateClassForm(request.POST or None, instance = classid)
 
    # save the data from the form and
    # redirect to detail_view
    if request.method == "POST":
        if form.is_valid():
            
            classid = Class.objects.get(id=class_id)
            classid.name = form.cleaned_data['name']
            classid.save()
        return HttpResponseRedirect('/classes')
        
    # add form dictionary to context
    context["form"] = form

    return render(request, "update_student.html", context)

def delete_class(request):

    # fetch the object related to passed id
    class_id=request.GET['class_id']
    Class.objects.filter(id=class_id).delete()

    return HttpResponseRedirect('/classes')

def manage_subject(request):
    current_user = request.user
    subject_list = Subject.objects.all()
    context ={
        'subjects' : subject_list,

    }
    return render(request, "manage_subject.html", context)

def add_subject(request):
    current_user = request.user
     
    if request.method == 'POST':
        form = AddSubjectForm(request.POST)
       
        if (form.is_valid() ) :
            subject = Subject()
            subject.user =current_user
            subject.name = form.cleaned_data['name']
            subject.save()
            return HttpResponseRedirect('/managesubject')
    else:
        form = AddSubjectForm()
    context = {'form' : form, 'title': 'Thêm môn học'}    
    return render(request, 'add_object.html', context)

def edit_subject(request):
    context ={}
 
    # fetch the object related to passed id
    subject_id=request.GET['subject_id']
    subject = Subject.objects.get(id=subject_id)
 
    # pass the object as instance in form
    form = UpdateSubjectForm(request.POST or None, instance = subject)
 
    # save the data from the form and
    # redirect to detail_view
    if request.method == "POST":
        if form.is_valid():
            
            subject = Subject.objects.get(id=subject_id)
            subject.name = form.cleaned_data['name']
            subject.save()
        return HttpResponseRedirect('/managesubject')
        
    # add form dictionary to context
    context["form"] = form

    return render(request, "update_student.html", context)

def delete_subject(request):

    # fetch the object related to passed id
    subject_id=request.GET['subject_id']
    Subject.objects.filter(id=subject_id).delete()

    return HttpResponseRedirect('/managesubject')



def manage_test(request):
    current_user = request.user
    test_list = Test.objects.all()
    context ={
        'tests' : test_list,

    }
    return render(request, "manage_test.html", context)

def add_test(request):
    current_user = request.user
     
    if request.method == 'POST':
        form = AddTestForm(request.POST)
       
        if (form.is_valid() ) :
            test = Test()
            test.user =current_user
            test.name = form.cleaned_data['name']
            test.weight = form.cleaned_data['weight']
            test.save()
            return HttpResponseRedirect('/managetest')
    else:
        form = AddTestForm()
    context = {'form' : form, 'title': 'Thêm lớp học'}   
    return render(request, 'add_object.html', context)

def edit_test(request):
    context ={}
 
    # fetch the object related to passed id
    test_id=request.GET['test_id']
    test = Test.objects.get(id=test_id)
 
    # pass the object as instance in form
    form = UpdateTestForm(request.POST or None, instance = test)
 
    # save the data from the form and
    # redirect to detail_view
    if request.method == "POST":
        if form.is_valid():
            
            test = Test.objects.get(id=test_id)
            test.name = form.cleaned_data['name']
            test.weight = form.cleaned_data['weight']
            test.save()
        return HttpResponseRedirect('/managetest')
        
    # add form dictionary to context
    context["form"] = form

    return render(request, "update_student.html", context)

def delete_test(request):

    # fetch the object related to passed id
    test_id=request.GET['test_id']
    Test.objects.filter(id=test_id).delete()

    return HttpResponseRedirect('/managetest')