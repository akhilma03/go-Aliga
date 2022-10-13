from importlib.resources import Package
import json
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response
from trips.models import Packages
from .models import Order,PassengerDetails
from .serializers import OrderSerializer,AddressSerializer
from django.conf import settings
from rest_framework import generics
from django.shortcuts import render
from .forms import OrderForm
from trips.models import DateBooking


# you have to create .env file in same folder where you are using environ.Env()
# reading .env file which located in api folder

@api_view(['POST'])
def DetailsPassenger(request):
    data = request.data
    details = PassengerDetails.objects.create(
        user = request.user,
        name = data['name'],
        address=data['address'],
        city = data['city'],
        pincode=data['pincode'])
    serializer = AddressSerializer(details,many=True)
    return Response(serializer.data)



@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    amount = request.data['amount']
    name = request.data['name']
    address = request.data['address'] 
    slot = request.data['slot']

    # setup razorpay client this is the client to whome user is paying money that's you
    client = razorpay.Client(auth=(settings.RAZORPAY_PUBLIC_KEY,settings.RAZORPAY__SECRET_KEY))
    # create razorpay orderpees.
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    # we are saving an order with isPaid=False because we've just initialized the order
    # we haven't received the money we will handle the payment succes in next 
    # function
    order = Order.objects.create(order_package_id=name, 
                                 order_amount=amount, 
                                 order_payment_id=payment['id'],
                                 slot=slot,
                                 address=address)

    serializer = OrderSerializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)


@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    res = request.data['response']

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Order.objects.get(order_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client =razorpay.Client(auth=(settings.RAZORPAY_PUBLIC_KEY,settings.RAZORPAY__SECRET_KEY))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is  None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    id=request.data['id']
    slot = request.data['slot']
    package = Package.object.get(id=id)
    package.stock-=1
    package.save()
    Booking = DateBooking.objects.get(id=slot)
    Booking.isbooked=True
    Booking.count-=1
    Booking.save()
    order.isPaid = True
    order.order_status='Approved'
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)


#fggfd
def temp_payment(request):
    payment =0
    order=0
    if request.method == 'POST':
        amount = request.POST.get('amount')
        name = request.POST['name']
        request.session['key'] = name
        print(name)

        client =razorpay.Client(auth=(settings.RAZORPAY_PUBLIC_KEY,settings.RAZORPAY__SECRET_KEY))
        payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})
      
        # user = request.user
        order = Order.objects.create(order_package_id=name, 
                                 order_amount=amount, 
                                #  user=user,
                                 order_id=payment['id'])
        payment['name']=name      
        print(order)                                          

    return render(request,'paymentz.html',{'payment':payment,'order':order})


def paymentstatus(request):
    status =None
    response = request.POST
    # id = request.data['id']
    # print(id)

    print("ddd",response)

    params_dict = {
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }

    client =razorpay.Client(auth=(settings.RAZORPAY_PUBLIC_KEY,settings.RAZORPAY__SECRET_KEY))

   
    status = client.utility.verify_payment_signature(params_dict)
    print(status,'ghg')
    try:
        order = Order.objects.get(order_id=response['razorpay_order_id'])
        order.order_payment_id  = response['razorpay_payment_id']
            
        order.isPaid = True
        order.order_status='Approved'
        order.save()

        name = request.session['key']
        package = Packages.objects.get(id=name)
        print(package)
        package.stock -=1
        package.save()

        print(name,111112)
        #df
        return render(request,'success.html',{'status':True})
    except:
        return render(request,'success.html',{'status':False})

 # request.data is coming from frontend
    # amount = request.data['amount']
    # name = request.data['name']

    # setup razorpay client this is the client to whome user is paying money that's you
    # client = razorpay.Client(auth=(settings.RAZORPAY_PUBLIC_KEY,settings.RAZORPAY__SECRET_KEY))
    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.
    

    # we are saving an order with isPaid=False because we've just initialized the order
    # we haven't received the money we will handle the payment succes in next 
    # function


    # serializer = OrderSerializer(order)

    # """order response will be 
    # {'id': 17, 
    # 'order_date': '23 January 2021 03:28 PM', 
    # 'order_product': '**product name from frontend**', 
    # 'order_amount': '**product amount from frontend**', 
    # 'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    # 'isPaid': False}"""

    # data = {
    #     "payment": payment,
    #     "order": serializer.data
    # }    


    