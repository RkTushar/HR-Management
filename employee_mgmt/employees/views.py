from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm
from django.http import HttpResponse
from django.contrib import messages

import csv

# Homepage view with optional search query
def home(request):
    query = request.GET.get('search', '')
    if query:
        employees = Employee.objects.filter(name__icontains=query)
    else:
        employees = Employee.objects.all()

    print(f"[DEBUG] Total employees found: {employees.count()} | Search term: '{query}'")

    return render(request, 'employees/home.html', {
        'employees': employees,
        'query': query
    })

# Add new employee
def add_employee(request):
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, '✅ Employee added successfully!')
        return redirect('home')
    return render(request, 'employees/form.html', {
        'form': form,
        'form_title': 'Add Employee'
    })

# Edit existing employee
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, instance=employee)
    if form.is_valid():
        form.save()
        messages.success(request, '✏️ Employee updated successfully!')
        return redirect('home')
    return render(request, 'employees/form.html', {
        'form': form,
        'form_title': 'Edit Employee'
    })

# Delete employee
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    messages.warning(request, '🗑️ Employee deleted.')
    return redirect('home')

# Export to CSV
def export_employees_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Department', 'Role', 'Contact', 'Joining Date'])
    for e in Employee.objects.all():
        writer.writerow([e.name, e.department, e.role, e.contact, e.joining_date])
    return response
