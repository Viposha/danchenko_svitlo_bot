<h2 align="center">Данченка Світло Telegram Bot</h2>

<p align="center">
<img src="screen.jpg" alt="drawing" width="200"/>
</p>

It`s a simpe telegram bot with some specifics:
- After /start command user is saved to small db build with sqlite3
- Main func pings routers IP and when response changed sends message to all users in db
- CI/CD is integrated. After git push command it:
  * Builds Docker image
  * Pushes container to DigitalOcean Container Registry
  * Deploys to Digital Ocean droplet via SSH action

    
   
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png" alt="drawing" width="90"/><img src="https://d1.awsstatic.com/acs/characters/Logos/Docker-Logo_Horizontel_279x131.b8a5c41e56b77706656d61080f6a0217a3ba356d.png" alt="drawing" width="200"/><img src="https://miro.medium.com/max/828/0*DXbRQtXOJYHMmJiR" alt="drawing" width="120"/><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/DigitalOcean_logo.svg/1200px-DigitalOcean_logo.svg.png" alt="drawing" width="120"/><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Telegram_2019_Logo.svg/1200px-Telegram_2019_Logo.svg.png" alt="drawing" width="110"/>
