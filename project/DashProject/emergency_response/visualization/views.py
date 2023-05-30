from django.shortcuts import render
from .models import Incident, Location
from .incident_builder import create_incident, build_dataset
import plotly.graph_objects as go
from plotly.offline import plot
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# def incident_list(request):
#     incidents = Incident.objects.all()
#     context = {
#         'incidents': incidents
#     }
#     return render(request, 'visualization/incident_list.html', context)


def incident_list(request):
    # Retrieve incident data from the database or any other data source
    incidents = Incident.objects.all()

    # Generate a Plotly graph
    data = [
        go.Bar(
            x=[incident.title for incident in incidents],
            y=[incident.priority for incident in incidents],
            name='Priority'
        ),
        go.Scatter(
            x=[incident.title for incident in incidents],
            y=[incident.response_time for incident in incidents],
            name='Response Time'
        )
    ]

    layout = go.Layout(
        title='Incident Statistics',
        xaxis=dict(title='Incident Title'),
        yaxis=dict(title='Values')
    )

    graph = plot({'data': data, 'layout': layout}, output_type='div')

    context = {
        'incidents': incidents,
        'graph': graph
    }

    return render(request, 'incident_list.html', context)



# def incident_detail(request, incident_id):
#     incident = Incident.objects.get(id=incident_id)
#     context = {
#         'incident': incident
#     }
#     return render(request, 'visualization/incident_detail.html', context)


def incident_detail(request, incident_id):
    incident = Incident.objects.get(id=incident_id)
    
    # Generate Plotly graph
    data = [
        go.Bar(
            x=['Accidents', 'Fire', 'EMS'],
            y=[incident.accidents, incident.fire, incident.ems]
        )
    ]
    layout = go.Layout(title='Incident Types', xaxis=dict(title='Type'), yaxis=dict(title='Count'))
    fig = go.Figure(data=data, layout=layout)
    plot_div = fig.to_html(full_html=False, default_height=500)
    
    context = {
        'incident': incident,
        'plot_div': plot_div
    }
    return render(request, 'visualization/incident_detail.html', context)

@login_required
def create_incident(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        location_id = request.POST.get('location')

        location = Location.objects.get(id=location_id)
        incident = Incident.objects.create(name=name, description=description, category=category, location=location)
        return redirect('incident_detail', incident_id=incident.id)

    locations = Location.objects.all()
    context = {
        'locations': locations
    }
    return render(request, 'visualization/create_incident.html', context)

@login_required
def create_incident_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        
        incident = create_incident(name, description, category)
        # Redirect or render a response
        ...
    
    return render(request, 'create_incident.html')


def visualize_data_view(request):
    dataset = build_dataset()
    # Perform visualizations using the dataset
    ...
    
    return render(request, 'visualize_data.html')

@login_required
def dashboard(request):
    incidents = Incident.objects.all().order_by('-timestamp')  # Sort incidents by timestamp in descending order

    context = {
        'incidents': incidents
    }

    return render(request, 'dashboard.html', context)


# Authentication
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard view
        else:
            # Invalid credentials, display an error message
            error_message = 'Invalid username or password.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login view


