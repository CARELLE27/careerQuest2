from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils import timezone
import requests

from .models import User, Competence, UserCompetence, Quete, UserQuete
from .serializers import (UserSerializer, RegisterSerializer,
                           CompetenceSerializer, UserCompetenceSerializer,
                           QueteSerializer, UserQueteSerializer)


# AUTH
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Compte créé avec succès'}, status=201)
    return Response(serializer.errors, status=400)


# PROFIL
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profil(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# COMPETENCES
@api_view(['GET'])
@permission_classes([AllowAny])
def liste_competences(request):
    competences = Competence.objects.all()
    serializer = CompetenceSerializer(competences, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def mes_competences(request):
    if request.method == 'GET':
        uc = UserCompetence.objects.filter(user=request.user)
        serializer = UserCompetenceSerializer(uc, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        competence_id = request.data.get('competence_id')
        if UserCompetence.objects.filter(user=request.user, competence_id=competence_id).exists():
            return Response({'error': 'Compétence déjà ajoutée'}, status=400)
        uc = UserCompetence.objects.create(user=request.user, competence_id=competence_id)
        request.user.points += 20
        request.user.save()
        return Response(UserCompetenceSerializer(uc).data, status=201)

    if request.method == 'DELETE':
        competence_id = request.data.get('competence_id')
        UserCompetence.objects.filter(user=request.user, competence_id=competence_id).delete()
        return Response({'message': 'Compétence supprimée'})


# QUETES
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mes_quetes(request):
    uq = UserQuete.objects.filter(user=request.user).select_related('quete')
    serializer = UserQueteSerializer(uq, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def completer_quete(request, quete_id):
    try:
        uq = UserQuete.objects.get(user=request.user, quete_id=quete_id)
    except UserQuete.DoesNotExist:
        return Response({'error': 'Quête introuvable'}, status=404)

    if uq.completee:
        return Response({'error': 'Quête déjà complétée'}, status=400)

    uq.completee = True
    uq.date_completion = timezone.now()
    uq.save()

    request.user.points += uq.quete.points
    request.user.save()

    return Response({
        'message': f'+{uq.quete.points} points !',
        'points_total': request.user.points,
        'level': request.user.get_level(),
        'avatar': request.user.get_avatar(),
    })


# CLASSEMENT
@api_view(['GET'])
@permission_classes([AllowAny])
def classement(request):
    users = User.objects.order_by('-points')[:10]
    data = []
    for i, user in enumerate(users):
        data.append({
            'rang': i + 1,
            'username': user.username,
            'points': user.points,
            'level': user.get_level(),
            'avatar': user.get_avatar(),
        })
    return Response(data)


# GITHUB
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def github_repos(request, username):
    try:
        response = requests.get(
            f'https://api.github.com/users/{username}/repos',
            headers={'Accept': 'application/vnd.github.v3+json'},
            timeout=5
        )
        repos = response.json()
        # Donner des points pour les repos
        nb_repos = len(repos) if isinstance(repos, list) else 0
        bonus = nb_repos * 10
        request.user.points += bonus
        request.user.github_username = username
        request.user.save()

        return Response({
            'repos': repos[:10],  # max 10
            'bonus_points': bonus,
            'message': f'GitHub connecté ! +{bonus} points pour {nb_repos} repos'
        })
    except Exception as e:
        return Response({'error': 'Impossible de contacter GitHub'}, status=500)
