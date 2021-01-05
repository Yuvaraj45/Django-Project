import os,django,random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project1.settings')
django.setup()
from post.models import post
from faker import Faker
from django.contrib.auth.models import User
from django.utils import timezone

def create_data(n):
	fake = Faker()
	for _ in range(n):
		id = random.randint(1,3)
		title=fake.name()
		post.objects.create(
			title=title,
			author=User.objects.get(id=id),
			slug = '-'.join(title.lower().split()),
			description=fake.text(),
			created = timezone.now(),
			updated = timezone.now(),
			status = random.choice(['published','draft'])
			)
create_data(5)
print("successfully created")