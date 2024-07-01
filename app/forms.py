
from django import forms
from .models import Task, User


class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-multiselect block w-full mt-1 rounded-md shadow-sm border-gray-300 focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 sm:text-sm'
        })
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'category', 'assigned_to']
        widgets = {
            'due_date': forms.DateInput(attrs={
                'class': 'form-input block w-full mt-1 rounded-md border border-gray-300 p-2 shadow-sm focus:outline-none focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 sm:text-sm',
                'placeholder': 'YYYY-MM-DD'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-input block w-full mt-1 rounded-md border border-gray-300 p-2 shadow-sm focus:outline-none focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 sm:text-sm'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea block w-full mt-1 rounded-md border border-gray-300 p-2 shadow-sm focus:outline-none focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 sm:text-sm'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select block w-full mt-1 rounded-md border border-gray-300 p-2 shadow-sm focus:outline-none focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 sm:text-sm'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select block w-full mt-1 rounded-md border border-gray-300 p-2 shadow-sm focus:outline-none focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 sm:text-sm'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-input block w-full mt-1 rounded-md border border-gray-300 p-2 shadow-sm focus:outline-none focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 sm:text-sm'
            }),
        }



class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-input block w-full mt-1 rounded-md border border-gray-300 p-2 shadow-sm focus:outline-none focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 sm:text-sm'
    }))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={
        'class': 'form-input block w-full mt-1 rounded-md border border-gray-300 p-2 shadow-sm focus:outline-none focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 sm:text-sm'
    }))

    class Meta:
        model = User
        fields = ('username', 'image')

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input block w-full mt-1 rounded-md border border-gray-300 p-2 shadow-sm focus:outline-none focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 sm:text-sm'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-input block w-full mt-1 rounded-md border border-gray-300 p-2 shadow-sm focus:outline-none focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 sm:text-sm'
            }),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    
