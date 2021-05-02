/* Artists */
INSERT INTO artists (name, city, state, phone, genres, facebook_link, image_link, seeking_venue, seeking_description, website)
VALUES ('Batman and the Cat Clan', 'Gotham', 'NY', '+1-800-BATMAN', '["Jazz", "Reggae", "Swing", "Classical", "Folk"]', 'https://www.facebook.com/TheMusicalHop', 'https://external-preview.redd.it/hz97a0_m_j9AoB8pC4TpVIOb4mLzfuPW6f5CsU7TywM.jpg?auto=webp&s=99bcfaa4433ed4be0d504e3d78c7346d0d6e0d8c', TRUE, 'We are on the lookout for a local artist to play every two weeks. Please call us.', 'https://www.themusicalhop.com');
INSERT INTO artists (name, city, state, phone, genres, facebook_link, image_link, seeking_venue, seeking_description, website)
VALUES ('The Massive Massives', 'Gotham', 'NY', '+1-800-BATMAN', '["Jazz", "Reggae", "Swing", "Classical", "Folk"]', 'https://www.facebook.com/TheMusicalHop', 'https://metro.co.uk/wp-content/uploads/2020/01/chonky-for-featured-0555.jpg', TRUE, 'We are on the lookout for a local artist to play every two weeks. Please call us.', 'https://www.themusicalhop.com');
INSERT INTO artists (name, city, state, phone, genres, facebook_link, image_link, seeking_venue, seeking_description, website)
VALUES ('Meowdy', 'Gotham', 'NY', '+1-800-BATMAN', '["Jazz", "Reggae", "Swing", "Classical", "Folk"]', 'https://www.facebook.com/TheMusicalHop', 'https://pbs.twimg.com/media/C61vO2wVwAAYhW0.jpg:large', TRUE, 'We are on the lookout for a local artist to play every two weeks. Please call us.', 'https://www.themusicalhop.com');


/* Venues */
INSERT
INTO venues (name, city, state, address, genres, seeking_talent, image_link)
VALUES ('The Cave', 'San Francisco', 'CA', '1015 Folsom Street', '["Jazz", "Folk"]', FALSE, 'https://static1.cbrimages.com/wordpress/wp-content/uploads/2020/07/Bat-Cave.jpg');
INSERT
INTO venues (name, city, state, address, genres, seeking_talent, image_link)
VALUES ('Shitbaby House', 'San Diego', 'NY', '1015 Folsom Street', '["Jazz", "Stuff", "EDM"]', FALSE, 'https://pbs.twimg.com/media/Eddr4hmXsAIjVz3.jpg');
INSERT
INTO venues (name, city, state, address, genres, seeking_talent, image_link)
VALUES ('High Noon Ranch', 'A Place', 'NJ', '1015 Folsom Street', '["Shitmusic"]', FALSE, 'http://movie-locations.com/movies/h/High-Noon-Columbia-Street.jpg');


/* Shows */
INSERT INTO shows (venue_id, artist_id, start_time) VALUES (1, 3, '2019-05-21 21:30:00');
INSERT INTO shows (venue_id, artist_id, start_time) VALUES (2, 1, '2021-04-08 20:00:00');
INSERT INTO shows (venue_id, artist_id, start_time) VALUES (2, 2, '2019-06-15 23:00:00');
INSERT INTO shows (venue_id, artist_id, start_time) VALUES (3, 1, '2035-04-08 20:00:00');
INSERT INTO shows (venue_id, artist_id, start_time) VALUES (3, 3, '2021-04-23 19:00:00');