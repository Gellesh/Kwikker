import database_manager

db_manager = database_manager.db_manager


def get_profile_kweeks(username):
    """
        Gets the kweeks that should appear on a specific user profile.
        The kweeks returned are missing some data to construct kweek objects.

        *Parameters:*
            - *username*: The username of the user whose profile kweeks are required.

        *Returns:*
            - *List of dictionaries*: {
                                        | *id (int)*: The id of the kweek.,
                                        | *created_at (datetime)*: The date and time in which the kweek was created.,
                                        | *text (string)*: The main content of the kweek.,
                                        | *media_url (string)*: The url of the image attached with the kweek, if any.,
                                        | *username (string)*: The username of the author of the kweek.,
                                        | *reply_to (int)*: The id of the kweek which this kweek is a reply to, if any.
                                        | }
    """
    query = """
                SELECT ID, CREATED_AT, TEXT, MEDIA_URL, USERNAME, REPLY_TO, IS_REKWEEK FROM
                (
                (SELECT TRUE as IS_REKWEEK, K.ID, K.CREATED_AT, K.TEXT, K.MEDIA_URL, K.USERNAME, K.REPLY_TO, 
                        RK.CREATED_AT AS SORT_BY 
                 FROM KWEEK K
                 JOIN REKWEEK RK ON RK.KWEEK_ID = K.ID
                 WHERE RK.USERNAME = %s)

                UNION

                (SELECT FALSE as IS_REKWEEK, *, CREATED_AT AS SORT_BY FROM KWEEK WHERE USERNAME = %s)
                ) AS KWEEKS
                ORDER BY SORT_BY 
            """

    data = (username, username)
    profile_kweeks = db_manager.execute_query(query, data)
    return profile_kweeks


def get_kweek_statistics(kweek_id, authorized_username):
    """
        Gets the statistics of a kweek and the interactions of the authorized user with it.


        *Parameters:*
            - *authorized_username*: The username of the authorized user.
            - *kweek_id*: The id of the kweek.

        *Returns:*
            - *List of dictionaries*: {
                                | *number_of_likes (int)*: The number of likes of the kweek.,
                                | *number_of_rekweeks (int)*: The number of rekweeks of the kweek.,
                                | *number_of_replies (int)*: The number of replies of the kweek.,
                                | *liked_by_user (bool)*: Whether the kweek is liked by the authorized user.,
                                | *rekweeked_by_user (bool)*: Whether the kweek is rekweeked by the authorized user.
                                | }
    """
    kweek_statistics = {}
    # Number of likes
    query = """
                SELECT COUNT(*) FROM FAVORITE WHERE KWEEK_ID = %s
            """
    data = (kweek_id, )
    response = db_manager.execute_query(query, data)
    if not response:
        kweek_statistics['number_of_likes'] = 0
    else:
        kweek_statistics['number_of_likes'] = response[0].get('count')

    # Number of rekweeks
    query = """
                SELECT COUNT(*) FROM REKWEEK WHERE KWEEK_ID = %s
            """
    response = db_manager.execute_query(query, data)
    if not response:
        kweek_statistics['number_of_rekweeks'] = 0
    else:
        kweek_statistics['number_of_rekweeks'] = response[0].get('count')

    # Number of replies
    query = """
                SELECT COUNT(*) FROM KWEEK WHERE REPLY_TO = %s 
            """
    response = db_manager.execute_query(query, data)
    if not response:
        kweek_statistics['number_of_replies'] = 0
    else:
        kweek_statistics['number_of_replies'] = response[0].get('count')

    # Is liked by the authorized user
    query = """
                SELECT * FROM FAVORITE
                WHERE KWEEK_ID = %s AND USERNAME = %s
            """
    data = (kweek_id, authorized_username)
    if not db_manager.execute_query(query, data):
        kweek_statistics['liked_by_user'] = False
    else:
        kweek_statistics['liked_by_user'] = True

    # Is rekweeked by the authorized user
    query = """
                SELECT * FROM REKWEEK
                WHERE KWEEK_ID = %s AND USERNAME = %s
            """
    data = (kweek_id, authorized_username)
    if not db_manager.execute_query(query, data):
        kweek_statistics['rekweeked_by_user'] = False
    else:
        kweek_statistics['rekweeked_by_user'] = True

    return kweek_statistics


def get_kweek_mentions(kweek_id):
    """
        Gets the mentions in a given kweek.


        *Parameters:*
            - *kweek_id*: The id of the kweek.

        *Returns:*
            - *List of dictionaries*: {
                                | *username (string)*: The username of the mentioned user.,
                                | *starting_index (int)*: The starting index of the mention in the kweek.,
                                | *ending_index (int)*: The ending index of the mention in the kweek.,
                                | *kweek_id (int)*: The id of the kweek.
                                | }
    """
    query = """
                SELECT * FROM MENTION WHERE KWEEK_ID = %s
            """
    data = (kweek_id,)
    mentions = db_manager.execute_query(query, data)
    return mentions


def get_kweek_hashtags(kweek_id):
    """
        Gets the hashtags in a given kweek.


        *Parameters:*
            - *kweek_id*: The id of the kweek.

        *Returns:*
            - *List of dictionaries*: {
                                | *hashtag_id (int)*: The id of the hashtag.,
                                | *starting_index (int)*: The starting index of the hashtag in the kweek.,
                                | *ending_index (int)*: The ending index of the hashtag in the kweek.,
                                | *kweek_id (int)*: The id of the kweek.
                                | }
    """
    query = """
                SELECT *, TEXT FROM KWEEK_HASHTAG 
                JOIN HASHTAG H ON H.ID = HASHTAG_ID
                WHERE KWEEK_ID = %s
            """
    data = (kweek_id,)
    hashtags = db_manager.execute_query(query, data)
    return hashtags


def get_user_data(required_username):
    """
        Gets the basic data of a user.


        *Parameters:*
            - *required_username*: username of the required user.

        *Returns:*
            - *Dictionary*: {
                                | *username (string)*: The username of the required user.,
                                | *screen_name (string)*: The screen name of the required user.,
                                | *profile_image_url (string)*: The url of the required user's profile image.
                                | }
    """
    query = """
                SELECT USERNAME, SCREEN_NAME, PROFILE_IMAGE_URL FROM PROFILE
                WHERE USERNAME = %s
            """
    data = (required_username, )
    user = db_manager.execute_query(query, data)
    return user


def check_following(authorized_username, required_username):
    """
        Checks if the authorized user is following the required user.


        *Parameters:*
            - *authorized_username*: The username of the authorized user.
            - *required_username*: The username of the required user.

        *Returns:*
            - *True*: The authorized user follows the required user.
            - *False*: Otherwise.
    """
    query = """
                SELECT * FROM FOLLOW WHERE FOLLOWER_USERNAME = %s AND FOLLOWED_USERNAME = %s
            """
    data = (authorized_username, required_username)
    if not db_manager.execute_query(query, data):
        return False
    else:
        return True


def check_follows_you(authorized_username, required_username):
    """
        Checks if the authorized user is followed by the required user.


        *Parameters:*
            - *authorized_username*: The username of the authorized user.
            - *required_username*: The username of the required user.

        *Returns:*
            - *True*: The authorized user is followed by the required user.
            - *False*: Otherwise.
    """
    query = """
                SELECT * FROM FOLLOW WHERE FOLLOWER_USERNAME = %s AND FOLLOWED_USERNAME = %s
            """
    data = (required_username, authorized_username)
    if not db_manager.execute_query(query, data):
        return False
    else:
        return True


def check_muted(authorized_username, required_username):
    """
        Checks if the authorized user is muting the required user.


        *Parameters:*
            - *authorized_username*: The username of the authorized user.
            - *required_username*: The username of the required user.

        *Returns:*
            - *True*: The authorized user is muting the required user.
            - *False*: Otherwise.
    """
    query = """
                SELECT * FROM MUTE WHERE MUTER_USERNAME = %s AND MUTED_USERNAME = %s
            """
    data = (authorized_username, required_username)
    if not db_manager.execute_query(query, data):
        return False
    else:
        return True


def check_blocked(authorized_username, required_username):
    """
        Checks if the authorized user is blocking the required user.


        *Parameters:*
            - *authorized_username*: The username of the authorized user.
            - *required_username*: The username of the required user.

        *Returns:*
            - *True*: The authorized user is blocking the required user.
            - *False*: Otherwise.
    """
    query = """
                SELECT * FROM BLOCK WHERE BLOCKER_USERNAME = %s AND BLOCKED_USERNAME = %s
            """
    data = (authorized_username, required_username)
    if not db_manager.execute_query(query, data):
        return False
    else:
        return True


def is_user(username):
    """
        Checks if a username belongs to an existing user.


        *Parameters:*
            - *username*: The username to be checked.

        *Returns:*
            - *True*: The username belongs to an existing user.
            - *False*: The username does not exist.
    """
    query = """
                SELECT * FROM USER_CREDENTIALS WHERE USERNAME = %s
            """
    data = (username,)
    if not db_manager.execute_query(query, data):
        return False
    else:
        return True
