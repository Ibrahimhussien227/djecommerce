from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.utils import timezone
from .forms import *
from .models import *


def handler_404(request, exception):
    return render(request, '404/404.html')


def products(request):
    context = {
        'item': Item.objects.all(),
    }
    return render(request, "product.html", context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get()
        context = {
            'form': form,
            'object': order
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('mystore:checkout')
            messages.warning(self.request, "Failed Checkout")
            return redirect('mystore:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("mystore:order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'object': order,
        }
        return render(self.request, "payment.html", context)


class HomeView(ListView):
    model = Item
    # for 6 item in one page
    paginate_by = 6
    ordering = ['category']
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['comment'] = CommentForm()
        context['comments'] = Comment.objects.filter(item=self.object)
        return context

    def post(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        form = CommentForm(request.POST)

        if form.is_valid():
            content = request.POST.get('comment')
            comment = Comment.objects.create(item=item, user=request.user, comment=content)
            comment.save()

            return redirect('mystore:product', slug)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("mystore:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("mystore:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("mystore:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("mystore:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("mystore:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("mystore:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("mystore:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("mystore:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("mystore:product", slug=slug)


@login_required
def delete_item(request, slug):
    if request.user.is_superuser:
        Item.objects.get(slug=slug).delete()
    return redirect('mystore:home')


def edit_item(request, slug):
    item = Item.objects.get(slug=slug)
    if request.method == 'POST':
        p_form = ItemUpdateForm(request.POST, request.FILES, instance=item)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'The product has been updated')
            return redirect("mystore:product", slug=slug)
    else:
        p_form = ItemUpdateForm(instance=item)
    context = {
        'p_form': p_form,
        'item': item
    }
    return render(request, 'edit_item.html', context)


def add_item(request):
    add_item = AddItemForm()
    if request.method == 'POST':
        add_item = AddItemForm(request.POST, request.FILES)
        if add_item.is_valid():
            add_item.save()
            return redirect('mystore:home')
    context = {'add_item': add_item}
    return render(request, 'add_item.html', context)


def room(request, room_name):
    return render(request, 'chatroom.html', {
        'room_name': room_name
    })
