from django.shortcuts import render, redirect
from crud.forms import StudentForm
from crud.models import Student
from django.contrib.auth.decorators import login_required


def create(request):
    form= StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            mem = Student()
            FirstName = form.cleaned_data['FirstName']
            mem.FirstName = FirstName
            mem.Lastname = form.cleaned_data['Lastname']
            mem.Address = form.cleaned_data['Address']
            mem.Date_Of_Birth = form.cleaned_data['Date_Of_Birth']
            mem.Relationship_Status = form.cleaned_data['Relationship_Status']
            mem.Gender = form.cleaned_data['Gender']
            form.save()
        return redirect(index)
    return render(request, 'crud/create.html', {'form': form})

@login_required(login_url='/sites/signin')
def index(request):
    resultSet = Student.objects.all()
    return render(request, 'crud/index.html',{'data': resultSet})

def update(request, id):
        data = Student.objects.get(id=id)
        form = StudentForm(request.POST, instance=data)
        if request.method == 'POST':
            form = StudentForm(request.POST)
            if form.is_valid():
                mem = Student()
                FirstName = form.cleaned_data['FirstName']
                mem.FirstName = FirstName
                mem.Lastname = form.cleaned_data['Lastname']
                mem.Address = form.cleaned_data['Address']
                mem.Date_Of_Birth = form.cleaned_data['Date_Of_Birth']
                mem.Relationship_Status = form.cleaned_data['Status']
                mem.Gender = form.cleaned_data['Gender']
                form.save()
                return redirect(index)
        return render(request, 'crud/update.html', {'form': form})


def delete(request, id):
    data = Student.objects.get(id=id)
    data.delete()
    return redirect(index)


def views(request, id):
    data = Student.objects.get(id=id)
    return render(request, 'crud/view.html', {'data': data})
