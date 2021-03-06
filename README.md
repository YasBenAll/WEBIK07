### Introductie Likestack:

https://www.youtube.com/watch?v=WkzlbQSQS4M

### Controller: application.py

##### /register
GET:     register.html
POST:    invoer om te registreren op onze site. Nagaan of gebruiker al in database staat, en valide gegevens heeft ingevoerd. Indien alles juist is dan wordt de gebruiker toegevoegd aan de database.

##### /login
GET:    login.html
POST: Pagina om in te loggen op de website. Hierbij moet een gebruikersnaam en wachtwoord ingevoerd worden.  Wanneer gebruiker nog geen account heeft kan deze klikken op de registreer knop en wordt de gebruiker redirect naar /register.

##### /logout
GET:    logout.html
POST:   Wanneer er op logout wordt geklikt zal de gebruiker uitgelogd worden door middel van session clear().

##### /forgot
GET:    forgot.html
POST:   Slaat nieuw wachtwoord op wanneer het antwoord juist is op de security question. 

##### /friends
friends.html
Geeft een tabel met alle vrienden die je volgt en hun like score.

##### /
redirect naar feed (login required)

##### /feed
GET: feed.html een random foto uit de database die de gebruiker nog niet heeft gezien door te checken in history.
POST: Foto wordt geplaatst in history met username en gemarkeerd of deze hem heeft geliket, disliket of als ongepast.

##### /friendfeed
GET: friendfeed.html 
Een random foto uit de database die de gebruiker nog niet heeft gezien en een is van de gebruiker die hij of zij volgt.
POST: Foto wordt geplaatst in history met username en gemarkeerd of deze hem heeft geliket, disliket of als ongepast.

##### /upload
GET: upload.html 
De gebruiker kiest een Giph uit de zoekresultaten die naar aanleiding van zijn zoekwoord.
POST: Foto die de gebruiker heeft geupload wordt in de database van alle foto’s geplaatst.

##### /likelist
likelist.html
Selecteerd alle fotos uit History die de user heeft geliket en zet deze op de pagina.

##### /friend
friend.html 
Zie een lijst van de gebruikers die je volgt. 

##### /mijn_foto's 
mijn_fotos.html 
Zie alle foto's die je geupload hebt.

### Views: html-pagina’s
1.      register.html
2.      login.html
3.      feed.html
4.      upload.html
5.      likelist.html
6.      friendfeed.html
7.      apology.html
8.      apogolgyfeed.html
9.      forgot.html
10.     friend.html
11.     layout.html
12.     uitleg.html


### Models/helpers, helpers.py:
In helpers.py hebben we een fucntie voor upload en feed. 


### 3 databases:
- Users: Alle gebruikers in deze database inclusief uniek id per gebruiker -> gebruiker-id en settings
- Fotos: Alle fotos in de database inclusief uniek id per foto -> foto-id
- History: Hier wordt de activiteit van de gebruiker bijgehouden. Wanneer de gebruiker een foto liked, disliked of markeert als inappropriate wordt deze in de database gezet. 


### Plugins en frameworks:
- Flask
- Flask-uploads
- Bootstrap
- Jinja
- Giphy
- Ajax


### Schetsen van alle pagina's:

![feed](fotos_technisch_ontwerp/feed3.png)

![likelist](fotos_technisch_ontwerp/likelist2.png)

![loginpage](fotos_technisch_ontwerp/loginpage.png)

![menu](fotos_technisch_ontwerp/menu2.png)

![mijnaccount](fotos_technisch_ontwerp/mijnaccount.png)

![mijnfotos](fotos_technisch_ontwerp/mijnfotos2.png)

![rankings](fotos_technisch_ontwerp/rankings2.png)

![register](fotos_technisch_ontwerp/register.png)

![themas](fotos_technisch_ontwerp/themas2.png)

![upload](fotos_technisch_ontwerp/upload.png)

![vrienden](fotos_technisch_ontwerp/vrienden2.png)



