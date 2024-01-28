from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from .models import *


class LoginView(View):
    def get(self,request):
        return render(request,"login.html")

    def post(self,request):
        user = authenticate(
            username = request.POST.get('username'),
            password = request.POST.get('password')
        )
        if user is None:
            return redirect('login')
        login(request,user)
        return redirect('main')


class RegisterView(View):
    def get(self,request):
        return render(request,"register.html")

    def post(self,request):
        if request.POST.get('password') == request.POST.get('password2'):
            u = User.objects.create_user(
                username= request.POST.get('username'),
                password= request.POST.get('password')
            )
            um = UserModel.objects.create(
                ism = request.POST['ism'],
                fam = request.POST['familya'],
                user = u
            )
            Savat.objects.create(
                account = um,
            )
            return redirect('login')



class IndexView(View):
    def get(self,request):
        if request.user.is_authenticated:
            content = {
                "banner_mahsulotlar":BannerMahsulot.objects.all(),
                "mahsulotlar":Mahsulot.objects.all(),
                "savat_count":len(Savatitem.objects.filter(savat__account__user=request.user)),
                "like_count":len(Like.objects.filter(account__user=request.user)),
                "bolimlar":Bolim.objects.all()
            }
            print(len(Savatitem.objects.filter(savat__account__user=request.user)))
            return render(request, 'index.html', content)
        else:
            content = {
                "banner_mahsulotlar": BannerMahsulot.objects.all(),
                "mahsulotlar": Mahsulot.objects.all(),
                "bolimlar": Bolim.objects.all()
            }
            return render(request, 'index_not_reg.html', content)



class ContactView(View):
    def get(self,request):
        if request.user.is_authenticated:
            content = {
                "like_count": len(Like.objects.filter(account__user=request.user)),
                "savat_count": len(Savatitem.objects.filter(savat__account__user=request.user))
            }
            return render(request, 'contact.html', content)
        else:
            return render(request, 'contact_not_reg.html')


class CartView(View):
    def get(self,request):
        if request.user.is_authenticated:
            savat_itemlar = Savatitem.objects.filter(savat__account__user=request.user)
            umumiy_summa = 0
            for i in savat_itemlar:
                 umumiy_summa += i.mahsulot.narx * i.miqdor
            content = {
                "savat_itemlar":savat_itemlar,
                "umumiy_summa": umumiy_summa,
                "like_count": len(Like.objects.filter(account__user=request.user))
            }
            return render(request, 'cart.html', content)
        else:
            return redirect('login')


class DetailView(View):
    def get(self,request,pk):
        if request.user.is_authenticated:
            mahsulot = Mahsulot.objects.get(id=pk)
            if mahsulot:
                content = {"mahsulot":mahsulot,
                           "banner_mahsulotlar":BannerMahsulot.objects.all(),
                           "like_count": len(Like.objects.filter(account__user=request.user)),
                           "savat_count": len(Savatitem.objects.filter(savat__account__user=request.user)),
                           "mahsulot_like_count":len(Like.objects.filter(mahsulot=mahsulot))
                           }
                return render(request,'detail.html',content)
            return redirect('main')
        else:
            mahsulot = Mahsulot.objects.get(id=pk)
            if mahsulot:
                content = {"mahsulot": mahsulot,
                           "banner_mahsulotlar": BannerMahsulot.objects.all(),
                           "mahsulot_like_count": len(Like.objects.filter(mahsulot=mahsulot))
                           }
                return render(request, 'detail_not_reg.html', content)
            return redirect('main')



class LikesListView(View):
    def get(self,request):
        mahsulotlar = Like.objects.filter(account__user=request.user)
        if mahsulotlar:
            content = {
                "likemahsulotlar":mahsulotlar,
                "savat_count": len(Savatitem.objects.filter(savat__account__user=request.user))
            }
            return render(request, 'likes.html', content)
        content = {
            "not_mahsulotlar":True
        }
        return render(request, 'likes.html', content)


class LikeView(View):
    def get(self,request,pk):
        key = Like.objects.filter(account__user=request.user, mahsulot__id=pk)
        if not key:
            Like.objects.create(
                account = UserModel.objects.get(user=request.user),
                mahsulot = Mahsulot.objects.get(id=pk)
            )
            return redirect('/yoqganlar/')
        Like.objects.get(mahsulot__id=pk).delete()
        return redirect('/yoqganlar/')


class ItemPlusView(View):
    def get(self,request,pk):
        savat_item = Savatitem.objects.get(id=pk)
        savat_item.miqdor += 1
        savat_item.summa += savat_item.mahsulot.narx
        savat_item.save()
        return redirect('/savat/')


class ItemMinusView(View):
    def get(self,request,pk):
        savat_item = Savatitem.objects.get(id=pk)
        if savat_item.miqdor > 1:
            savat_item.miqdor -= 1
            savat_item.summa -= savat_item.mahsulot.narx
            savat_item.save()
        return redirect('/savat/')




class BolimView(View):
    def get(self,request,pk):
        if request.user.is_authenticated:
            kitoblar = Mahsulot.objects.filter(bolim=pk)
            content = {
                "mahsulotlar":kitoblar,
                "savat_count":len(Savatitem.objects.filter(savat__account__user=request.user)),
                "like_count":len(Like.objects.filter(account__user=request.user)),
                "bolimlar":Bolim.objects.all()
            }
            return render(request, 'filter_mahsulot.html', content)
        else:
            kitoblar = Mahsulot.objects.filter(bolim=pk)
            content = {
                "mahsulotlar": kitoblar,
                "bolimlar": Bolim.objects.all()
            }
            return render(request, 'filter_mahsulot_not_reg.html', content)


class SavatItemPlusView(View):
    def get(self,request,pk):
        if request.user.is_authenticated:
            mahsulot = Mahsulot.objects.get(id=pk)
            if mahsulot:
                Savatitem.objects.create(
                    savat = Savat.objects.get(account__user=request.user),
                    mahsulot = mahsulot,
                    miqdor = 1,
                    summa = mahsulot.narx
                )
                return redirect('savat')

class SavatItemMinusView(View):
    def get(self,request,pk):
        if request.user.is_authenticated:
            Savatitem.objects.get(id=pk, savat__account__user=request.user).delete()
            return redirect('savat')






