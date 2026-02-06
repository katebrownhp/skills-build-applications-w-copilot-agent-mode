from django.test import TestCase
from .models import User, Team, Activity, Workout, Leaderboard

class ModelSmokeTest(TestCase):
    def test_team_create(self):
        team = Team.objects.create(name='Test Team', description='desc')
        self.assertEqual(str(team), 'Test Team')
    def test_user_create(self):
        team = Team.objects.create(name='T', description='d')
        user = User.objects.create(email='a@b.com', username='u', team=team, is_superhero=True)
        self.assertEqual(str(user), 'u')
    def test_activity_create(self):
        team = Team.objects.create(name='T2', description='d2')
        user = User.objects.create(email='b@c.com', username='u2', team=team, is_superhero=False)
        activity = Activity.objects.create(user=user, activity_type='run', duration=10, date='2024-01-01')
        self.assertEqual(str(activity), 'u2 - run on 2024-01-01')
    def test_workout_create(self):
        workout = Workout.objects.create(name='W', description='desc')
        self.assertEqual(str(workout), 'W')
    def test_leaderboard_create(self):
        team = Team.objects.create(name='T3', description='d3')
        leaderboard = Leaderboard.objects.create(team=team, total_points=42)
        self.assertIn('T3', str(leaderboard))
