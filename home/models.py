from django.contrib.auth.models import User
from django.db import models

class UserModel(models.Model):
    ism = models.CharField(max_length=20)
    fam = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"ism={self.ism},username={self.user.username}"

class Bolim(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Mahsulot(models.Model):
    nom = models.CharField(max_length=50)
    muallif = models.CharField(max_length=70)
    narx = models.PositiveIntegerField()
    mavjud = models.IntegerField()
    kitob_tili = models.CharField(max_length=50)
    bolim = models.ForeignKey(Bolim, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.nom},{self.bolim}"


class Izoh(models.Model):
    matn = models.CharField(max_length=200)
    account = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    sana = models.DateField(auto_now_add=True)
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.user.username


class Media(models.Model):
    rasm = models.FileField(upload_to="mahsulotlar-media")
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)

    def __str__(self):
        return self.mahsulot.nom


class Like(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)
    account = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.mahsulot.nom

class Savat(models.Model):
    account = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    sana = models.DateField(auto_now_add=True)
    umumiy_summa = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.account.user.username


class Savatitem(models.Model):
    savat = models.ForeignKey(Savat, on_delete=models.CASCADE)
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)
    miqdor = models.PositiveIntegerField()
    summa = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.savat.account.user.username


class BannerMahsulot(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)

    def __str__(self):
        return self.mahsulot.nom






