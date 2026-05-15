from django.contrib.auth.models import User
from django.http import HttpResponse

def fix_admin(request):
    User.objects.filter(username="admin").delete()

    User.objects.create_superuser(
        username="admin",
        email="admin@gmail.com",
        password="1234"
    )

    return HttpResponse("Admin reset successful")