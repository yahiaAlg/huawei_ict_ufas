from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *

@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        try:
            # Parse JSON data if the request is AJAX
            if request.headers.get('Content-Type') == 'application/json':
                data = json.loads(request.body)
                name = data.get('name')
                email = data.get('email')
                message = data.get('message')
            else:
                # Handle form data if submitted via standard form
                name = request.POST.get('name')
                email = request.POST.get('email')
                message = request.POST.get('message')
            
            # Validate required fields
            if not all([name, email, message]):
                return JsonResponse({
                    'success': False,
                    'message': 'Please fill all required fields'
                }, status=400)
            
            # Create contact record
            contact = Contact.objects.create(
                name=name,
                email=email,
                message=message
            )
            
            # Send email notification
            subject = f'New contact from {name}'
            email_message = f"""
            You have received a new contact form submission:
            
            Name: {name}
            Email: {email}
            
            Message:
            {message}
            
            Date: {contact.created_at.strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            # Send email to admin
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  # Add this to settings.py
                fail_silently=False,
            )
            
            # Send confirmation email to user
            confirmation_subject = 'Thank you for contacting Huawei ICT Academy'
            confirmation_message = f"""
            Dear {name},
            
            Thank you for contacting Huawei ICT Academy. We have received your message and will get back to you as soon as possible.
            
            Best regards,
            Huawei ICT Academy Team
            """
            
            send_mail(
                confirmation_subject,
                confirmation_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Your message has been sent successfully. We will contact you soon!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }, status=500)
    
    # If GET request, just render the contact form
    return render(request, 'index.html')

class IndexView(TemplateView):
    template_name = 'pages/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['announcements'] = Announcement.objects.all()
        context['gallery_images'] = GalleryImage.objects.all()
        return context

def about(request):
    return render(request, 'pages/about.html')


