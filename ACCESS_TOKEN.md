First obtain a standalone app ID; my own “Wishmaster” app is 6950115.

Then pick a scope (see https://vk.com/dev/permissions); you would probably want to include "offline".

Navigate to
https://oauth.vk.com/authorize?client_id=${CLIENT_ID}&scope=${SCOPE}&redirect_uri=blank.html&response_type=token

You will be redirected to
https://oauth.vk.com/blank.html#access_token=...&expires_in=...&user_id=...
