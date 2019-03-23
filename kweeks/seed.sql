INSERT INTO USER_CREDENTIALS(USERNAME, PASSWORD, EMAIL, IS_CONFIRMED) VALUES
('test_user1', 'password', 'test_user1@test.com', TRUE),
('test_user2', 'password', 'test_user3@test.com', TRUE),
('hagar', 'password', 'test_user3@test.com', TRUE);


INSERT INTO PROFILE(USERNAME, SCREEN_NAME, PROFILE_IMAGE_URL, PROFILE_BANNER_URL, BIO, CREATED_AT, BIRTH_DATE)
VALUES
('test_user1', 'test1', 'image_url', 'banner_url', 'bio', '01-01-2019', '01-01-1999'),
('test_user2', 'test2', 'image_url', 'banner_url', 'bio', '01-01-2019', '01-01-1999'),
('test_user3', 'test3', 'image_url', 'banner_url', 'bio', '01-01-2019', '01-01-1999');

INSERT INTO FOLLOW VALUES
('test_user1', 'test_user3'),
('test_user2', 'test_user3'),
('test_user3', 'test_user1');

INSERT INTO MUTE VALUES
('test_user1', 'test_user3');

INSERT INTO BLOCK VALUES
('test_user2', 'test_user1');

INSERT INTO KWEEK(CREATED_AT, TEXT, USERNAME, REPLY_TO) VALUES
('01-01-2010', 'post1, user1', 'test_user1', null),
('01-01-2013', 'post2, user1', 'test_user1', null),
('01-01-2016', 'post3, user1', 'test_user1', null),
('01-01-2011', 'post1, user2', 'test_user2', null),
('01-01-2014', 'post2, user2', 'test_user2', null),
('01-01-2015', 'post3, user2', 'test_user2', null),
('01-01-2012', 'post1, user3', 'test_user3', null),
('01-01-2017', 'post2, user3', 'test_user3', null),
('01-01-2018', 'post3, user3', 'test_user3', null);

INSERT INTO MENTION(KWEEK_ID, USERNAME, STARTING_INDEX, ENDING_INDEX) VALUES
((SELECT ID FROM KWEEK WHERE USERNAME = 'test_user1' LIMIT 1), 'test_user3', 1, 2);

INSERT INTO HASHTAG(TEXT) VALUES ('trend');

INSERT INTO KWEEK_HASHTAG VALUES
((SELECT ID FROM KWEEK WHERE USERNAME = 'test_user3' LIMIT 1),
(SELECT ID FROM HASHTAG WHERE TEXT='trend' LIMIT 1), 1, 2);

INSERT INTO FAVORITE VALUES
('test_user3', (SELECT ID FROM KWEEK WHERE USERNAME = 'test_user1' LIMIT 1), '01-01-2011');

INSERT INTO REKWEEK VALUES
('test_user3', (SELECT ID FROM KWEEK WHERE USERNAME = 'test_user1' LIMIT 1), '01-01-2011'),
('test_user1', (SELECT ID FROM KWEEK WHERE USERNAME = 'test_user3' LIMIT 1), '01-01-2013');