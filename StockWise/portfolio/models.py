from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import views
class myportfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_purchased = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = ("myportfolio")
        verbose_name_plural = ("myportfolios")

    def __str__(self):
        return self.stock_symbol

    def get_absolute_url(self):
        return reverse("myportfolio_detail", kwargs={"pk": self.pk})

    def __init__(self, user):
        self.user = user
        self.portfolio = views.get_consolidated_portfolio(user)
        return self.portfolio