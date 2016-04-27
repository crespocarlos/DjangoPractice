from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

GAME_STATUS_CHOICES = (
    ('A', 'Ativo'),
    ('F', 'Primeiro Jogador Vence'),
    ('S', 'Segundo Jogador Vence'),
    ('D', 'Empate')
)

FIRST_PLAYER_MOVE = 'X'
SECONDE_PLAYER_MOV = 'O'
BOARD_SIZE = 3


class GamesManager(models.Manager):

    def games_for_user(self, user):
        """Return a queryset of games that this user participates in"""
        return super(GamesManager, self).get_queryset().filter(
            Q(first_player_id=user.id) | Q(second_player_id=user.id))

    def new_game(self, invitation):
        game = Game(first_player=invitation.to_user,
                    second_player=invitation.from_user,
                    next_to_move=invitation.to_user)
        return game


class Game(models.Model):
    first_player = models.ForeignKey(User, related_name="games_first_player")
    second_player = models.ForeignKey(User, related_name="games_secod_player")
    next_to_move = models.ForeignKey(User, related_name="games_to_move")
    start_time = models.DateTimeField(auto_now_add=True)
    last_ative = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1, default='A', choices=GAME_STATUS_CHOICES)
    objects = GamesManager()

    def as_board(self):
        """Retorna a representação de um tabuleiro como uma lista bi-dimensional,
        para que você possa pedir pelo estado do quadrado na posição [x][y].

        Isso irá conter a lista de linhas, onde cada linha é uma lista de 'X',
        'O' ou ''. Por exemplo, uma posição no tabuleiro 3x3:

        [['','X',''],
         ['O,'',''],
         ['X','','']]"""
        board = [['' for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]

        for move in self.move_set.all():
            boad[move.y][
                move.x] = FIRST_PLAYER_MOVE if move.by_first_player else SECOND_PLAYER_MOVE
        return board

    def is_empty(self, x, y):
        return not self.move_set.filter(x=x, y=y).exists()

    def last_move(self):
        return self.move_set.latest()

    def get_absolute_url(self):
        return reverse('tictactoe_game_detail', args=[self.id])

    def is_users_move(self, user):
        return self.status == 'A' and self.next_to_move == user

    def __str__(self):
        return "{0} vs {1}".format(self.first_player, self.second_player)


class Move(models.Model):
    x = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(BOARD_SIZE - 1)])
    y = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(BOARD_SIZE - 1)])
    comment = models.CharField(max_length=300)
    game = models.ForeignKey(Game)
    by_first_player = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        get_latest_by = 'timestamp'

    def player(self):
        return self.game.first_player if self.by_first_player else self.game.second_player


class Invitation(models.Model):
    from_user = models.ForeignKey(User, related_name='invitations_sent')
    to_user = models.ForeignKey(
        User,
        related_name='invitations_received',
        verbose_name="Usuário para convidar",
        help_text="Por favor, selecione o usuário que você quer jogar")
    message = models.CharField(
        "Mensagem Opcional",
        max_length=300,
        blank=True,
        help_text="Adicionar uma mensagem amigável nunca é demais")
    timestamp = models.DateTimeField(auto_now_add=True)
