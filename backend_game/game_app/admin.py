from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(BattleUnit)
admin.site.register(PlayerBattleUnit)
admin.site.register(BattleHistory)

# Register your models here.
