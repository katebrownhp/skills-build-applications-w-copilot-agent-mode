
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'


    def handle(self, *args, **kwargs):
        # Drop collections directly to avoid Djongo deletion issues
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'], settings.DATABASES['default']['CLIENT']['port'])
        db = client[settings.DATABASES['default']['NAME']]
        for col in ['activity', 'workout', 'leaderboard', 'user', 'team']:
            db[col].drop()

        # Ensure unique index on user email
        db['user'].create_index('email', unique=True)

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Team Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='Team DC Superheroes')

        # Create users individually to avoid Djongo bulk_create issues
        users = []
        users.append(User.objects.create(email='tony@stark.com', username='IronMan', team=marvel, is_superhero=True))
        users.append(User.objects.create(email='steve@rogers.com', username='CaptainAmerica', team=marvel, is_superhero=True))
        users.append(User.objects.create(email='bruce@wayne.com', username='Batman', team=dc, is_superhero=True))
        users.append(User.objects.create(email='clark@kent.com', username='Superman', team=dc, is_superhero=True))

        # Create activities
        Activity.objects.create(user=users[0], activity_type='Running', duration=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], activity_type='Cycling', duration=45, date=timezone.now().date())
        Activity.objects.create(user=users[2], activity_type='Swimming', duration=60, date=timezone.now().date())
        Activity.objects.create(user=users[3], activity_type='Yoga', duration=20, date=timezone.now().date())

        # Create workouts
        w1 = Workout.objects.create(name='Super Strength', description='Strength workout for superheroes')
        w2 = Workout.objects.create(name='Flight Training', description='Aerobic workout for flying heroes')
        w1.suggested_for.set([users[0], users[2]])
        w2.suggested_for.set([users[1], users[3]])

        # Create leaderboards
        Leaderboard.objects.create(team=marvel, total_points=150)
        Leaderboard.objects.create(team=dc, total_points=120)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data!'))
