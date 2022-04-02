# Create your views here.
import datetime

# from django.forms import ValidationError

from django.http import JsonResponse
from django.shortcuts import redirect

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


from django.core.mail import send_mail
import uuid
from django.conf import settings


from profiles.models import Profile, Subscription
from posts.models import Post, Comment, Vote, Notification
from .serializer import (
    CommentSerializer,
    NotificationSerializer,
    PostSerializer,
    ProfileSerializer,
    SubscriptionSerializer,
)

# from api import serializer


@csrf_exempt
@api_view(["POST"])
def createUser(request):
    data = request.data
    try:
        user = User.objects.create(username=data["username"], email=data["email"])
        password = data["password"]
        password1 = data["confirm-password"]
        if password == password1:
            user.set_password(data["password"])
        user.save()
        profile = Profile.objects.create(
            user=user,
            name=data["name"],
            username=user.username,
            email=user.email,
            password=user.password,
            profileImage=data["profileImage"],
        )
        if profile.profileImage == "":
            profile.profileImage = "images\profileImages\mehdi.png"
        profile.save()
        verification_mail(
            profile.email, profile.id, profile.name, profile.verificationToken
        )
        profiles = Profile.objects.filter(is_verified=True)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    except Exception as e:
        raise ValidationError()
    # except Exception as e:
    #     return JsonResponse({"message": "Username or Email already exists", "error":"Email and Username should be unique", "status": 400})


def verification_mail(email, id, name, token):
    subject = "Verification Email"
    message = f"Hello {name},\n Welcome to Quora. We are delighted to see you participate.\n Please activate your account by verifying your email. Click on the link below.\n http://localhost:4200/verifying/{id}/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipients = [email]
    send_mail(subject, message, email_from, recipients)


@api_view(["GET"])
def activateAccount(request, pk, sk):
    print("\n\n\nActivating account", request)
    print("Profile Id", pk)
    profile = Profile.objects.get(id=pk)
    if int(sk) == profile.verificationToken:
        profile.is_verified = True
        profile.save()
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@csrf_exempt
def forgetPassword(request):
    data = request.data
    name = data["username"]
    profile = Profile.objects.get(username=name, is_verified=True)
    email = data["email"]
    if profile.email != email:
        return JsonResponse({"message": "Email and username does not match"})
    send_forget_password_mail(email, profile.id, profile.name)
    # Send email
    return JsonResponse(
        {
            "message": "A reset password link is sent to your mail account. Follow the link to reset password."
        }
    )


def send_forget_password_mail(email, id, name):
    token = str(uuid.uuid4())
    subject = "Reset Password Link"
    message = f"Hello {name}, click on the link below to reset your password. \n http://localhost:4200/reset-password/{id}"
    email_from = settings.EMAIL_HOST_USER
    recipients = [email]
    send_mail(subject, message, email_from, recipients)


@api_view(["POST"])
def resetPassword(request, pk):
    profile = Profile.objects.get(id=pk)
    user = profile.user
    if request.data["password"] == request.data["confirmPassword"]:
        user.set_password(request.data["password"])
        user.save()
        return JsonResponse({"message": "New Password set"})
    return JsonResponse({"message": "Password does not match"})


@api_view(["GET"])
def getPosts(request):
    posts = Post.objects.all()
    response = []
    if request.user.is_authenticated != False:
        for post in posts:
            votes = Vote.objects.filter(owner=request.user.profile, post=post)
            if len(votes) > 0:
                vote = votes[0]
            postSerial = PostSerializer(post, many=False)
            response.append(
                {
                    "Post": postSerial.data,
                    "Vote": vote.value if len(votes) > 0 else "None",
                }
            )
        return Response(response)
    else:
        for post in posts:
            postSerial = PostSerializer(post, many=False)
            response.append(
                {
                    "Post": postSerial.data,
                    "Vote": "None",
                }
            )
        return Response(response)


@api_view(["GET"])
def getPost(request, pk):
    # try:
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=post)
    commentserializer = CommentSerializer(comments, many=True)
    serializer = PostSerializer(post)
    response = {"Post": serializer.data, "Comments": commentserializer.data}
    if request.user.is_authenticated != False:
        votes = Vote.objects.filter(owner=request.user.profile, post=post)
        if len(votes) > 0:
            vote = votes[0]
        postSerial = PostSerializer(post, many=False)
        response["Vote"] = vote.value if len(votes) > 0 else "None"
    response["Vote"] = "None"
    return Response(response)


# except:
#     return JsonResponse({"message": "Post not found"})


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def createPost(request):
    post = Post.objects.create()
    data = request.data
    post.owner = request.user.profile
    post.title = data["title"]
    post.body = data["body"]
    post.save()

    serializer = PostSerializer(post)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["PUT"])
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    data = request.data
    post.title = data["title"]
    post.body = data["body"]
    post.save()
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["DELETE"])
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.user.profile == post.owner:
        post.delete()
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addVote(request, pk):
    post = Post.objects.get(id=pk)
    user = request.user.profile
    data = request.data
    vote, created = Vote.objects.get_or_create(
        owner=user,
        post=post,
    )

    vote.value = data["value"]
    vote.save()
    post.getVoteCount

    serializer = PostSerializer(post, many=False)
    response = {"Post": serializer.data, "Vote": vote.value}
    return Response(response)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def addComment(request, pk):
    postObj = Post.objects.get(id=pk)
    data = request.data
    comment = Comment.objects.create(
        owner=request.user.profile, post=postObj, body=data["body"]
    )
    comment.save()
    today = datetime.datetime.now()
    date_time = today.strftime("%H:%M, %m/%d/%Y ")
    notification = Notification.objects.create(
        owner=postObj.owner,
        post=postObj,
        messages=comment.owner.name
        + ' commented on your "'
        + postObj.title
        + '" at '
        + date_time
        # + "on" + date.date()
    )
    notification.save()
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def getComments(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=post)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def editComment(request, pk):
    comment = Comment.objects.get(id=pk)
    data = request.data
    comment.body = data["body"]
    comment.save()
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def getProfiles(request):
    profiles = Profile.objects.filter(is_verified=True)
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def getProfile(request, pk):
    profile = Profile.objects.get(pk=pk)
    posts = Post.objects.filter(owner=profile)
    comments = Comment.objects.filter(owner=profile)
    profileserializer = ProfileSerializer(profile, many=False)
    postserializer = PostSerializer(posts, many=True)
    commentserializer = CommentSerializer(comments, many=True)
    response = {
        "Profile": profileserializer.data,
        "Posts": postserializer.data,
        "Comments": commentserializer.data,
    }
    return Response(response)


@api_view(["GET"])
def profile(request):
    profile = request.user.profile
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@csrf_exempt
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateProfile(request, pk):
    data = request.data

    if request.user.check_password(data["password"]):
        profile = Profile.objects.get(id=pk, is_verified=True)
        img = profile.profileImage
        if request.user.profile == profile:
            profile.name = data["name"]
            profile.username = data["username"]
            profile.email = data["email"]
            profile.profileImage = data["profileImage"]
            if profile.profileImage == "":
                profile.profileImage = (
                    img if img != " " else "images\profileImages\mehdi.png"
                )

            profile.save()
            serializer = ProfileSerializer(profile, many=False)
            return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def changePassword(request):
    user = request.user
    profile = user.profile
    data = request.data
    if request.user.check_password(data["password"]):
        user.set_password(data["newPassword"])
        user.save()

    profile = request.user.profile
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    if request.user.profile == profile:
        profile.delete()
    profiles = Profile.objects.filter(is_verified=True)
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMyProfile(request):
    try:
        profile = request.user.profile
        posts = Post.objects.filter(owner=profile)
        comments = Comment.objects.filter(owner=profile)
        profileserializer = ProfileSerializer(profile, many=False)
        postserializer = PostSerializer(posts, many=True)
        commentserializer = CommentSerializer(comments, many=True)
        response = {
            "Profile": profileserializer.data,
            "Posts": postserializer.data,
            "Comments": commentserializer.data,
        }
        return Response(response)
    except Exception as e:
        raise Exception(e)


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def subscribe(request):
    id = request.data["id"]
    subscription, created = Subscription.objects.get_or_create(
        owner=request.user.profile,
        subscribedUser=Profile.objects.get(id=id, is_verified=True),
    )
    if created:
        subscription.save()
    else:
        subscription.delete()
    serializer = SubscriptionSerializer(subscription, many=False)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getSubscribed(request):
    profile = request.user.profile
    subscriptions = Subscription.objects.filter(owner=profile)
    profiles = []
    for subscription in subscriptions:
        profile1 = Profile.objects.filter(
            id=subscription.subscribedUser.id, is_verified=True
        )
        if profile1:
            profiles.append(profile1[0])
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getFollowers(request):
    profile = request.user.profile
    subscriptions = Subscription.objects.filter(subscribedUser=profile)
    profiles = []
    for subscription in subscriptions:
        profile1 = Profile.objects.filter(id=subscription.owner.id, is_verified=True)
        if profile1:
            profiles.append(profile1[0])
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def getNotifications(request):
    profile = request.user.profile
    notifications = Notification.objects.filter(owner=profile)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def getUnreadNotificationCount(request):
    profile = request.user.profile
    count = 0
    notifications = Notification.objects.filter(owner=profile)
    for notification in notifications:
        if notification.isRead == False:
            count += 1
    return JsonResponse({"unreadNotification": count})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def readNotification(request, pk):
    profile = request.user.profile
    notification = Notification.objects.get(id=pk)
    notification.isRead = True
    notification.save()
    notifications = Notification.objects.filter(owner=profile, isRead=False)
    return JsonResponse({"unreadNotification": len(notifications)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def readAllNotification(request):
    profile = request.user.profile
    notifications = Notification.objects.filter(owner=profile)
    for notification in notifications:
        notification.isRead = True
        notification.save()
    return JsonResponse({"unreadNotification": 0})
