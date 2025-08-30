# Contribuer à "Detection de Bad Buzz"

Bonjour et merci de l'intérêt que vous portez à ce projet ! Nous sommes ravis de vous accueillir. Toute contribution, qu'elle soit petite ou grande, est la bienvenue.

Ce document est un guide pour vous aider à contribuer efficacement.

## Table des matières
- [Comment puis-je contribuer ?](#comment-puis-je-contribuer-)
  - [Rapporter des bugs](#rapporter-des-bugs)
  - [Suggérer des améliorations](#suggérer-des-améliorations)
  - [Proposer du code](#proposer-du-code)
- [Mise en place de l'environnement](#mise-en-place-de-lenvironnement)
- [Processus de Pull Request](#processus-de-pull-request)
- [Style de code](#style-de-code)
- [Code de conduite](#code-de-conduite)

## Comment puis-je contribuer ?

### Rapporter des bugs

Si vous trouvez un bug, veuillez vous assurer qu'il n'a pas déjà été rapporté en consultant les [Issues GitHub](https://github.com/emmanuel-ouedraogo/P7OEDetectionBadBuzzParDeepLearning/issues).

Si vous ne trouvez pas de ticket ouvert correspondant, veuillez en [ouvrir un nouveau](https://github.com/emmanuel-ouedraogo/P7OEDetectionBadBuzzParDeepLearning/issues/new). Assurez-vous d'inclure :
- Un **titre clair et descriptif**.
- Une **description précise** des étapes pour reproduire le bug.
- Le **comportement attendu** et le **comportement observé**.
- Des captures d'écran si possible.

### Suggérer des améliorations

Les suggestions sont les bienvenues ! Pour toute nouvelle fonctionnalité ou amélioration d'une fonctionnalité existante, veuillez d'abord ouvrir une "Issue" pour en discuter. Cela nous permet de nous assurer que votre proposition correspond à la direction du projet.

### Proposer du code

Les contributions de code sont la meilleure façon d'améliorer le projet. Nous suivons le modèle "fork and pull".

## Mise en place de l'environnement

Pour travailler sur le code, vous aurez besoin de configurer votre environnement de développement. Toutes les instructions nécessaires se trouvent dans le fichier [README.md](./README.md#installation).

En résumé :
1.  Forkez le dépôt.
2.  Clonez votre fork en local.
3.  Créez un environnement virtuel et installez les dépendances avec `pip install -r requirements.txt`.

## Processus de Pull Request

1.  **Forkez** le dépôt et clonez-le sur votre machine.
2.  Créez une nouvelle branche pour vos modifications :
    ```sh
    git checkout -b ma-super-fonctionnalite
    ```
3.  Effectuez vos modifications. Assurez-vous que le code est propre et commenté si nécessaire.
4.  **Commitez** vos changements. Utilisez des messages de commit clairs et descriptifs. Nous suivons la convention Conventional Commits. Par exemple :
    - `feat: Ajout de l'authentification via JWT`
    - `fix: Correction d'une fuite de mémoire dans le traitement des images`
    - `docs: Mise à jour du README avec les instructions de déploiement`
    ```sh
    git commit -m "feat: Description de ma nouvelle fonctionnalité"
    ```
5.  **Poussez** votre branche vers votre fork sur GitHub :
    ```sh
    git push origin ma-super-fonctionnalite
    ```
6.  Ouvrez une **Pull Request** (PR) vers la branche `main` du dépôt original.
    - Remplissez le template de la PR avec une description claire de ce que vous avez fait.
    - Liez la PR à l'issue correspondante si elle existe (ex: `Closes #123`).

## Style de code

Pour maintenir une cohérence dans le code, nous utilisons les outils suivants :
- **Black** pour le formatage du code Python.
- **Flake8** pour le linting.

Avant de soumettre votre code, veuillez lancer ces outils pour vous assurer que tout est en ordre.

## Code de conduite

Ce projet et tous ses contributeurs sont soumis à un Code de Conduite. En participant, vous vous engagez à respecter ce code. Veuillez signaler tout comportement inacceptable.

Merci encore pour votre contribution !
