from .models import Incident

def create_incident(name, description, category):
    incident = Incident.objects.create(name=name, description=description, category=category)
    return incident


def build_dataset():
    incidents = Incident.objects.all()
    dataset = {
        'categories': [],
        'counts': []
    }
    
    for incident in incidents:
        dataset['categories'].append(incident.category)
        dataset['counts'].append(incident.count)
    
    return dataset
