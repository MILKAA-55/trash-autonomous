# PCB (ou schéma du cablage) de Robot-Poubelle : 

* **Alimentation et Distribution d'Énergie (VCC / GND)**
* **Ligne 3.3V / VCC :** Distribuée depuis la broche d'alimentation principale de l'ESP32-S3-N16R8 (U1) vers :
* Les broches `VCC` des 4 capteurs ultrasons `RCWL-1601` (U3, U4, U5, U6)
* La broche d'alimentation logique du module radio UWB `EWM550-7G9T10SP` (U7)
* La broche d'alimentation logique du driver de moteur `TB6612FNG` (U2)
* L'alimentation des encodeurs (fils bleus) des deux moteurs `JGA25-370` (E1, E2)


* **Ligne GND (Masse commune) :** Interconnectée entre la masse de l'ESP32-S3 (U1) et :
* Les broches `GND` des 4 capteurs ultrasons `RCWL-1601` (U3 à U6)
* La broche `GND` du module UWB `EWM550-7G9T10SP` (U7)
* La broche `GND` du driver de moteur `TB6612FNG` (U2)
* Les masses des encodeurs (fils verts) des moteurs `JGA25-370` (E1, E2)




* **Capteurs Ultrasons `RCWL-1601` (U3, U4, U5, U6) $\rightarrow$ ESP32-S3 (U1)**
* **Capteur Avant-Gauche (U3) :**
* Broche `Trig` $\rightarrow$ Reliée à une broche GPIO dédiée de l'ESP32-S3 pour le déclenchement des impulsions ultrasonores
* Broche `Echo` $\rightarrow$ Reliée à une broche GPIO de l'ESP32-S3 configurée en entrée pour la réception du signal réfléchi


* **Capteur Avant-Droit (U4) :**
* Broche `Trig` $\rightarrow$ Reliée à une broche GPIO dédiée de l'ESP32-S3
* Broche `Echo` $\rightarrow$ Reliée à une broche GPIO de l'ESP32-S3


* **Capteur Latéral/Arrière 1 (U5) :**
* Broche `Trig` $\rightarrow$ Reliée à une broche GPIO de l'ESP32-S3
* Broche `Echo` $\rightarrow$ Reliée à une broche GPIO de l'ESP32-S3


* **Capteur Latéral/Arrière 2 (U6) :**
* Broche `Trig` $\rightarrow$ Reliée à une broche GPIO de l'ESP32-S3
* Broche `Echo` $\rightarrow$ Reliée à une broche GPIO de l'ESP32-S3




* **Module Radio UWB `EWM550-7G9T10SP` (U7) $\rightarrow$ ESP32-S3 (U1)**
* Liaison Série UART :
* Broche `TXD` du module UWB $\rightarrow$ Connectée à la broche `RX` (GPIO de réception série) de l'ESP32-S3
* Broche `RXD` du module UWB $\rightarrow$ Connectée à la broche `TX` (GPIO de transmission série) de l'ESP32-S3


* Lignes de contrôle et de signal additionnelles reliées aux GPIOs de configuration et de statut de l'ESP32-S3


* **Driver de Moteur `TB6612FNG` (U2) $\rightarrow$ ESP32-S3 (U1)**
* Commandes logiques de direction et de vitesse PWM :
* Broche `PWMA` $\rightarrow$ Reliée à une sortie PWM de l'ESP32-S3 pour contrôler la vitesse du moteur gauche
* Broches `AIN1` et `AIN2` $\rightarrow$ Reliées aux GPIOs de direction de l'ESP32-S3 pour le moteur gauche
* Broche `PWMB` $\rightarrow$ Reliée à une sortie PWM de l'ESP32-S3 pour contrôler la vitesse du moteur droit
* Broches `BIN1` et `BIN2` $\rightarrow$ Reliées aux GPIOs de direction de l'ESP32-S3 pour le moteur droit
* Broche `STBY` (Standby) $\rightarrow$ Reliée à une broche GPIO de l'ESP32-S3 pour activer ou désactiver le driver




* **Driver de Moteur `TB6612FNG` (U2) $\rightarrow$ Moteurs `JGA25-370` (E1, E2)**
* Canaux de puissance de sortie :
* Bornes de sortie `AO1` et `AO2` du driver $\rightarrow$ Reliées respectivement au fil Rouge (`Motor+`) et au fil Noir (`Motor-`) du Moteur Gauche (E1)
* Bornes de sortie `BO1` et `BO2` du driver $\rightarrow$ Reliées respectivement au fil Rouge (`Motor+`) et au fil Noir (`Motor-`) du Moteur Droit (E2)




* **Encodeurs Quadrature des Moteurs (E1, E2) $\rightarrow$ ESP32-S3 (U1)**
* Moteur Gauche (E1) :
* Fil Jaune (`Signal A`) $\rightarrow$ Relié à une broche GPIO de l'ESP32-S3 configurée en interruption externe pour le comptage des impulsions odométriques
* Fil Blanc (`Signal B`) $\rightarrow$ Relié à une deuxième broche GPIO de l'ESP32-S3 pour la détermination du sens de rotation


* Moteur Droit (E2) :
* Fil Jaune (`Signal A`) $\rightarrow$ Relié à une broche GPIO de l'ESP32-S3 configurée en interruption externe
* Fil Blanc (`Signal B`) $\rightarrow$ Relié à une deuxième broche GPIO de l'ESP32-S3 pour le suivi de la direction du moteur droit