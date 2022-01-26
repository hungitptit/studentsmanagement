from os import name
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, request
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.core.files.storage import FileSystemStorage
import datetime as dt
#Simport os
import cloudinary


# Create your views here.
@login_required(login_url='/login') # Check login
def add_student(request):
  
    if request.method == 'POST':
        form = AddStudentForm(request.POST, request.FILES)
        one_student_form = AddOneStudentForm(request.POST, request.FILES)
        if (form.is_valid() ) :
            if form.cleaned_data['name']!='':
                classid = Class.objects.filter(id=form.cleaned_data['classid'])
                student = Student()
                #current_user= request.user
                #studen.user=current_user
                student.classid = classid[0]
                student.name = form.cleaned_data['name']
               
                student.gender = form.cleaned_data['gender']
                student.address = form.cleaned_data['address']
                student.phone = form.cleaned_data['phone']
                student.dob = form.cleaned_data['dob']
                student.image =form.cleaned_data['image']
                student.save()
                #data.save()
                #form.save()
                #return redirect('success')
        if one_student_form.is_valid():
            
            try:
                if request.FILES['myfile']:
                    one_student_classid = Class.objects.filter(id=one_student_form.cleaned_data['classid'])
                    myfile = request.FILES['myfile']   
                    document = Document()  
                    document.upload = myfile
                    
                    document.save()   
                    print(document.upload.url)
                    #fs = FileSystemStorage()
                    #filename = fs.save(myfile.name, myfile)
                    #uploaded_file_url = fs.url(filename)
                    #excel_file = uploaded_file_url
                    #exceldata = pd.read_excel("."+excel_file,names=['stt','name','gender','address','phone','dob'], converters={'phone':str})
                    exceldata = pd.read_excel(document.upload.url,names=['stt','name','gender','address','phone','dob'], converters={'phone':str})
                    dbframe = exceldata
                   
                    print(dbframe)
                    for index,row in dbframe.iterrows():
                        messages.success(request,row['name'])
                        student = Student()
                        student.classid = one_student_classid[0]
                        student.name = row['name']
                        student.gender = row['gender']
                        student.address = row['address']
                        student.phone = row['phone']
                        student.dob = row['dob']
                        student.save()
            except Exception as identifier:            
                print(identifier)
    else:
        form = AddStudentForm()
        one_student_form = AddOneStudentForm()
    return render(request, 'add_student.html', {'form' : form, 'onestudentform':one_student_form})
  
def success(request):
    return HttpResponse('successfully uploaded')

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
            messages.warning(request,"Đăng nhập không thành công !! Sai tên đăng nhập hoặc mật khẩu")
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
    class_id=request.GET['class_id']
    classid = Class.objects.filter(id=class_id)
    student_list = Student.objects.filter(classid=classid[0])
    #print(student_list[0].image)
    if student_list != None:
        return render(request, 'student_list.html', {'items': student_list, 'title':"Danh sách học sinh"})
    else:
        return render(request, 'student_list.html', {'items': []})


def show_student_detail(request):
    student_id=request.GET['student_id']
    student = Student.objects.filter(id=student_id)
    if student != None:
        return render(request, 'student_detail.html', {'student': student[0], 'title':"Danh sách học sinh"})
    else:
        return render(request, 'student_list.html', {'student': []})

@login_required (login_url='/login')
def scoring(request):
    form = ScoringForm(request.POST, request.FILES)  
    if request.method == 'POST':
        
      
        try:
            if form.is_valid() and request.FILES['myfile']:
                classid = Class.objects.filter(id=form.cleaned_data['classid'])
                testid = Test.objects.filter(id=form.cleaned_data['test'])
                subject = Subject.objects.filter(id=form.cleaned_data['subject'])
                myfile = request.FILES['myfile']
                
                document = Document()  
                document.upload = myfile
                    
                document.save()   
                #print(document.upload.url)
           
                exceldata = pd.read_excel(document.upload.url,names=['stt','name','score'])
                dbframe = exceldata                
                #print(type(empexceldata))
                dbframe =exceldata
                #print(dbframe['Họ và tên'])
                
            
                for index,row in dbframe.iterrows():
                    #print(row['score'])
                    
                    student = Student.objects.filter(name=row['name'],classid=classid[0])
                    print(len(student))
                    result = Result()
                    result.student = student[0]
                    result.subject = subject[0]
                    result.testid = testid[0]
                    result.score = row['score']
                    #print(result.score)
                    result.save()
            else:
                form = ScoringForm()
        except Exception as identifier:            
            print(identifier)
   
    return render(request, 'scoring.html', {'form' : form})
def logout_func(request):
    logout(request)
    messages.success(request,'Đã đăng xuất')
    return HttpResponseRedirect('/login')

def edit_student(request):
    context ={}
 
    # fetch the object related to passed id
    student_id=request.GET['student_id']
    student = Student.objects.filter(id=student_id)
 
    # pass the object as instance in form
    form = UpdateStudentForm(request.POST or None, instance = student[0])
 
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