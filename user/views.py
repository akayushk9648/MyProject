from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from datetime import datetime
from django.db import connection
# Create your views here.


def index(request):
    data = category.objects.all().order_by('id')
    slider_data=slider.objects.all().order_by('-id')[0:3]
    latest_product = myproduct.objects.all()
    deal = myproduct.objects.all().filter(total_discount__gte=30)
    mydict = {
        "cdata": data, 'sdata': slider_data, "ldata": latest_product, "offerdata": deal
    }
    return render(request, 'user/index.html', mydict)


def aboutus(request):
    return render(request, 'user/aboutus.html')


def contact(request):
    if (request.method == "POST"):
        a1 = request.POST.get('query')
        a2 = request.POST.get('name')
        a3 = request.POST.get('email')
        a4 = request.POST.get('mobile')
        a5 = request.POST.get('message')
        X = contactus(Query=a1, Name=a2, Email=a3,
                      Mobile=a4, Message=a5).save()
        return (HttpResponse("<script> location.href='/user/thank'</script>"))

    return render(request, 'user/contactus.html')

def indexcart(request):
    user = request.session.get('user')
    if user:
        qt =int(request.GET.get('qt'))
        pname = request.GET.get('pname')
        ppic = request.GET.get('ppic')
        pw = request.GET.get('pw')
        price = request.GET.get('price')
        total_price = qt*int(price)
        if qt > 0:
            cart(userid=user, product_name=pname, quantity=qt, price=price, total_price=total_price,
                 product_picture=ppic, pw=pw, added_date=datetime.now().date()).save()
            cartitem = cart.objects.filter(userid=user).count()
            request.session['cartitem'] = cartitem
            return HttpResponse("<script>alert('your item is added in cart'); location.href='/user/index/'</script>")
        else:
            return HttpResponse("<script>alert('Please Increase your card item');location.href='/user/index/'</script>")

    return render(request,'user/indexcart.html')
def thank(request):
    return render(request, 'user/thankcon.html')



def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')  
        password = request.POST.get('password')
        x = register.objects.filter(email=email, password=password)
        if x.count() == 1:

            request.session['user'] = email
            request.session['userpic'] = str(x[0].profile)
            request.session['username'] = str(x[0].name)
            user=request.session.get('user')
            cartitem = cart.objects.filter(userid=user).count()
            request.session['cartitem'] = cartitem
            return HttpResponse("<script>location.href='/user/signin/'</script>")
        else:
            return HttpResponse("<script>location.href='/user/signin/'</script>")

    return render(request, 'user/signin.html')


def signout(request):
    if request.session.get('user'):
        del request.session['user']
        del request.session['userpic']
        return HttpResponse("<script>location.href='/user/index'</script>")
    return render(request, 'user/signin.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        profile = request.FILES['profile']
        add = request.POST.get("address")
        x = register.objects.all().filter(email=email).count()
        if x == 1:
            return HttpResponse("<script>location.href='/user/registered'</script>")
        else:
            register(name=name, mobile=mobile, email=email,
                     password=password, address=add, profile=profile).save()
            return HttpResponse("<script> location.href='/user/successreg'</script>")
    return render(request, 'user/signup.html')


def successreg(request):

    return render(request, 'user/successreg.html')


def already(request):

    return render(request, 'user/already.html')


def product(request):
    catid = request.GET.get('cid')
    subcatid = request.GET.get('sid')
    subcategory_name = subcategory.objects.all().order_by("-id")

    if subcatid is not None:
        prod = myproduct.objects.all().filter(subcategory_name=subcatid)
    elif catid is not None:
        prod = myproduct.objects.all().filter(product_category=catid)
    else:
        prod = myproduct.objects.all().order_by('-id')
    cat = {
        "scat": subcategory_name, "ldata": prod
    }
    return render(request, 'user/product.html', cat)


def myprofile(request):
    user = request.session.get('user')
    rdata = ""
    if request.method == 'POST':
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        profile = request.FILES['profile']

        add = request.POST.get("address")
        register(name=name, email=user, mobile=mobile, address=add,
                 password=password, profile=profile).save()
        return HttpResponse("<script>location.href='/user/profupdate'</script>")
    if user:
        rdata = register.objects.filter(email=user)
    md = {
        "rdata": rdata
    }
    return render(request, 'user/myprofile.html', md)


def profupdate(request):
    return render(request, 'user/profupdate.html')



def orders(request,cursor=None):
    user=request.session.get('user')
    msg=request.GET.get('msg')
    oid=request.GET.get('oid')
    orderdata=""
    if msg is not None:
        cursor=connection.cursor()
        cursor.execute(r"insert into user_myorders(product_name,quantity,price,total_price,product_picture,pw,userid,status, order_date) select product_name,quantity,price,total_price,product_picture,pw,'"+str(user)+"','Pending','"+str(datetime.now().date())+"' from user_cart where userid='"+str(user)+"'")
        cart.objects.filter(userid=user).delete()
        cartitem=cart.objects.filter(userid=user).count()
        request.session['cartitem']=cartitem
        return HttpResponse('<script>alert("Your order is placed Successfully");location.href="/user/orderitem/"</script>')
    if user:
        pdata=myorders.objects.filter(userid=user,status='Pending')
        ddata=myorders.objects.filter(userid=user,status='Delivered')
        adata=myorders.objects.filter(userid=user,status='Accepted')
        if oid is not None:
            myorders.objects.filter(id=oid).delete()
        md={
        "pdata":pdata,"ddata":ddata,"adata":adata}
    return render(request, 'user/orderitem.html',md)


def mycart(request):
    user = request.session.get('user')
    if user:
        qt =int(request.GET.get('qt'))
        pname = request.GET.get('pname')
        ppic = request.GET.get('ppic')
        pw = request.GET.get('pw')
        discount_price = request.GET.get('price')
        total_price = qt*int(discount_price)
        if qt > 0:
            cart(userid=user, product_name=pname, quantity=qt, price=discount_price, total_price=total_price,
                 product_picture=ppic, pw=pw, added_date=datetime.now().date()).save()
            cartitem = cart.objects.filter(userid=user).count()
            request.session['cartitem'] = cartitem
            return HttpResponse("<script>alert('your item is added in cart'); location.href='/user/product/'</script>")
        else:
            return HttpResponse("<script>alert('Please Increase your card item');location.href='/user/product/'</script>")
    return render(request, 'user/mycart.html')


def cartitem(request):
    user=request.session.get('user')
    cid=request.GET.get('cid')
    cartdata=""
    if user:
        cartdata=cart.objects.filter(userid=user)
        if cid is not None:
            cart.objects.filter(id=cid).delete()
            cartitem = cart.objects.filter(userid=user).count()
            request.session['cartitem'] = cartitem
    md={
        "cartdata":cartdata
    }
    return render(request, 'user/cartitem.html',md)
def mprofile(request):
    return render(request,'user/mprofile.html')