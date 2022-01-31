from django import forms
from django.forms.fields import ImageField
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

ADDRESS_CHOICES = ['Thành phố Hà Nội', 'Tỉnh Hà Giang', 'Tỉnh Cao Bằng', 'Tỉnh Bắc Kạn']

GENDER_CHOICES = [
    ('Nam','Nam',), 
    ('Nữ','Nữ',), 
    ('Khác','Giới tính khác')]
class AddOneStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        CLASS_CHOICES = kwargs.pop('CLASS_CHOICES', None)
        super(AddOneStudentForm, self).__init__(*args, **kwargs)
        self.fields['classid']=forms.ChoiceField(
            label="Tên lớp",
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=CLASS_CHOICES,
        )
    classid =forms.ChoiceField() 
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
class AddStudentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        CLASS_CHOICES = kwargs.pop('CLASS_CHOICES', None)
        super(AddStudentForm, self).__init__(*args, **kwargs)
        self.fields['classid']=forms.ChoiceField(
            label="Tên lớp",
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=CLASS_CHOICES,
        )
    classid =forms.ChoiceField()   
    
class AddClassForm(forms.Form):
    name = forms.CharField( required=True, max_length=255, label="Tên lớp", widget=forms.TextInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'}))          

class AddSubjectForm(forms.Form):
    name = forms.CharField( required=True, max_length=255, label="Tên môn học", widget=forms.TextInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'})) 

class AddTestForm(forms.Form):
    name = forms.CharField( required=True, max_length=255, label="Tên loại bài kiểm tra", widget=forms.TextInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'})) 
    weight = forms.IntegerField(required=True, label="Trọng số",widget=forms.NumberInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'}))

class UpdateStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        CLASS_CHOICES = kwargs.pop('CLASS_CHOICES', None)
        super(UpdateStudentForm, self).__init__(*args, **kwargs)
        self.fields['classid']=forms.ChoiceField(
            label="Tên lớp",
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=CLASS_CHOICES,
        )
    classid =forms.ChoiceField() 
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

class UpdateClassForm(forms.ModelForm):
    
    name = forms.CharField( required=False, max_length=255, label="Tên lớp", widget=forms.TextInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'}))
    

    class Meta:
        model = Class
      
        fields = ['name']


class UpdateSubjectForm(forms.ModelForm):
    
    name = forms.CharField( required=False, max_length=255, label="Tên môn học", widget=forms.TextInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'}))
    class Meta:
        model = Subject
      
        fields = ['name']

class UpdateTestForm(forms.ModelForm):
    
    name = forms.CharField( required=False, max_length=255, label="Tên môn học", widget=forms.TextInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'}))
    weight = forms.IntegerField(required=True, label="Trọng số",widget=forms.NumberInput(attrs={ 'style': 'width: 100%;', 'class': 'form-control'}))
    class Meta:
        model = Test
      
        fields = ['name', 'weight']

class ScoringForm(forms.Form):
    def __init__(self, *args, **kwargs):
        CLASS_CHOICES = kwargs.pop('CLASS_CHOICES', None)
 
        TEST_CHOICES = kwargs.pop('TEST_CHOICES', None)
        
        SUBJECT_CHOICES = kwargs.pop('SUBJECT_CHOICES', None)
        super(ScoringForm, self).__init__(*args, **kwargs)
        self.fields['classid']=forms.ChoiceField(
            label="Tên lớp",
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=CLASS_CHOICES,
        )
        self.fields['subject']=forms.ChoiceField(
            label="Môn học",
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=SUBJECT_CHOICES,
        )
        self.fields['test']=forms.ChoiceField(
            label="Bài kiểm tra",
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=TEST_CHOICES,
        )
  

    classid =forms.ChoiceField() 
    test = forms.ChoiceField()
    subject = forms.ChoiceField()
    
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