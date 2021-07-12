By running this script you can:
- get mp3, img, title and description as input
- generate episode covers (for youtube, RSS, VK)
- upload mp3 and covers to file_hosting via scp
- render video using mp3 and cover
- upload video to youtube in proper playlist, using youtube API
- publish podcast to the site

You can use `./release.py -h` to get help.

Examples:
Publishing podcast:
```./release.py -i img/test.jpeg -m 'mp3/test.mp3' -t 'telecom №196. Лист и феоктист' -d description.html```
Publishing podcast announce:
```./release.py -i img/test.jpeg -t 'telecom №196. Лист и феоктист' --announce 20210718T140000```

You are recommended to put episode mp3 to `mp3/` directory and image to `img/`.  
Generated covers will be saved in `img/covers`.  
Rendered video will be saved in `mp4/`. 

`img/` direcory aslo contains default templates for covers and default feed images in case there is no image file provided.

All the temporary files are in `.gitignore` to not change the repo.

You can put environment variables to `.env` file to make them available for `decouple`.

To get this script run you alse need `client_secrets.json` for google account responsible for the youtube channel.

Possible arguments:
- `-i IMG` - Point to podcast image file. **Mandatory**
- `-m MP3` - Point to podcast mp3 file. **Mandatory for podcasts**. No need for Announces
- `-t TITLE` - Title of the podcast or announece. "Анонс" will be added automatically when using `--announce`
- `-d DESCRIPTION_FILE` - Point to a file with shownotes
- `--announce ANNOUNCE` - This will public podcast announce. It takes On-air date in format `YYYYmmddTHHMMSS`, like `20210718T140000`
- `--no-video` - If you don't wan't to render and upload video for some reason.

To run script in environment you poetry can be used as `poetry run python release.py ...`