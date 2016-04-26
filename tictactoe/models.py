from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

GAME_STATUS_CHOICES = (
    ('A', 'Ativo'),
    ('F', 'Primeiro Jogador Vence'),
    ('S', 'Segundo Jogador Vence'),
    ('D', 'Empate')
)


class GamesManager(models.Manager):

    def games_for_user(self, user):
        """Return a queryset of games that this user participates in"""
        return super(GamesManager, self).get_queryset().filter(
            Q(first_player_id=user.id) | Q(second_player_id=user.id))


class Game(models.Model):
    first_player = models.ForeignKey(User, related_name="games_first_player")
    second_player = models.ForeignKey(User, related_name="games_secod_player")
    next_to_move = models.ForeignKey(User, related_name="games_to_move")
    start_time = models.DateTimeField(auto_now_add=True)
    last_ative = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1, default='A', choices=GAME_STATUS_CHOICES)
    objects = GamesManager()

    def __str__(self):
        return "{0} vs {1}".format(self.first_player, self.second_player)


class Move(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    comment = models.CharField(max_length=300)
    game = models.ForeignKey(Game)
