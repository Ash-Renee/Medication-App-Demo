import bcrypt
from django.shortcuts import render, redirect
from django.contrib import messages


from .models import Medication, User, Rx

def login(request):
    return render(request, 'access.html')

def login_check(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/access")

    else:
        user_list = User.objects.filter(email = request.POST['email'])
        user = user_list[0]
        request.session['uuid'] = user.id
        return redirect('/dashboard')

def logout(request):
    del request.session['uuid']
    return redirect("/")

def registration(request):
    return render(request, 'register.html')

def register(request):
    print(request.POST)
    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect("/registration")
    
    else:
        pills = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            preferred_name = request.POST["preferred_name"],
            pronouns = request.POST["pronouns"],
            email = request.POST["email"],
            password = pills
        )
        request.session['uuid'] = user.id
        return redirect('/')

def guest_view(request):
    context = {
        'med': Medication.objects.all(),
    }
    return render(request, "guest view.html", context)

def dashboard(request):
    context = {
        'user' : User.objects.get(id = request.session['uuid']),
        'med' : Medication.objects.all()
    }
    return render(request, "dashboard.html", context)

def add_med(request):
    return render(request, "add_medication.html")

def create_med(request):
    errors = Medication.objects.med_validator(request.POST)
    medication_name = Medication.objects.filter(name = request.POST["name"])
    if len(medication_name) > 0:
        errors['name'] = "Medication already exists."
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/medication/new")
    else:
        med = Medication.objects.create(
            doctor= request.POST['doctor'],
            name = request.POST['name'],
            common_name = request.POST['common_name'],
            dose = request.POST['dose'],
            intake_method = request.POST['intake_method'],
            description = request.POST['description'],
            frequency = request.POST['frequency'],
            starting_count = request.POST['starting_count'],
            end_date = request.POST['end_date'],
            notes = request.POST['notes'],
        )
        print(request.POST)
        return redirect('/dashboard')

def display_medication(request, medication_id):
    context = {
        "meds": Medication.objects.get(id=medication_id)
    }
    return render(request, 'medication.html', context)

def cancel(request):
    if "uuid" in request.session:
        return redirect('/dashboard')
    else:
        return redirect('/')

def edit_medication(request, medication_id):
    context = {
        "meds": Medication.objects.get(id=medication_id),
    }
    return render(request, "edit_medication.html", context)

def update_medication(request, medication_id):
    errors = Medication.objects.med_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/medication/{medication_id}/edit")
    else:
        edited_medication = Medication.objects.get(id=medication_id)
        if request.POST['doctor']:
            edited_medication.doctor = request.POST['doctor']
        if request.POST['name']:
            edited_medication.name = request.POST['name']
        if request.POST['common_name']:
            edited_medication.common_name = request.POST['common_name']
        if request.POST['dose']:
            edited_medication.dose = request.POST['dose']
        if request.POST['intake_method']:
            edited_medication.intake_method = request.POST['intake_method']
        if request.POST['description']:
            edited_medication.description = request.POST['description']
        if request.POST['frequency']:
            edited_medication.frequency = request.POST['frequency']
        if request.POST['starting_count']:
            edited_medication.starting_count = request.POST['starting_count']
        if request.POST['end_date']:
            edited_medication.end_date = request.POST['end_date']
        if request.POST['notes']:
            edited_medication.notes = request.POST['notes']

        edited_medication.save()
        return redirect('/dashboard')

def delete_medication(request, medication_id):
    context = {
        "meds" : Medication.objects.get(id=medication_id),
    }
    Medication.objects.get(id=medication_id).delete()
    return redirect('/dashboard', context)

def register(request):
    print(request.POST)
    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect("/")

    else:
        pills = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            preferred_name= request.POST["preferred_name"],
            password = pills
        )
        request.session['uuid'] = user.id ##unique user id is uuid, but is not mandatory to be there, can use other variables
    return redirect('/dashboard')

def take_med(request):
    if 'click_count' in request.session:
        request.session ['click_count'] -= 1
    else:
        request.session ['click_count'] = 0
    return redirect ('/dashboard.html')

def undo_take(request):
    if 'click_count' in request.session:
        request.session ['click_count'] += 1
    else:
        request.session ['click_count'] = 0
    return redirect( '/dashboard.html')