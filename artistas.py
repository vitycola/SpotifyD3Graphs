import	spotipy
import	json
import	spotipy.util as	util

scope	=	'user-library-read'
username	=	'Victor Valero'
token	=	util.prompt_for_user_token(username,	scope)
search_str =	'The Limboos'
if	token:
    sp =	spotipy.Spotify(auth=token)
    result	=	sp.search(search_str,	type='artist')
    print	(json.dumps(result,	indent=1))
else:
    print("Can't	get	token	for",	username)