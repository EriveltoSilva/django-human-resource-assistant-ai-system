from django import forms
from apps.users.models import Area
from django.contrib.auth.models import User
from . import utils 

class LoginForms(forms.Form):
    username = forms.CharField(
        label='Username',
        required=True,
        max_length=255,  
        widget=forms.TextInput(
            attrs={
                "placeholder":"Insira o seu username",
                "class":"form-control form-control-lg",
                "id":"usernameID"
            }
        )      
    )
  
    password = forms.CharField(
        label='Senha',
        required=True,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Insira a sua senha",
                "class":"form-control form-control-lg",
                "id":"passwordID"
            }
        )
    )

class RegisterForms(forms.Form):
    first_name = forms.CharField(
        label="Primeiro Nome",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder":"Insira o seu nome",
            "fatherClass":"form-group", 
            "class":"form-control form-control-lg"
        }),
        error_messages={
            "required":"O campo primiero nome não pode estar vazio!" 
        }
        # help_text={
        #     "Seu Primeiro nome"
        # }
    )

    last_name = forms.CharField(
        label="Sobrenome",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder":"Insira o seu sobrenome","fatherClass":"form-group", "class":"form-control form-control-lg"})
    )
    
    gender = forms.ChoiceField(
        label="Gênero",
        choices=utils.GENDER,
        widget=forms.Select(attrs={"fatherClass":"form-group","class": "form-control"})
    )

    birthday = forms.DateField(
        label="Data de Nascimento",
        required=True,
        widget=forms.DateInput(attrs={'type':'date',"placeholder":"Sua data de nascimento","fatherClass":"form-group", "class":"form-control"})
    )

    hiring_date = forms.DateField(
        label="Data de Inicio na Empresa",
        required=True,
        widget=forms.DateInput(attrs={'type':'date',"placeholder":"Data de entrada na empresa","fatherClass":"form-group", "class":"form-control"})
    )

    area = forms.ModelChoiceField(
        label="Área",
        required=True,
        queryset=Area.objects.all(),
        widget=forms.Select(attrs={"fatherClass":"form-group","class": "form-control"})
    )

    username = forms.CharField(
        label="Username",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder":"Insira o seu username","fatherClass":"form-group", "class":"form-control"})
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={"placeholder":"Insira o seu email","fatherClass":"form-group", "class":"form-control"})
    )
    

    

    password1 = forms.CharField(
        label='Senha',
        required=True,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Insira a sua senha",
                "fatherClass":"form-group",
                "class":"form-control"
            }
        ),
        # help_text="A senha deve conter pelo menos 8 digitos"

    )

    password2 = forms.CharField(
        label='Senha de Confirmação',
        required=True,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Insira a sua senha novamente",
                "fatherClass":"form-group",
                "class":"form-control"
            }
        )
    )

    
    is_admin = forms.BooleanField(
        label="Gestor",
        required=False,
        widget=forms.CheckboxInput(attrs={"fatherClass":"form-check", "class": "form-check-input"})
    )



    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.strip()
            if " " in username:
                raise forms.ValidationError("O Username não pode conter espaços em branco!")
            else:
                return username
    
    def clean_password2(self):
        TAM_PASSWORD = 8
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("As senhas introduzidas não concidem!")
        elif len(password2)<TAM_PASSWORD:
            raise forms.ValidationError(f"A password não pode ter menos de {TAM_PASSWORD} caracter!")
            
        return password1


class EditUserForm(forms.Form):
    class Meta:
        model  = User
        fields = ('first_name','last_name','username','email','password')

        firstName = forms.CharField(
            label="Primeiro Nome",
            required=True,
            max_length=100,
            widget=forms.TextInput(attrs={"placeholder":"Insira o seu nome", "class":"form-control"})
        )

        lastName = forms.CharField(
            label="Sobrenome",
            required=True,
            max_length=100,
            widget=forms.TextInput(attrs={"placeholder":"Insira o seu sobrenome", "class":"form-control"})
        )
        username = forms.CharField(
            label="Username",
            disabled=True,
            max_length=100,
            widget=forms.TextInput(attrs={"placeholder":"Insira o seu username", "class":"form-control"})
        )

        email = forms.EmailField(
            label="Email",
            required=True,
            disabled=True,
            max_length=100,
            widget=forms.EmailInput(attrs={"placeholder":"Insira o seu email", "class":"form-control"})
        )


        password2 = forms.CharField(
            label='Senha',
            required=True,
            max_length=32,
            widget=forms.PasswordInput(
                attrs={
                    "placeholder":"Insira a sua senha",
                    "class":"form-control"
                }
            )
        )


        area = forms.CharField(
            label="Função",
            required=True,
            max_length=100,
            widget=forms.TextInput(attrs={"placeholder":"Insira a sua função", "class":"form-control"})
        )


        def clean_username(self):
            username = self.cleaned_data.get('username')
            if username:
                username = username.strip() # retira os espaços no inicio e fim da string
                if " " in username:
                    raise forms.ValidationError("O Username não pode conter espaços em branco!")
                else:
                    return username
        
        def clean_password2(self):
            TAM_PASSWORD = 8
            password2 = self.cleaned_data.get('password2')
            if len(password2)<TAM_PASSWORD:
                raise forms.ValidationError(f"A password não pode ter menos de {TAM_PASSWORD} caracter!")
                
            return password2
