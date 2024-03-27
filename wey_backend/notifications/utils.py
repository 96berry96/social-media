from .models import Notification
from post.models import Post
from account.models import FriendshipRequest

def create_notification(request, type_of_notification, post_id=None, friendrequest_id=None):
    created_for = None
    
    if type_of_notification == 'postlike':
        body = f'{request.user.name} liked your post'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'postcomment':
        body = f'{request.user.name} commented on your post'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'newfriendrequest':
        body = f'{request.user.name} sent you a friend request'
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
    elif type_of_notification == 'acceptedfriendrequest':
        body = f'{request.user.name} accepted your friend request'
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
    elif type_of_notification == 'rejectedfriendrequest':
        body = f'{request.user.name} rejected your friend request'
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
    
    notification = Notification.objects.create(
        body = body,
        type_of_notification = type_of_notification,
        created_for = created_for,
        created_by = request.user,
        post_id = post_id
    )
    
    return notification