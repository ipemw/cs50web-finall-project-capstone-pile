from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='pileh_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='pileh_users_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    storage = models.CharField(max_length=20)
    color = models.CharField(max_length=50, default="Not Specified")
    sim_card_status = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='product_images/')

class Chat(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="chats")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_chats")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_chats")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('product', 'seller', 'buyer')

    def __str__(self):
        return f"Chat for product '{self.product.title}' between {self.seller.username} and {self.buyer.username}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"Message from {self.sender.username} in chat {self.chat.id}"