from . import query_factory
from timelines_and_trends import actions
from models import UserProfile
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
"""
    All the functions containing the logic should reside here. 
    The routes functions should contain no logic, they should only call the functions in this module.
"""


def get_user_profile(authorized_username, username):
    """
            The function return user profile for a specific user.

            Parameters:
                authorized_username (string): The user that is logged in now .
                username (string): The user that we will test friendship on it like (following ..)

            Returns:
                UserProfile: an object of user profile .
    """
    profile = query_factory.get_user_profile(username)
    if profile:
        profile["profile_image_url"] = 'http://127.0.0.1:5000/user/upload/picture/' + profile[
            "profile_image_url"]
        profile["profile_banner_url"] = 'http://127.0.0.1:5000/user/upload/banner/' + profile[
            "profile_banner_url"]
        profile["followers_count"] = query_factory.get_user_followers(username)["count"]
        profile["following_count"] = query_factory.get_user_following(username)["count"]
        profile["kweeks_count"] = query_factory.get_number_of_kweeks(username)['count']
        profile["likes_count"] = query_factory.get_number_of_likes(username)['count']
        friendship = actions.get_friendship(authorized_username, username)
        profile.update(friendship)
        return UserProfile(profile)
    else:
        return -1


def update_user_profile(authorized_username, bio, screen_name):
    """
                The function updates bio and screen name in user profile.

                Parameters:
                    authorized_username (string): The user that is logged in now .
                    bio (text): The biography of the user.
                    screen_name(string): The name shown on profile screen.
                Returns:
                    response: which is none of case in successful update .
                    -1: in case of exception error in database.
                    0: in case of bad request.
    """
    if bio == "" and screen_name == "":
        return 0
    if bio is not None or screen_name is not None:

        response = query_factory.update_user_profile(authorized_username, bio, screen_name)
        if response is None:
            return response
        else:
            return -1
    else:
        return 0


def update_profile_picture(file, authorized_username):
    """
                    The function updates profile picture.

                    Parameters:
                        file (file): The profile image which will be updated.
                        authorized_username (string): The user that is logged in now .
                    Returns:
                        filename: the image name saved in database .
    """
    target = os.path.join(APP_ROOT, 'images\profile/')
    if not os.path.isdir(target):
        os.mkdir(target)
    filename = authorized_username + 'profile.png'
    response = query_factory.update_user_profile_picture(authorized_username, filename)
    if response is None:
        destination = "/".join([target, filename])
        file.save(destination)
        return filename

    else:
        return -1


def delete_profile_picture(authorized_username):
    """
                            The function deletes profile picture and reset it to default.

                            Parameters:
                                authorized_username (string): The user that is logged in now .
                            Returns:
                                response: which is none of case in successful deletion .
    """
    filename = 'profile.jpg'
    response = query_factory.update_user_profile_picture(authorized_username, filename)
    if response is None:
        return

    else:
        return -1


def update_profile_banner(file, authorized_username):
    """
                        The function updates banner picture.

                        Parameters:
                            file (file): The banner image which will be updated.
                            authorized_username (string): The user that is logged in now .
                        Returns:
                            filename: the image name saved in database .
    """
    target = os.path.join(APP_ROOT, 'images\ banner/')
    if not os.path.isdir(target):
        os.mkdir(target)
    filename = authorized_username + 'banner.png'
    response = query_factory.update_user_banner_picture(authorized_username, filename)
    if response is None:
        destination = "/".join([target, filename])
        file.save(destination)
        return filename
    else:
        return -1


def delete_banner_picture(authorized_username):
    """
                        The function deletes banner picture and reset it to default.

                        Parameters:
                            authorized_username (string): The user that is logged in now .
                        Returns:
                            response: which is none of case in successful deletion .
    """
    filename = 'banner.png'
    response = query_factory.update_user_banner_picture(authorized_username, filename)
    if response is None:
        return

    else:
        return -1
