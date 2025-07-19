from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, ProductImage, Chat, Message, User
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db import IntegrityError
import os
from django.db.models import Max
from django.db.models import Prefetch

def index(request):
    list(messages.get_messages(request))
    query = request.GET.get('q')
    if query:
        all_products = Product.objects.filter(
            Q(title__icontains=query) | Q(brand__icontains=query) | Q(description__icontains=query)
        ).order_by("-timestamp")
    else:
        all_products = Product.objects.all().order_by("-timestamp")
    paginator = Paginator(all_products, 9)
    page_number = request.GET.get('page')
    products_of_the_page = paginator.get_page(page_number)
    return render(request, "pileh/index.html", {
        "products_of_the_page": products_of_the_page
    })

def product_detail(request, product_id):
    list(messages.get_messages(request))
    product = get_object_or_404(Product, pk=product_id)
    all_products_ordered = Product.objects.all().order_by("-timestamp")
    product_ids = list(all_products_ordered.values_list('id', flat=True))
    try:
        current_product_index = product_ids.index(product.id)
    except ValueError:
        current_product_index = -1
    next_product_id = None
    previous_product_id = None
    if current_product_index != -1:
        if current_product_index > 0:
            previous_product_id = product_ids[current_product_index - 1]
        if current_product_index < len(product_ids) - 1:
            next_product_id = product_ids[current_product_index + 1]
    return render(request, "pileh/product_detail.html", {
        "product": product,
        "previous_product_id": previous_product_id,
        "next_product_id": next_product_id,
    })

@login_required
def profile_view(request, user_id):
    list(messages.get_messages(request))
    user_profile = get_object_or_404(User, pk=user_id)
    user_products = Product.objects.filter(user=user_profile).order_by("-timestamp")
    paginator = Paginator(user_products, 9)
    page_number = request.GET.get('page')
    products_of_the_page = paginator.get_page(page_number)
    return render(request, "pileh/profile.html", {
        "user_profile": user_profile,
        "products_of_the_page": products_of_the_page,
    })

@login_required
def messages_view(request):
    list(messages.get_messages(request))
    all_chats = Chat.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).annotate(
        last_message_timestamp=Max('messages__timestamp')
    ).order_by('-last_message_timestamp')
    chats_info = []
    for chat in all_chats:
        other_user = chat.buyer if chat.seller == request.user else chat.seller
        last_message = chat.messages.order_by('-timestamp').first()
        chats_info.append({
            'chat_id': chat.id,
            'other_user': other_user,
            'product_title': chat.product.title,
            'last_message': last_message
        })
    return render(request, "pileh/messages.html", {
        "chats": chats_info
    })

def get_product_data(request):
    list(messages.get_messages(request))
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'product_data.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    return JsonResponse(data)

@login_required
def add_product(request):
    list(messages.get_messages(request))
    if request.method == "POST":
        title = request.POST.get('title')
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        storage = request.POST.get('storage')
        sim_card_status = request.POST.get('sim_card_status')
        color = request.POST.get('color')
        description = request.POST.get('description')
        price = request.POST.get('price')
        if not all([title, brand, model, storage, sim_card_status, color, description, price]):
            messages.error(request, 'Please fill in all fields.')
            return redirect('add_product')
        try:
            new_product = Product.objects.create(
                user=request.user,
                title=title,
                brand=brand,
                model=model,
                storage=storage,
                color=color,
                sim_card_status=sim_card_status,
                description=description,
                price=price
            )
            uploaded_images = request.FILES.getlist('images')
            for img in uploaded_images[:5]:
                ProductImage.objects.create(product=new_product, image=img)
            return redirect('index')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return redirect('add_product')
    return render(request, "pileh/new_product.html")

@login_required
def start_chat(request, product_id):
    list(messages.get_messages(request))
    product = get_object_or_404(Product, pk=product_id)
    if request.user == product.user:
        messages.error(request, "You cannot start a chat with yourself.")
        return redirect('product_detail', product_id=product_id)
    chat = Chat.objects.filter(
        Q(product=product),
        Q(seller=product.user, buyer=request.user) | Q(seller=request.user, buyer=product.user)
    ).first()
    if not chat:
        return redirect('chat_initiate_view', product_id=product.id, seller_id=product.user.id, buyer_id=request.user.id)
    else:
        return redirect('chat_view', chat_id=chat.id)

@login_required
def chat_view(request, chat_id=None, product_id=None, seller_id=None, buyer_id=None):
    list(messages.get_messages(request))
    chat = None
    product_obj = None
    seller_obj = None
    buyer_obj = None
    if chat_id is not None:
        chat = get_object_or_404(Chat, pk=chat_id)
        product_obj = chat.product
        seller_obj = chat.seller
        buyer_obj = chat.buyer
    else:
        if product_id and seller_id and buyer_id:
            product_obj = get_object_or_404(Product, pk=product_id)
            seller_obj = get_object_or_404(User, pk=seller_id)
            buyer_obj = get_object_or_404(User, pk=buyer_id)
        else:
            return redirect('index')
    if request.user not in [seller_obj, buyer_obj]:
        return redirect('index')
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            if chat is None:
                chat, created = Chat.objects.get_or_create(
                    product=product_obj,
                    seller=seller_obj,
                    buyer=buyer_obj
                )
            Message.objects.create(
                chat=chat,
                sender=request.user,
                content=content
            )
            return redirect('chat_view', chat_id=chat.id)
    messages_in_chat = []
    if chat:
        messages_in_chat = chat.messages.all()
    return render(request, "pileh/chat.html", {
        "chat": chat,
        "product": product_obj,
        "messages": messages_in_chat,
        "chat_id_from_url": chat_id
    })

@login_required
@require_POST
def edit_product(request, product_id):
    list(messages.get_messages(request))
    product = get_object_or_404(Product, pk=product_id)
    if product.user != request.user:
        return JsonResponse({"error": "You are not authorized to edit this product."}, 403)
    data = json.loads(request.body)
    product.title = data.get("title", product.title)
    product.brand = data.get("brand", product.brand)
    product.model = data.get("model", product.model)
    product.storage = data.get("storage", product.storage)
    product.sim_card_status = data.get("sim_card_status", product.sim_card_status)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.save()
    return JsonResponse({
        "message": "Product updated successfully.",
        "title": product.title,
        "description": product.description,
        "price": str(product.price)
    })

@login_required
@require_POST
def delete_product(request, product_id):
    list(messages.get_messages(request))
    try:
        product = get_object_or_404(Product, pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found."}, 404)
    if product.user != request.user:
        return JsonResponse({"error": "You are not authorized to delete this product."}, 403)
    product.delete()
    return JsonResponse({"message": "Product deleted successfully."})

@login_required
@require_POST
def delete_chat(request, chat_id):
    list(messages.get_messages(request))
    chat = get_object_or_404(Chat, pk=chat_id)
    if request.user not in [chat.seller, chat.buyer]:
        return JsonResponse({"error": "You are not authorized to delete this chat."}, 403)
    chat.delete()
    return redirect('messages')

@login_required
@require_POST
def delete_message(request, message_id):
    list(messages.get_messages(request))
    message = get_object_or_404(Message, pk=message_id)
    if message.sender != request.user:
        return JsonResponse({"error": "You are not authorized to delete this message."}, 403)
    chat_id = message.chat.id
    message.delete()
    return redirect('chat_view', chat_id=chat_id)

@login_required
@require_POST
def mark_as_sold(request, product_id):
    list(messages.get_messages(request))
    product = get_object_or_404(Product, pk=product_id)
    if product.user != request.user:
        return JsonResponse({"error": "You are not authorized to perform this action."}, 403)
    product.is_sold = not product.is_sold
    product.save()
    return JsonResponse({
        "message": "Product status updated successfully.",
        "is_sold": product.is_sold
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            list(messages.get_messages(request))
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "pileh/login.html", {
                "message": "Invalid username and/or password.",
                "current_view": "login"
            })
    else:
        list(messages.get_messages(request))
        return render(request, "pileh/login.html", {
            "current_view": "login"
        })

def logout_view(request):
    list(messages.get_messages(request))
    logout(request)
    return redirect('index')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return render(request, "pileh/register.html", {
                "message": "Passwords must match.",
                "current_view": "register"
            })
        try:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "pileh/register.html", {
                "message": "Username already taken.",
                "current_view": "register"
            })
        list(messages.get_messages(request))
        login(request, user)
        return redirect('index')
    else:
        list(messages.get_messages(request))
        return render(request, "pileh/register.html", {
            "current_view": "register"
        })