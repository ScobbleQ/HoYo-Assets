# HoYo-Art
A repository for storing and accessing art from HoYoverse games, Genshin Impact and Honkai: Star Rail, with the use of raw.githubusercontent. This is free for anyone to use and all art belongs to HoYoverse. Use Enka.Network API to obtain character IDs.

# Version
<p>Genshin Impact - v5.0<br>Honkai: Star Rail - v2.4</p>

# Update
This repo is managed by GitHub Workflow Actions, I will try to check on it from time to time. Please contact me on Discord(@ScobbleQ) if anything is wrong.

# Example
Genshin Impact using JavaScript:
```js
const { loadImage } = require('@napi-rs/canvas');

let id = "10000051";
const image = await loadImage(`https://raw.githubusercontent.com/ScobbleQ/HoYo-Assets/main/genshin/splash/${id}.png`);
```
Honkai: Star Rail using Python:
```py
from PIL import Image
import requests

id = '1307'
response = requests.get(f'https://raw.githubusercontent.com/ScobbleQ/HoYo-Assets/main/starrail/wish/{id}.png')
image = Image.open(BytesIO(response.content))
```

# Libraries
```
python -m pip install requests
python -m pip install pillow
python -m pip install tqdm
```