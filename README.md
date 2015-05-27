This is the project Media Link

People will have choice to submit a link or share original content by uploading it.

People will be able to share links to media content, classify it by the type, and comment and rate it.

People looking to search for media or explore genre will be able to view a list of media, with a filter at the top.

Filter will allow them to filter by type of media (books, shows, movies, art, music, etc.).

Each media will have at least one link - along with ability to have more links.


The "art" class:
- art_id (integer, primary key)
- user_id (link back to who posted it)
- title (text)
- artist_name (text)
- ratings (integer, averaged)
- link (text) # maybe we want to check if this is a not repeated, show if external art
- upload_file (text) # show if custom art
- type (can be selected from books, motion picture, music, visual art)
- tags (can be genre tag, qualifier tag, artist name, etc. This will be a class/table - don't want to duplicate tags.)
- comments (will be another class)
- last_update_by (text) # name of the user to last update this item

The "tags" class:
- tag_id (integer, primary key)
- tag_name (text)

The "tag_art" class:
- tag_id (integer) # to link back to the media
- art_id (integer) # to link back to the media that has this tag

The "comments" class:
- comment_id (integer, primary key)
- user_id (link back to the user)
- timestamp (timestamp of when comment was made)
- comment_text (text)
- (in the future, make comment's reply-able)
- art_id (link back to the media)

The "user" class:
- user_id (integer, primary key)
- user_name (text)
- user_image (text)
- email (text)
- is_admin (bool) # only admins will be able to delete comments and links, admin can make other admins

