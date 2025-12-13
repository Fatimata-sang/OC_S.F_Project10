from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé.
    Ajout de l’âge et des consentements pour répondre aux exigences légales et RGPD.
    """

    age = models.IntegerField(verbose_name="Âge")
    contact_consent = models.BooleanField(
        default=False, verbose_name="Consentement aux contacts"
    )
    data_share_consent = models.BooleanField(
        default=False, verbose_name="Consentement au partage de données"
    )

    # Champs obligatoires pour la création via createsuperuser
    REQUIRED_FIELDS = ['age']

    def __str__(self):
        return self.username


class Project(models.Model):
    """
    Modèle représentant un projet.
    Un projet possède un auteur et peut avoir plusieurs contributeurs.
    """

    # Types de projets (valeurs courtes)
    BACKEND = "B"
    FRONTEND = "F"
    IOS = "I"
    ANDROID = "A"

    # Labels des types de projets
    PROJECT_TYPES = [
        (BACKEND, "Back-end"),
        (FRONTEND, "Front-end"),
        (IOS, "iOS"),
        (ANDROID, "Android"),
    ]

    name = models.CharField(max_length=100, verbose_name="Nom du projet")
    description = models.TextField(verbose_name="Description du projet")
    type = models.CharField(
        max_length=1, choices=PROJECT_TYPES, verbose_name="Type de projet"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name="project_author",
        verbose_name="Auteur du projet",
    )

    contributors = models.ManyToManyField(
        User,
        blank=True,
        related_name="project_contributors",
        verbose_name="Contributeurs du projet",
    )

    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Créé le"
    )
    updated_time = models.DateTimeField(
        auto_now=True, verbose_name="Mis à jour le"
    )

    def __str__(self):
        return f"Projet : {self.name} | Auteur : {self.author}"


class Issue(models.Model):
    """
    Modèle représentant un ticket / problème dans un projet.
    Une issue appartient à un projet et possède :
    - un auteur
    - un assigné
    - un état
    - une priorité
    """

    # Tags : valeurs courtes
    BUG = "B"
    FEATURE = "F"
    TASK = "T"

    TAGS = [
        (BUG, "Bug"),
        (FEATURE, "Fonctionnalité"),
        (TASK, "Tâche"),
    ]

    # États
    TODO = "T"
    IN_PROGRESS = "I"
    COMPLETED = "C"

    STATES = [
        (TODO, "À faire"),
        (IN_PROGRESS, "En cours"),
        (COMPLETED, "Terminé"),
    ]

    # Priorités
    LOW = "L"
    MEDIUM = "M"
    HIGH = "H"

    PRIORITIES = [
        (LOW, "Faible"),
        (MEDIUM, "Moyenne"),
        (HIGH, "Haute"),
    ]

    name = models.CharField(max_length=100, verbose_name="Nom de l’issue")
    description = models.TextField(verbose_name="Description de l’issue")

    tag = models.CharField(max_length=2, choices=TAGS, verbose_name="Tag")
    state = models.CharField(
        max_length=2,
        choices=STATES,
        default=TODO,
        verbose_name="État"
    )
    priority = models.CharField(
        max_length=1,
        choices=PRIORITIES,
        verbose_name="Priorité"
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        blank=True,
        related_name="issues",
        verbose_name="Projet lié",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name="issues_created",
        verbose_name="Auteur",
    )

    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name="issues_assigned",
        verbose_name="Assigné",
    )

    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Créé le"
    )

    def __str__(self):
        return (
            f"{self.name} | Tag: {self.tag}, "
            f"État: {self.state}, Priorité: {self.priority}"
        )


class Comment(models.Model):
    """
    Modèle représentant un commentaire associé à une issue.
    """

    name = models.CharField(max_length=100, verbose_name="Nom du commentaire")
    description = models.TextField(verbose_name="Description")
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        blank=True,
        related_name="comments",
        verbose_name="Issue liée",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name="comments_created",
        verbose_name="Auteur",
    )

    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Créé le"
    )

    issue_url = models.URLField(
        blank=True, verbose_name="URL de l’issue"
    )

    def __str__(self):
        return f"{self.name} | Issue : {self.issue}"

