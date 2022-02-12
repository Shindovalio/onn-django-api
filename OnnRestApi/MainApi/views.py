from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from MainApi.models import *
from MainApi.serializers import *
from rest_framework.decorators import (
    api_view,
    permission_classes,
)

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# GET all products, POST a new product
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def product_list(request):
    if request.method == "GET":
        products = Product.objects.all()

        # Find by search query param
        search = request.GET.get("search", None)
        if search is not None:
            print("Filtering by search")
            products = products.filter(title__icontains=search) or products.filter(
                description__icontains=search
            )

        products_serializer = ProductSerializer(products, many=True)
        return JsonResponse(products_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == "POST":

        product_data = JSONParser().parse(request)
        # Check for valid request bodys
        try:
            if (
                product_data["title"]
                and product_data["price"]
                and product_data["stock"]
                and product_data["description"]
            ):
                # Create the product
                product_serializer = ProductSerializer(data=product_data)
                if product_serializer.is_valid():
                    product_serializer.save()
                    return JsonResponse(
                        product_serializer.data, status=status.HTTP_201_CREATED
                    )
                return JsonResponse(
                    product_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return JsonResponse(
                {"Error": "Incorrect fields."}, status=status.HTTP_400_BAD_REQUEST
            )


# DELETE a product by id
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    # Check if product exists
    try:
        product = Product.objects.get(pk=pk)

    except Product.DoesNotExist:
        return JsonResponse(
            {"message": "The product does not exist."}, status=status.HTTP_404_NOT_FOUND
        )

    # Delete the product
    if request.method == "DELETE":
        product.delete()

        return JsonResponse(
            {"message": "Product was deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )


# POST an order, GET all logged user's orders
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def order_list(request):
    if request.method == "GET":
        orders = Order.objects.all()

        orders_serializer = OrderSerializer(orders, many=True)
        return JsonResponse(orders_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    if request.method == "POST":
        order_data = JSONParser().parse(request)
        # Check for valid request body
        try:
            if order_data["product"] is not None and order_data["address"]:
                # Check if product exists
                try:
                    product = Product.objects.get(pk=order_data["product"])
                except Product.DoesNotExist:
                    return JsonResponse(
                        {"message": "The product does not exist."},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                # Check if product is in stock
                if product.stock > 0:
                    new_data = {"stock": product.stock - 1}
                    product_serializer = ProductSerializer(
                        product, data=new_data, partial=True
                    )
                    order_serializer = OrderSerializer(data=order_data)
                    if order_serializer.is_valid() and product_serializer.is_valid():

                        # Update stock count
                        order_serializer.save()
                        product_serializer.save()
                        return JsonResponse(
                            order_serializer.data, status=status.HTTP_201_CREATED
                        )

                    return JsonResponse(
                        order_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

                return JsonResponse(
                    {"Error": "Product out of stock"},
                    status=status.HTTP_200_OK,
                )

        except:
            return JsonResponse(
                {"Error": "Incorrect fields."}, status=status.HTTP_400_BAD_REQUEST
            )
