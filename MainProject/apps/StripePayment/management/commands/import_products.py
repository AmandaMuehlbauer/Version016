# apps/StripePayment/management/commands/import_products.py
from django.core.management.base import BaseCommand
from StripePayment.models import Product, Price
import stripe
from django.conf import settings


class Command(BaseCommand):
    help = 'Import products and prices from Stripe API into Product and Price models'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Importing products and prices from Stripe API...'))

        # Set your Stripe API key
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Retrieve products from the Stripe API
        products = stripe.Product.list()

        # Save products and prices to the Product and Price models
        for product_data in products.data:
            product, created = Product.objects.get_or_create(
                stripe_product_id=product_data.id,
                defaults={'name': product_data.name}
            )

            # Fetch prices for the product from the Stripe API
            prices = stripe.Price.list(product=product_data.id)

            # Save prices to the Price model
            for price_data in prices.data:
                if price_data.unit_amount_decimal is not None:
                    price, price_created = Price.objects.get_or_create(
                        product=product,
                        stripe_price_id=price_data.id,
                        defaults={'price': float(price_data.unit_amount_decimal) / 100.0}
                    )

                    if not price_created:
                        price.price = float(price_data.unit_amount_decimal) / 100.0
                        price.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully imported price: {price.price} for product: {product.name}'))

            self.stdout.write(self.style.SUCCESS(f'Successfully imported product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Product and price import completed.'))
