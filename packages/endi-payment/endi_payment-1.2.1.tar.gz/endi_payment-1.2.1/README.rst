Librairie enDI pour la gestion des encaissements
======================================================

Cette librairie a pour objectif de fournir un ensemble cohérent pour la gestion
des encaissements, ce afin de répondre aux exigences de la loi de finance 2018.
Le texte suivant `http://bofip.impots.gouv.fr/bofip/10691-PGP` décrit plus en
détail le besoin à couvrir

Elle fonctionne comme suit :

- Les opérations d'encaissement sont effectuées au travers d'une API publique
- Pour chaque opération d'encaissement, une entrée est écrite dans le journal

Le journal est le garant de l'intégrité des opérations d'encaissement.

Activation du module
---------------------

L'api publique est configurable dans enDI au travers du fichier de
configuration .ini.

Assurez-vous que la librairie endi_payment est bien dans les pyramid.includes

.. code-block:: console

   pyramid.includes = ...
                      ...
                      endi_payment

Configurez le service endi.interfaces.IPaymentRecordService

.. code-block:: console

   endi.interfaces.IPaymentRecordService = endi_payment.public.PaymentService

Configurez les journaux de 'endi_payment'. Voir la documentation sur le module
python logging pour le détail : https://docs.python.org/2/library/logging.html
ainsi que les exemples dans le fichier development.ini.sample.


Configurez le service de journalisation
endi_payment.interfaces.IPaymentRecordHistoryService à utiliser.

endi_payment propose deux services de journalisation

   HistoryLogService : Service par défaut, prévu pour le mode développement, se
   content de journaliser les actions sans détails.

   HistoryDBService : Journalise les actions effectuées dans une base de données
   spécifiques (pas forcément sur le même serveur mysql)

HistoryDBService
...................

Pour activer la journalisation détaillée dans une base de données spécifiques
ajouter la ligne suivante dans la section [app:endi] du fichier .ini

.. code-block:: console

   endi_payment.interfaces.IPaymentRecordHistoryService = endi_payment.history.endi_payment.history.HistoryDBService

Créer une nouvelle base de données, vous pouvez utiliser l'utilitaire
./tools/add_payment_database.sh fournit dans le repository endi.

.. code-block:: console

   cd endi/
   ./tools/add_payment_database.sh
   # Suivez les instructions

Puis saisissez les informations de connexion de la nouvelle base de données dans
la section [app:endi] du fichier .ini

.. code-block:: console

   endi_payment_db.url = mysql://endi_payment:endi_payment@localhost/endi_payment?charset=utf8


Validation locale d'archive
-----------------------------

Pour chaque action d'encaissement dans enDI, une entrée est ajoutée dans
l'historique d'encaissement.

Cette entrée :

    * contient un hash de l'entrée précédente de l'historique.
    * est ajoutée à un journal mensuel des modifications
    * est associée à une entrée de "scellement" dans la table
      endi_payment_archive_seal. La clé de scellement correspond à la somme sha1
      du fichier journal.

En l'absence d'un tiers de confiance, cette méthode rend compliquée la
réécriture de l'historique et fournie une garantie assez élevée d'intégrité des
données.
