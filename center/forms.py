from django import forms
from django.forms.fields import ImageField
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

ADDRESS_CHOICES = ['Thành phố Hà Nội', 'Tỉnh Hà Giang', 'Tỉnh Cao Bằng', 'Tỉnh Bắc Kạn']

GENDER_CHOICES = [
    ('Nam','Nam',), 
    ('Nữ','Nữ',), 
    ('Khác','Giới tính khác')]
class AddStudentForm(forms.ModelForm):
    CLASS_CHOICES = []
    #classes = Class.objects.all()
    #for aclass in classes:
    #    CLASS_CHOICES.append((aclass.id,aclass.name))
    classid = forms.ChoiceField(
        label="Tên lớp",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=CLASS_CHOICES,
    )
    name = forms.CharField( required=False, max_length=255, label="Tên", widget=forms.TextInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'}))
    gender = forms.ChoiceField(
        label="Giới tính",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=GENDER_CHOICES,
    )
    image = forms.ImageField(  required=False, label="Ảnh chân dung",
        widget=forms.FileInput(attrs={'style': 'width:100%;','class': 'form-control'})
    )
    
    address = forms.CharField( required=False,max_length=2550, label="Địa chỉ", widget=forms.TextInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'}))

    phone = forms.CharField( required=False, max_length=255, label="Số điện thoại", widget=forms.TextInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'}))
    description = forms.CharField(required=False, max_length=2550,widget=forms.Textarea(attrs={'class': 'form-control'}), label="Mô tả")
    dob = forms.DateTimeField(
        required=False, 
        label="Ngày sinh",
        help_text= "Ví dụ: 1/1/1999",
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input','style': 'width:100%;','data-target': '#datetimepicker1'})
    )
    class Meta:
        model = Student
      
        fields = ['name', 'gender', 'image', 'address', 'phone', 'description']
class AddOneStudentForm(forms.Form):
    CLASS_CHOICES = []
    #classes = Class.objects.all()
    #for aclass in classes:
    #    CLASS_CHOICES.append((aclass.id,aclass.name))
    classid = forms.ChoiceField(
        label="Tên lớp",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=CLASS_CHOICES,
    )
class UpdateStudentForm(forms.ModelForm):
    CLASS_CHOICES = []
    #classes = Class.objects.all()
    #for aclass in classes:
    #    CLASS_CHOICES.append((aclass.id,aclass.name))
    classid = forms.ChoiceField(
        label="Tên lớp",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=CLASS_CHOICES,
    )
    name = forms.CharField( required=False, max_length=255, label="Tên", widget=forms.TextInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'}))
    gender = forms.ChoiceField(
        label="Giới tính",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=GENDER_CHOICES,
    )
    image = forms.ImageField(  required=False, label="Ảnh chân dung",
        widget=forms.FileInput(attrs={'style': 'width:100%;','class': 'form-control','name':'image'})
    )
    
    address = forms.CharField( required=False,max_length=2550, label="Địa chỉ", widget=forms.TextInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'}))

    phone = forms.CharField( required=False, max_length=255, label="Số điện thoại", widget=forms.TextInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'}))
    description = forms.CharField(required=False, max_length=2550,widget=forms.Textarea(attrs={'class': 'form-control'}), label="Mô tả")
    dob = forms.DateTimeField(
        required=False, 
        label="Ngày sinh",
        help_text= "Ví dụ: 1/1/1999",
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input','style': 'width:100%;','data-target': '#datetimepicker1'})
    )
    class Meta:
        model = Student
      
        fields = ['name', 'gender', 'image', 'address', 'phone', 'description','dob']

class ScoringForm(forms.Form):
    CLASS_CHOICES = []
    TEST_CHOICES = []
    SUBJECT_CHOICES = []
    #tests = Test.objects.all()
    #for atest in tests:
    #    TEST_CHOICES.append((atest.id,atest.name))
    #classes = Class.objects.all()
    #for aclass in classes:
    #    CLASS_CHOICES.append((aclass.id,aclass.name))
    #subjects = Subject.objects.all()
    #for subject in subjects:
     #   SUBJECT_CHOICES.append((subject.id,subject.name))
    classid = forms.ChoiceField(
        label="Tên lớp",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=CLASS_CHOICES,
    )
    test = forms.ChoiceField(
        label="Bài kiểm tra",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=TEST_CHOICES,
    )
    subject = forms.ChoiceField(
        label="Môn học",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=SUBJECT_CHOICES,
    )
    
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                            
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                             
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                            
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                             
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
       
         widget=forms.TextInput(
            attrs={
                              
                "class": "form-control"
            }
        ))
    first_name = forms.CharField(
       
         widget=forms.TextInput(
            attrs={              
                "class": "form-control"
            }
        ))
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={ 
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={          
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name',  'password1', 'password2' )