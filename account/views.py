from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket  # ✅ import Ticket for latest-ticket redirect

# Customer login/logout
def customer_login(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_staff:
                error = "Admin cannot login here."
            else:
                login(request, user)
                return redirect('account:home')
        else:
            error = "Invalid username or password."
    return render(request, 'account/customer_login.html', {'error': error})


def customer_logout(request):
    logout(request)
    return redirect('account:customer_login')


# Admin login/logout
def admin_login(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if not user.is_staff:
                error = "This is not an admin account."
            else:
                login(request, user)

                # ✅ Redirect to ticket list page
                # return redirect('admin_ticket_list')

                # OR ✅ Redirect to latest ticket’s chatroom automatically:
                latest_ticket = Ticket.objects.last()
                if latest_ticket:
                    return redirect('chatroom', ticket_id=latest_ticket.id)
                else:
                    return redirect('admin_ticket_list')  # fallback if no tickets
        else:
            error = "Invalid username or password."
    return render(request, 'account/admin_login.html', {'error': error})


def admin_logout(request):
    logout(request)
    return redirect('account:admin_login')


# Home page
@login_required
def home(request):
    return render(request, 'ticket_chat.html', {'user': request.user})
