from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse

# Create your views here.
# class AuthView(View):
#     def get(self, request):
#         user = self.request.user
#         if not user.is_anonymous:
#             return redirect('view')
#         return render(request, 'auth.html')
    
#     def post(self, request):
#         action = request.POST.get('action')
#         if action == 'login':
#             return self.handle_login(request)
#         elif action == 'signup':
#             return self.handle_signup(request)
#         else:
#             return JsonResponse({'error': 'Invalid action'}, status=400)
    
#     def handle_login(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             token, created = Token.objects.get_or_create(user=user)
#             request.session['auth_token'] = token.key
#             return JsonResponse({'success': 'Login successful'})
#         else:
#             return JsonResponse({'error': 'Invalid credentials'}, status=400)
    
#     def handle_signup(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         if User.objects.filter(username=username).exists():
#             return JsonResponse({'error': 'Username already exists'}, status=400)
#         user = User.objects.create_user(username=username, password=password)
#         if user:
#             login(request, user)
#             token, created = Token.objects.get_or_create(user=user)
#             request.session['auth_token'] = token.key
#             return JsonResponse({'success': 'Signup successful'})
#         else:
#             return JsonResponse({'error': 'Signup failed'}, status=400)
        
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('auth')

class AuthView(APIView):
    def get(self, request):
        user = self.request.user
        if not user.is_anonymous:
            return redirect('task_list')
        return render(request, 'auth.html')
    
    def post(self, request):
        action = request.data.get('action')
        if action == 'login':
            return self.handle_login(request)
        elif action == 'signup':
            return self.handle_signup(request)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
    
    def handle_login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            request.session['auth_token'] = token.key
            return Response({'success': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
    def handle_signup(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            request.session['auth_token'] = token.key
            return Response({'success': 'Signup successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Signup failed'}, status=status.HTTP_400_BAD_REQUEST)
        