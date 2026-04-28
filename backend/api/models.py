from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True)
    github_username = models.CharField(max_length=100, blank=True)
    points = models.IntegerField(default=0)
    avatar_level = models.IntegerField(default=1)

    def get_level(self):
        return max(1, self.points // 100)

    def get_avatar(self):
        level = self.get_level()
        if level <= 5:
            return 'etudiant'
        elif level <= 15:
            return 'junior'
        elif level <= 30:
            return 'senior'
        else:
            return 'expert'

    def __str__(self):
        return self.username


class Competence(models.Model):
    CATEGORIES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('devops', 'DevOps'),
        ('data', 'Data'),
        ('autre', 'Autre'),
    ]
    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=50, choices=CATEGORIES)
    niveau_requis = models.IntegerField(default=1)

    def __str__(self):
        return self.nom


class UserCompetence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competences')
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'competence')


class Quete(models.Model):
    TYPES = [
        ('projet', 'Projet'),
        ('formation', 'Formation'),
        ('certification', 'Certification'),
        ('contribution', 'Contribution'),
    ]
    titre = models.CharField(max_length=200)
    description = models.TextField()
    points = models.IntegerField(default=50)
    type_quete = models.CharField(max_length=50, choices=TYPES)
    icone = models.CharField(max_length=10, default='⚔️')

    def __str__(self):
        return self.titre


class UserQuete(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quetes')
    quete = models.ForeignKey(Quete, on_delete=models.CASCADE)
    completee = models.BooleanField(default=False)
    date_completion = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'quete')
