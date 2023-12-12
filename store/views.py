from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from .forms import LoginForms, UserForms
from django.contrib.auth import authenticate, login as login_django, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['username']
            senha = form.cleaned_data['password']
            user = authenticate(request, username=usuario, password=senha)
            if user is not None:
                login_django(request, user)
                messages.success(request, 'Logado com sucesso!')
                return redirect('/')
            else:
                messages.error(request, 'Usuário ou senha inválido(s)!')
                return redirect(request.path)
    else:
        form = LoginForms()
    if not request.user.is_authenticated:
        return render(
            request, 'store/pages/login.html', context={
            'name': 'login',
            'form': form,
            }
        )
    else:
        return redirect('/')
			
@csrf_exempt
def usuario_cadastro(request):
    if request.method == "POST":
        form = UserForms(request.POST)
        if form.is_valid():
            # Extract user data from the form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create a new User instance with email as username
            user = form.save(commit=False)
            user.username = email  # Set email as username
            user.set_password(password)
            user.save()

            # Create a Customer instance associated with the new User
            customer = Customer.objects.create(user=user, name=user.first_name, email=email, senha=password)

            return redirect('/login')
        messages.warning(request, 'Preencha corretamente os campos!')
    else:
        form = UserForms()
	
    if not request.user.is_authenticated:
        return render(
            request, 'store/pages/cadastro.html', context={
            'name': 'usuario_cadastro',
            'form': form
            }
        )
    else:
        return redirect('/')
    
def sair(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login')
	
@login_required()
def store(request):
    
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

@login_required()
def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

@login_required()
def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

@login_required()
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
 
	if action == 'add':
		if orderItem.quantity < product.estoque:
			orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

@login_required()
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	try:
		order_items = OrderItem.objects.filter(order=order)

		for orderItem in order_items:
			product = Product.objects.get(pk=orderItem.product.id)
			if product.estoque >= orderItem.quantity:
				product.estoque = product.estoque - orderItem.quantity
				product.save()
			else:
				raise ValidationError('Sem estoque')

	except OrderItem.DoesNotExist:
		raise ValidationError('Nenhum item de pedido encontrado para o pedido.')

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)
  
	return JsonResponse('Payment submitted..', safe=False)
