By running this script you can:
- get mp3, img, title and description as input
- generate episode cover (for youtube, RSS, VK)
- upload mp3 and covers to file_hosting via scp
- render video using mp3 and cover
- upload video to youtube in proper playlist, using youtube API
- prepare HTML text for post on a site

You can use `./release -h` to get help.

Example:  
```./release.py -i img/test.jpeg -m 'mp3/be0.mp3' -t 'telecom №96. Лист и фекотист' -d description.html```

You are recommended to put episode mp3 to `mp3/` directory and image to `img/`.  
Generated covers will be saved in `img/covers`.  
Rendered video will be saved in `mp4/`. 

`img/` direcory aslo contains default templates for covers and default feed images in case there is no image file provided.

All the temporary files are in `.gitignore` to not change the repo.

You can put environment variables to `.env` file to make them available for `decouple`.

To get this script run you alse need `client_secrets.json` for google account responsible for the youtube channel.