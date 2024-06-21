from django.shortcuts import render,redirect
from .models import pet,customer,cart,order,payment,orderdetail
from django.views.generic import DateDetailView,ListView,CreateView,DetailView
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password
from datetime import date
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class petview(ListView):
    model=pet
    template_name='petview.html'
    context_object_name='petobj'

    def get_context_data(self, **kwargs):
        data = self.request.session['sessionvalue']
        context = super().get_context_data(**kwargs)
        context['session'] = data
        return context
    

def search(request):
    if request.method=="POST":
        searchdata=request.POST.get('searchquery')
        petobj=pet.objects.filter(Q(name__icontains=searchdata)|(Q(breed__icontains=searchdata)) | (Q(species__icontains=searchdata)))
        return render(request,'petview.html',{'petobj':petobj})
    
def register(request):
    if request.method=="GET":
        return render(request,'register.html')
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phoneno=request.POST.get('phoneno')
        password=request.POST.get('password')
        epassword=make_password(password)

        cutobj=customer(name=name,email=email,phoneno=phoneno,password=epassword)
        cutobj.save()
        return redirect('../login/')


def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    elif request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        cust = customer.objects.filter(email=username)
        if cust:
            custobj = customer.objects.get(email=username)

            flag = check_password(password,custobj.password)

            if flag:
                request.session['sessionvalue']=  custobj.email
                return redirect('../petview/')
            else:
                return render(request,'login.html',{'msg':'Incorrect username and Password'})
            
        else:
            return render(request,'login.html',{'msg':'Incorrect username and Password'})
        
class petdetail(DetailView):
    model=pet
    template_name="petdetail.html"
    context_object_name="i"    

def addtocart(request):
    productid = request.POST.get('prouctid')
    print(productid)
    custsession = request.session['sessionvalue'] #email of customer
    custobj = customer.objects.get(email = custsession) #fetch record from database table using email
    custid = custobj.id #fetch customer id using customer object
    # pobj = pet.objects.get(id = productid)
    pobj = pet.objects.get(id = productid)

    flag = cart.objects.filter(cid = custobj.id,pid = pobj.id)
    if flag:
        cartobj = cart.objects.get(cid = custobj.id,pid = pobj.id)
        cartobj.quantity = cartobj.quantity +1
        cartobj.totalamount = pobj.price * cartobj.quantity
        cartobj.save()
    else:
        cartobj = cart(cid = custobj,pid = pobj,quantity = 1,totalamount = pobj.price*1)
        cartobj.save()

    return redirect('../petview/')


def viewcart(request):
    custsession = request.session['sessionvalue'] #email of customer
    custobj = customer.objects.get(email = custsession) 
    cartobj = cart.objects.filter(cid = custobj.id)

    return render(request,'cart.html',{'cartobj':cartobj,'session':custsession })

def cq(request):
    cemail =request.session['sessionvalue']
    pid=request.POST.get('pid')
    custobj=customer.objects.get(email=cemail)
    pobj=pet.objects.get(id=pid)
    cartobj=cart.objects.get(cid=custobj.id,pid=pobj.id)

    if request.POST.get('changequantitybutton')=='+':
        cartobj.quantity=cartobj.quantity+1
        cartobj.totalamount=cartobj.quantity*pobj.price
        cartobj.save()

    elif request.POST.get('changequantitybutton')=='-':
        print("inside- quantity")
        if cartobj.quantity==1:
            cartobj.delete()
        else:
            cartobj.quantity=cartobj.quantity-1
            cartobj.totalamount=cartobj.quantity*pobj.price
            cartobj.save()

    return redirect('../viewcart/')

def summary(request):
    custsession=request.session['sessionvalue']
    custobj=customer.objects.get(email=custsession)
    cartobj=cart.objects.filter(cid=custobj.id)
    totalbill=0
    for i in cartobj:
        totalbill=i.totalamount+totalbill
    return render(request,'summary.html',{'session':custsession,'cartobj':cartobj,'totalbill':totalbill})

def placeorder(request):
    fn=request.POST.get('fn')
    ln=request.POST.get('ln')
    phoneno=request.POST.get('phoneno')
    address=request.POST.get('address')
    city=request.POST.get('city')
    state=request.POST.get('state')
    pincode=request.POST.get('pincode')
   

    datev=date.today()
    print(datev)
    orderobj=order(firstname=fn,lastname=ln,phoneno=phoneno,address=address,city=city,state=state,pincode=pincode,orderstatus='pending',orderdate=datev)
    orderobj.save()
    

    ono=str(orderobj.id)+str(datev).replace('-','')
    orderobj.ordernumber=ono
    orderobj.save()

    custsession=request.session['sessionvalue']
    custobj=customer.objects.get(email=custsession)
    cartobj=cart.objects.filter(cid=custobj.id)

    totalbill = 0 
    for i in cartobj:
        totalbill=i.totalamount+totalbill


    sm=EmailMessage('order placed','order placed frompet store application.Total bill for your order is'+str(totalbill),to=['sakpalpurva4@gmail.com'])
    sm.send()
    return render(request,'payment.html',{'orderobj':orderobj,'session':custsession,'cartobj':cartobj,'totalbill':totalbill})


# def order_success(request):
#     custsession = request.session['sessionvalue']
#     custobj = customer.objects.get(email=custsession)
#     cartobj = cart.objects.filter(cid=custobj.id)

#     # Update order status
#     last_order = order.objects.filter(
#         firstname=request.POST.get('fn'),
#         lastname=request.POST.get('ln'),
#         phoneno=request.POST.get('phoneno'),
#         address=request.POST.get('address'),
#         city=request.POST.get('city'),
#         state=request.POST.get('state'),
#         pincode=request.POST.get('pincode'),
#     ).order_by('-id').first()
#     last_order.orderstatus = 'completed'
#     last_order.save()

#     # Clear the cart after successful order
#     cartobj.delete()

#     return render(request, 'success.html', {'session': custsession, 'orderobj': last_order})

def order_detail(request):
    custsession = request.session['sessionvalue']
    custobj = customer.objects.get(email=custsession)
    orders = order.objects.filter(firstname=custobj.name)

    return render(request, 'orderdetail.html', {'session': custsession, 'orders': orders})


def paymentsuccess(request):
    ono = request.GET.get('order_id')
    tid = request.GET.get('payment_id')
    request.session['sessionvalue']=request.GET.get('session')
    custsession=request.session['sessionvalue']
    custobj=customer.objects.get(email=custsession)
    cartobj=cart.objects.filter(cid=custobj.id)
    orderobj=order.objects.get(ordernumber=ono)
    
    paymentobj=payment()
    paymentobj.customerid = custobj
    paymentobj.oid = orderobj
    paymentobj.paymentstatus = "paid"
    paymentobj.transactionid = tid
    paymentobj.paymentmode ="razorpay"
    paymentobj.save()

    for i in cartobj:
        orderobj=orderdetail(ordernumber=ono,customerid=custobj,productid=i.pid,quantity=i.quantity,totalprice=i.totalamount,paymentid=paymentobj)
        orderdetail.save()
        i.delete()

    return render(request,'s1.html',)

def petviewcmfun(request,data):
    
    petdetails = pet.cpetobj.getdata(data)
    print(petdetails)
    return render(request,'PetView.html',{'petobj':petdetails})

def logout(request):
    del(request.session['sessionvalue'])
    return redirect('../login/')



