from django.contrib import admin
import app.models

# Register your models here.

admin.site.register(app.models.Category)
admin.site.register(app.models.Foundation)
admin.site.register(app.models.GiveAway)
admin.site.register(app.models.Gathering)
admin.site.register(app.models.Delivery)
admin.site.register(app.models.AdditionalInfo)
admin.site.register(app.models.SiteUser)
