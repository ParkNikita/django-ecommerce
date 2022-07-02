import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from . import models
from . import forms
# Create your views here.

class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = forms.CustomUserCreationForm
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        customer = models.Customer.objects.create(
            name = user.username,
            user = user,
            email = user.email
        )  
        return super(SignUpView, self).form_valid(form)

    def get_success_url(self):
        return reverse('login')    


class IndexView(ListView):
    template_name = 'store/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return models.Product.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                order = models.Order.objects.get(customer = self.request.user.customer)
                orderitems = order.orderitem_set.all()
                queryset = [orderitem.product.name for orderitem in orderitems]
            except:
                queryset = []
            context.update({
                'cart': queryset
            })
            return context
        else:
            return context


class ProductDetail(DetailView):
    template_name = 'store/product_detail.html'
    model = models.Product
    context_object_name = 'product'


class CartView(LoginRequiredMixin, ListView):
    login_url = '/login'
    template_name = 'store/cart.html'
    context_object_name = 'order'

    def get_queryset(self):
        try:
            order = models.Order.objects.get(customer=self.request.user.customer, complete=False)

        except(KeyError, models.Order.DoesNotExist):
            order = models.Order.objects.create(customer=self.request.user.customer)

        return order
        

class CheckOutView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    template_name = 'store/checkout.html'
    form_class = forms.DeliveryCreationForm

    def get_context_data(self, **kwargs):
        context = super(CheckOutView, self).get_context_data(**kwargs)
        order = models.Order.objects.get(customer=self.request.user.customer, complete=False)
        context.update({
            'order': order
        })
        return context

    def form_valid(self, form):
        order = models.Order.objects.get(customer=self.request.user.customer, complete=False)
        delivery_address = form.save(commit=False)
        delivery_address.customer = self.request.user.customer
        delivery_address.order = order
        delivery_address.save()

        order.complete = True
        order.transaction_id = datetime.datetime.now().timestamp()
        order.save()
        return super(CheckOutView, self).form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('store:index')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = models.Product.objects.get(id=productId)
    order, created = models.Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = models.OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse(f'item was {action}', safe=False)




        

