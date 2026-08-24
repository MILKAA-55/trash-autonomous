# Projet 1 : Robot-Poubelle

> [!Note]
> ⚠️ Projet en cours de développement. La documentation est susceptible de changer.

Une petite poubelle robot (pour habitation) intelligente capable d’aller à un point A jusqu’à un point B en toute autonomie, l’utilisateur du produit aura une télécommande/station pour exécuter les commandes/instructions à distance. Elle sera en forme d’un petit cylindre. 

Ayant un habitacle dans la cuve, non visible pour y ranger les composants et le matériel nécessaire.

Ceci est mon premier projet en électronique et robotique.

# Théorie :

- 4 roulettes (dont 2 folles et 2 motorisés, un entraînement différentiel)
- Boîtier
- Moteur
- Batterie type industriel
- Raspberry Pi 4
- Capteurs ultrasons (pour éviter les obstacles telles que des murs)

Maintenant, j’ai plusieurs manières pour faire venir le robot vers moi/station :

1. Wake-Word, il se balade dans toute l’habitation et lorsqu'il entend un mot tel que (Viens!) « poubelle vient ici » il se met à se rapprocher de la personne.
2. Un tag que l’utilisateur garde et ainsi le robot se dirigera vers la station.
3. Via un site web/logiciel.
4. Via une télécommande.

J’opte pour la dernière option, «via une télécommande». La principale difficulté est la “connaissance” de l'environnement depuis le robot, car, comment faire comprendre au robot, la localisation exacte de l’utilisateur ? Car d’ici là, naît un compromis entre coûts, précision et latence, qui sont les principaux défi  des concepteurs de solutions de localisation indoor. 

Plus tu veux de précision sans infrastructure, plus il faut de calcul embarqué (donc de batterie, de chaleur, et de prix). Et j'essaie de ne pas dépasser 500 euro.

Ainsi, je choisis la technologie UWB pour la «connaissance» de l’environnement, néanmoins, il existe plusieurs type d’UWB : 

> [!Note]
> PS : Si vous souhaitez, connaître plus à propos de l’uwb, suivez https://tecnoloblog.com/fr/technologie-UWB-ultra-large-bande/ (aucun lien affilié, t’inquiète pas).

- UWB / TOA/ToF (Time of Arrival / Time of Flight) : On mesure le temps que met le signal radio pour parcourir la distance entre les 2 modules. Comme la vitesse des ondes radio est connue (vitesse de la lumière), on en déduit la distance, (distance = temps de vol x vitesse de la lumière). 

**AVANTAGES  :** Précision de l’ordre de 10-30 cm avec l’UWB (grâce à la largeur des bandes très large du signal, cela permet une mesure temporelle très fine).
**LIMITE :** Nécessite une synchronisation d’horloges extrêmement précise entre les 2 modules (au niveau de la nanoseconde), ce qui est très complexe seul.

- TWR (Two-Way Ranging) : Une variante pratique du ToF qui évite le problème de synchronisation d'horloge. Le module A envoie un signal, le module B répond, et A mesure le temps aller-retour total. En connaissant (ou en estimant) le délai de traitement de B, on calcule la distance réelle. 
Avantage : C'est la méthode la plus utilisée en pratique avec les puces comme le DWM3000, car elle ne nécessite pas d'horloges synchronisées entre les deux appareils — chaque module utilise sa propre horloge locale. 
Résultat : Donne uniquement la distance (pas la direction).

Je choisis la technique de l’UWB TWR, avec uniquement 2 modules (car le coût est assez élevé, 23 euro pour le DWM1000 et 43 euro pour le DWM 3000). Je ferai de la MVP thinking (start small, iterate) littéralement, je testerai pendant quelques semaines si 2 modules UWB TWR suffisent et si le robot-poubelle n’est pas en difficulté, si oui, alors j’achèterai un 3e module et un esp32 (et une batterie et un bouton, j’y en reviendrai plus tard).


> Notez que le nombre de module uwb influence directement la puissance et intelligence du système (dans notre cas, le système est le robot-poubelle). Donc, oui, pour de la localisation indoor (intérieur), l’UWB est une excellente solution ! 

Pour avoir une meilleur connaissance, voici un récapitulatif : 

###  UWB : Avantages et Limitations

| Avantages | Limitations |
| :--- | :--- |
| **Précision de localisation :** Marge d'erreur < 10 cm (bien meilleure que le Bluetooth). | **Couverture limitée :** Portée restreinte à quelques mètres seulement. |
| **Vitesse de transmission :** Débit jusqu'à 27 Mbit/s (mobile) et 1.6 Gbit/s (courte distance). | **Interopérabilité :** Normes encore jeunes et souvent propriétaires. |
| **Faible consommation :** Fonctionne des années sur une simple pile bouton. | **Coût de mise en œuvre :** Composants et puces encore relativement chers. |
| **Capacité de pénétration :** Traverse mieux les matériaux que les autres signaux. | **Réglementation :** Déploiement soumis aux règles de chaque pays. |
| **Santé et sécurité :** Très peu d'interférences et signaux difficiles à pirater. | **Adaptation au marché :** Technologie perçue comme "avancée" par le grand public. |

Textes à propos des limitation et avantages de l'UWB, provenant https://tecnoloblog.com/fr/technologie-UWB-ultra-large-bande/#Limitaciones_y_retos_actuales_de_la_UWB | Technoloblog. 

Bon, désolé d’avoir fais du copiez-coller pour la description de l’uwb.

Le fait d’avoir 3 modules uwb twr améliore grandement la précisions, avec 3 modules, on peut faire de la triangulation. Avec seulement 2 modules, on ne peut qu'obtenir la distance, mais pas un plan précis, d’où se trouve exactement les modules; avec 2 modules nous avons uniquement la distance (imprécis pour une navigation), alors qu’avec +3 modules, nous avons une localisation complète (beaucoup plus précis). 

# Système de fixation : 

Le sac poubelle restera coincée, se fera prendre littéralement en sandwich. 

# Choix des composants : 

> [!NOTE]
> Tout le panier de l'ensemble des composants sera divulgué à la fin et également des fichiers de modélisation 3d, gratuitement.

# Roues : 
Elle sera doté de 2 roues motrices (en courant continue) avec les 2 roues folles restantes (pour équilibrer le châssis, celle-là ne sont pas motorisé).

Pourquoi 2 roues ??

Les avantages de 2 roues motorisés : 

- Meilleure autonomie (consommation d’électrique faible) 
- Moins cher
- Plus simple à configurer (hardware) et contrôle de trajectoire simple (différence de vitesse gauche/droite = rotation). 


Les inconvénients des 2 roues motorisé : 

- moins de motricité si le sol est irrégulier, glissant, ou en extérieur (herbe, gravier, petite pente), les roues folles peuvent accrocher sur un obstacle (seuil de porte, petit caillou) .
 
Avantages de 4 roues motorisé : Bien meilleure motricité et franchissement d'obstacles,
plus de couple disponible, utile si le robot est lourd (batterie industrielle + RPi + capteurs), meilleure stabilité sur sol irrégulier
Inconvénients de 4 roues motorisés : plus complexe, il faut synchroniser 4 moteurs (surtout en virage, sinon ça patine ou ça force), Plus cher, plus gourmand en énergie, nécessite un driver capable de gérer 4 canaux (ou 2 drivers). Je choisis du 4 roues, dont 2 folles et motorisée, littéralement du entraînement différentiel (Differential Driver).

# Micro-Controlleur : 

J'hésitais entre le Raspberry Pi 5/4 ou un Esp32, mais, j'opte finalement pour un Esp32. Pourquoi ?? : 

- Moins de consommation électrique.
- Suffisant pour un prototype.
- Démarrage instannée (Raspberry Pi charge un noyaux Linux).
- Prix moins abusif.

Son seul point négatif est qu'il ne supporte pas Python, il lui faut du Micro-Python ou du C++. Ainsi, je vais programmer le software (logiciel) de ce projet en MicroPython, mais ensuite faire une .... en C++, lorsque j'aurai acquis une bonne connaisance en C++. Pour déjà, améliorer le temps de traitement (C++ est plus rapide que Python1)

Attention, nuance ! l'ESP32 n'est pas parfait, mais il convient pour ce projet, par exemple si vous souhaitez faire des algorithme de navigation plus lourd, ajouter une caméra, le Raspberry Pi est mieux ! 

1 = Et oui ! C++ est plus rapide que Python car C++ est un language compilé (ce qui signifie, que lorsque la rédaction de votre programme en C++, C++ tourne et exécute une partie du code en arriere-plan). Le supplément C++ offre un meilleur contrôle sur la gestion de la mémoire et des performances accrues.

# C'est quoi Micro-Python ? 

"Micro-Python est une version de Python adaptées aux microcontrolleurs, écrite en C."

Source : Wikipédia 

# Driver :

Le Raspberry Pi ne sait pas communiquer avec un moteur, alors, il est nécessité d'implémenter un driver lorsque on souhaite utiliser un moteur (dans mon cas); ainsi, j’ai choisis le driver “TB6612FNG Motor Drive Board Module, High-Performance Ultra-L298N Self-Balancing Car Electric Drive Board”. Toutes le panier d’achats (acheté sur Aliexpress) sera disponible gratuitement à la fin du document (vers la rubrique «Informations complémentaires :»). 

Moteur : JGA25-370 Miniature Geared DC Motor With Encoder, 6V/12V/24V, Reversible Rotation, Torque up to 9 KG.CM, Encoder Geared DC Motor. Avec 170 de rpm, et sous 12v. 

# Module UWB : 

La version de UWB la plus récente est la DWM3000, mais elle est très cher (environs 43euro), cependant il faut prendre en compte, qu’il faudra acheter 2 ou 3 modules UWB (2 modules sont le minimum, obligatoire), ainsi j’ai décidé de prendre le DWM1000, qui est beaucoup moins cher (environs 23 euros). Les principaux changements entre les modules uwb DWM3000 et le DWM000 sont, un chiffrage plus important, une consommation d’électrique améliorée (plus intense/élevée chez le DW1000). Pour ce premier prototype, le DWM1000 me convient.

Update/Changement du 09 Juillet : 
J’ai trouvé une alternative moins chère, et suffisant pour mon projet; ainsi, je vous présente le : “Wireless Ranging Positioning Module UWB Module Ultra-Wideband Distance Measurement UART CH5 CH9 SMD EBYTE EWM550” avec USB Câble, donc il fournit en usb-c : USB-C to USB Classic
Module UWB => USB-C => Fils => port USB-Classic sur Raspberry Pi 4 

# Batterie 

J’ai longtemps réfléchi à quelle type de batterie pourrait me convenir, pour ce projet, et j’ai pris la décision de prendre des piles type classique (petite cylindrique), les 18650 2600 mAh 3.7V 10A. Ainsi, il y aura 3 piles 18650.... qui seront stocké sur un dock, on pourra le recharger en usb-c.

Voici le chemin pour la batterie : Recharge en Usb-C => Usb-C to (vers) DC (boîtier stockant/rechargeant les piles).

J’imagine aussi, pour la v2 de ce projet, une borne de recharge automatique, où lorsque le robot sera à une batterie faible, il ira à une borne de recharge automatiquement. 

# Capteurs ultrasons : 

Je m’apprêtait à choisir le “Ultrasonic sensor HC-SR04 HCSR04 to world Ultrasonic Wave Detector Ranging Module HC SR04 HCSR04 Distance Sensor For Arduino“  (bleu) lorsque, la mention “For Arduino” m'a gêné, mais, la mentions n’est faite uniquement pour du Marketing (à l’époque, lorsque ces capteurs ultrasons se sont propagé, la reine était Arduino, toute la documentation, tuto, étaient destinées à Arduino), et aussi que le capteur est “idiot”, en réalité, il s’en fiche à quoi il est connecté. Donc, pourquoi j’ai renoncé de choisir le Ultrasonic sensor HC-SR04 :  
Le capteur fonctionne en 5V : Il a besoin d'être alimenté en 5V pour émettre ses ultrasons, et son signal de retour (la broche Echo) renvoie donc du 5V.
Le Raspberry Pi 4 fonctionne en 3.3V : Les broches GPIO du Raspberry Pi ne tolèrent pas plus de 3.3V. Si tu branches directement la broche Echo (5V) sur un GPIO, tu risques d'endommager définitivement ton Raspberry Pi.
Ainsi, en approfondissant la recherche de capteurs ultrasons, j’ai trouvé un lot de 4 capteurs (parfait !), sortant du 3.3v et pour Raspberry Pi, “RCWL-1601 Ultrasonic Ranging Sensor Module with I2C Interface 2-4.5M Distance Measurement“.

# Contexte plus appronfondi : 

Pour limiter les coûts d'impressions 3d (je n'ai pas d'imprimante 3D, [ici pour découvrir plus d'informations](#prestataires-dimprimerie-3d-abeille-3d)), j'ai décidé de segmenté Robot-Poubelle en plusieurs base, 4 base au total dont 2 (celui du bas et haut) qui sont obligatoire. Ainsi, une méthode Lego pour l'enboitement des pieces : 

![GIF-LEGO](/img/Main/RP-TA.gif)

Une base vaut 100mm.
Donc, un total de 400mm.

Une station est également présente pour lancer/exécuter la recherche et guider le robot vers la station (le robot ira vers la station); ce projet utilise la technologie UWB, ce qui permet une localisation et un positionnement plus précis, type TWR. Néanmoins, le nombre de modules UWB TWR influence directement les performances du système. Warning! Si vous souhaitez réaliser un projet similaire ou un projet utilisant la technologie UWB TWR, il faut obligatoirement 2 modules uwb !! 

![img](/img/Station/4.png)
![img](/img/Station/3.png)
![img](/img/Station/5.png)

Aussi, il y a un couvercle pour cacher le BOM (les composants) qui seront stocké au fond de la cuve, ayant un trou, pour insérer un doigt et soulever/remontez le couvercle pour accéder aux composants; et un petit repose (je ne sais pas comment cela s'appelle), pour fixer le sac poubelle, littéralement le prendre en sandwich.

![img](/img/Main/cover1.png)
![img](/img/Main/cover2.png)

# Pratique : 

“Hi! Before you ship my order, can you please pre-solder JST connectors (2.54mm female) on the JGA25-370 motor wires (red, black, and encoder wire)? It would help a lot for my project. No extra charge needed. Thank you!“ 

# Architecture Logiciel : 

- `uwb.py` : Pour la logique/communication entre les modules uwb. 
- `btn.py` : Pour la logique du bouton de la station et 


# Modélisation 3d : 

Le 10 juillet, j’avais fini la grosse vérification de l'ensemble des composants, ainsi j’ai pu passer à la modélisation 3d du boîtier, je l’ai réalisé sur le logiciel de CAO FreeCAD. 
Voici quelques images : 

Voici l'ordre de modifications de la modélisation 3d : 
![img](img/Main/1.png)
![img](img/Main/4.png)
![img](img/Main/11.png)

Pour voir plus d'images (mais également d'obtenir gratuitement les fichiers de modélisation 3d), rendez vous sur le dossier «img» et vous aurez :

- Main : Le boîtier de la poubelle. 
- Station : Petit boîtier, obligatoire1 au bon fonctionnement de Robot-Poubelle, stockant un 2e module UWB.
- Relay : Petit boîtier, permettant d’améliorer les performances du robot, en stockant un module UWB.

Dans chaque dossier (de Main, Station), un dossier nommé «PCB» y sera présent. Mais le pcb (circuits imprimées) du Relay est identique à celui de la station. 

![img](/img/Main/20.png)
![img](/img/Main/21.png)

1 : Comme déjà mentionnées plus tôt, il est obligatoire d’avoir 2 module uwb, lorsque un projet utilise la technologie UWB TWR.

# Voici l’intégralité du panier Aliexpress de ce projet :

Robot-Poubelle : https://www.aliexpress.com/p/wish-manage/share.html?spm=a2g0o.best.headerAcount.6.2bb6142dnas95B&_gl=1*7mwwf7*_gcl_au*OTE1OTEzNjYyLjE3ODMwMjUyNDQ.*_ga*MjEwMDM3NDc0MS4xNzgzMDI1MjU3*_ga_VED1YSGNC7*czE3ODcwNzE2OTckbzExNSRnMCR0MTc4NzA3MTY5NyRqNjAkbDAkaDA.&smbPageCode=wishlist-amp&spreadId=9D17F73AD6E3321969CEB72831C0C71B5633AE79CA16C14777869F45B6FCB9BF

Station : https://www.aliexpress.com/p/wish-manage/share.html?spm=a2g0o.best.headerAcount.6.2bb6142dnas95B&_gl=1*7mwwf7*_gcl_au*OTE1OTEzNjYyLjE3ODMwMjUyNDQ.*_ga*MjEwMDM3NDc0MS4xNzgzMDI1MjU3*_ga_VED1YSGNC7*czE3ODcwNzE2OTckbzExNSRnMCR0MTc4NzA3MTY5NyRqNjAkbDAkaDA.&smbPageCode=wishlist-amp&spreadId=9D17F73AD6E3321969CEB72831C0C71B93FDB7C95A10AED5ACF5663CEDF8DD53

> [!WARNING]
> # Attention 
> Attention ! Ce projet est en cours de développement, attendez vous à quelques erreurs ou manque, je n’ai rien acheté pour l’instant. 


Pour les anglophones, j’ai légèrement modifier la traduction du nom de ce projet, Trash-Autonomous (Poubelle-Autonome) pour les anglophone et Robot-Poubelle (Robot-Trash) pour les francophone. 

Contactez moi si les liens sont devenu inaccessible (discord : milka330_47221 | E-mail : milkaa.linux@gmail.com). Je change rarement de nom d’utilisateur/mail, mais regarder la bio de mon profil Github (MILKAA-55) pour obtenir les derniers versions de mon e-mail et Discord. 

# Informations complémentaire : 

Merci énormément, d’avoir pris le temps d’avoir lu ce document texte ! 

Voici le récapitulatif financiers du projet :

# Robot-Poubelle :

- Esp32 | : €
- Moteur JGA25-370 | sous 170 de rpm, 12v et avec «With Fixed Bracket» : 14 € 
- Driver TB6612FNG | modèle TB6612FNG, Welded ou unwelded je ne sais pas encore : 3,39 € (pour - Welded, car j’opte pour lui, pas sure à 100%).
- Capteurs Ultrasons (RCWL-1601, avec Interface I2C, mesure de Distance 2-4.5M) | 4 pcs : 8,19 €
- Module UWB EWT550-7G9T10SP | EWT550-7G9T10SP + USB Cable (USB-C) : 12 € avec promotion et 14,22 € hors promotions. X2 (ou *2, multiplié par 2) = 12*2 = 24 € 
- Fils Duponts, Kit 120 pcs (F-F et M-M) : 4,19 €
- Duponts to PH2.0 (pour Moteur) : ! Vérification en cours...
- Piles 18650 2600 mAh 3.7V 10A| 2pcs + 1pcs : 13,89 € pour 2 pcs, et 11€ pour 1 pcs =
13, 89 + 11 = 26,89 €. Prix hors-promotions active. 
- Conteneur batterie/piles : 1,89 €
- Câble Usb-C Femelle to Usb-C Male | modèle 240W-0.5M : 4,59 €
- Connecteur alimentation, Usb-C Femelle to DC | Sous 12V et 5.5*2.1 de diamiètre interne du DC : 
1, 42 €

# Station : 

- Bouton poussoir (permettant l’exécution de la recherche ....) | Couleurs au choix, pour ma part j’ai pris du WHITE LED, 3V-6V(5V), taille au choix, pris 19mm et Momentary : 2,89 €. 
- Esp32 : 5,39 €

Optionnel : Une batterie externe (PowerBank) : https://fr.aliexpress.com/item/1005007748555286.html?pdp_ext_f=%7B%22sku_id%22%3A%2212000059013375681%22%7D&sourceType=1&spm=a2g0o.wish-manage-home.0.0&gatewayAdapt=glo2fra ou Batterie externe Xiaomi 5000mAh, chargeur USB Type C, chargeur de batterie externe pour téléphone mobile intelligent

Les total des prix ne prennent pas en compte, les taxes ni le surcoût de livraisons et ni la hausse des prix. 

> [!WARNING]
> # Attention 
> Attention ! Ce projet est en cours de développement, attendez vous à quelques erreurs ou manque, je n’ai rien acheté pour l’instant. 

X € pour l’électronique.

Une base (de 100mm) vaut 59, 46 € sous 20% de remplissage, hauteur de couche basse (de 0.20mm), PLA - Pro et FDM - Filaments et en classe « économique », prix avec réductions/promotions. 


La station vaut 24, 34 € sous 20% de remplissage, hauteur de couche basse (de 0.20mm), PLA - Pro et 
FDM - Filaments et en classe « économique », prix avec réductions/promotions. 

# Prestataires d’imprimerie 3d : Abeille 3d 

Les prix sont vraiment abusée... je suis en pleine réflexion sur l’achat d’une imprimante 3d. Car, pour les prestataires de services d’imprimerie 3d, ils ajoutent souvent une grosse marge, ainsi, imprimer en 3d chez vous ou un Fablab revient généralement moins cher.  

# Ressources : 

Email : milkaa.linux@gmail.com
Discord : milka330_47221

PS : Resonance by HOME c’est la meilleur musique ! Et The Caretaker aussi.  

