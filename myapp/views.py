from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages

from .models import *
from django.db.models import Q

def base(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #create a new registration object and avoid saving it yet
            new_user = user_form.save(commit=False)
            #reset the choosen password
            new_user.set_password(user_form.cleaned_data['password'])
            #save the new registration
            new_user.save()
            return render(request, 'registration/register_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html',{'user_form':user_form})

def profile(request):
    return render(request, 'profile/profile.html')



@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        user_form = EditProfileForm(instance=request.user)
    
    return render(request, 'profile/edit_profile.html', {'user_form': user_form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Your account was successfully deleted.')
        return redirect('base')  # Redirect to the homepage or another page after deletion

    return render(request, 'registration/delete_account.html')

#CRUD operations start here
@login_required
def dashboard(request):
    consumers = Consumer.objects.all()
    search_query = ""
    
    if request.method == "POST": 
        if "create" in request.POST:
            name = request.POST.get("name")
            email = request.POST.get("email")
            image = request.FILES.get("image")  # Handle the image file
            content = request.POST.get("content")

            Consumer.objects.create(
                name=name,
                email=email,
                image=image,
                content=content
            )
            messages.success(request, "Consumer added successfully")
    
        elif "update" in request.POST:
            id = request.POST.get("id")
            name = request.POST.get("name")
            email = request.POST.get("email")
            image = request.FILES.get("image")  # Handle the image file
            content = request.POST.get("content")

            consumer = get_object_or_404(Consumer, id=id)
            consumer.name = name
            consumer.email = email
            consumer.image = image
            consumer.content = content
            consumer.save()
            messages.success(request, "Consumer updated successfully")
    
        elif "delete" in request.POST:
            id = request.POST.get("id")
            Consumer.objects.get(id=id).delete()
            messages.success(request, "Consumer deleted successfully")
        
        elif "search" in request.POST:
            search_query = request.POST.get("query")
            consumers = Consumer.objects.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query))

    context = {"consumers": consumers, "search_query": search_query}
    return render(request, "dashboard/dashboard.html", context=context)

# CRUD operations end here

# Contact start
@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us!")
            return redirect('dashboard')  # Redirect to the same page to show the modal
    else:
        form = ContactForm()

    return render(request, 'contact/contact_form.html', {'form': form})

# contact end

# review start
def add_review(request, consumer_id):
    consumer = get_object_or_404(Consumer, id=consumer_id)
    consumer_name = consumer.name

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Assuming you have a Review model with fields 'comment' and 'rating'
            review = form.save(commit=False)
            review.consumer = consumer
            review.save()
            # You may want to add a success message here
            return redirect('dashboard')  # Redirect to the dashboard or any other page
    else:
        form = ReviewForm()

    return render(request, 'dashboard/review.html', {'consumer_id': consumer_id, 'consumer_name': consumer_name, 'form': form})
# review end

# views.py


def view_reviews(request, consumer_id):
    consumer = get_object_or_404(Consumer, id=consumer_id)
    reviews = Review.objects.filter(consumer=consumer)

    return render(request, 'dashboard/view_reviews.html', {'consumer': consumer, 'reviews': reviews})

#notification

@login_required
def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/user_notifications.html', {'notifications': notifications})
