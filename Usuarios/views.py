from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def registro(request):
    """Registrar un nuevo usuario"""
    if request.method != 'POST':
        # Display blank registration form.
        form= UserCreationForm()
    else:
        # Form para completar el proceso.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Registrar el usuario y redirigir a la página Home.
            login(request, new_user)
            return redirect('Cargas:index')
    # Muestra un form en blanco o inválido.
    context = {'form': form}
    return render(request, 'registration/registro.html', context)