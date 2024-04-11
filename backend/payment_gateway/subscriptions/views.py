import requests
from django.shortcuts import render
from django.http import JsonResponse
from .models import Subscription, Customer
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class InitializeTransactionViewSet(ViewSet):
    def create(self, request):
        initialize_url = "https://api.paystack.co/transaction/initialize"
        secret_key = settings.PAYSTACK_PRIVATE_KEY 
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json"
        }
        data = {
            "email": request.data.get('email'),
            "amount": request.data.get('amount'),
        }

        initialise_response = requests.post(initialize_url, headers=headers, json=data)

        if initialise_response.status_code == 200:
            # Transaction initialized 
            initialize_data = initialise_response.json()
            reference = initialize_data.get('data', {}).get('reference')
            if reference:
                return Response({"reference": reference}, status=status.HTTP_200_OK)

        # Transaction initialization failed
        return Response({"error": "Transaction initialization failed", "data": initialise_response.json()}, status=initialise_response.status_code)
    
class SubscriptionViewSet(ViewSet):
    def create(self, request):
        # Verify payment
        verify_url = f"https://api.paystack.co/transaction/verify/{request.data.get('reference')}"
        secret_key = settings.PAYSTACK_PRIVATE_KEY
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json"
        }

        verify_response = requests.get(verify_url, headers=headers)
        if verify_response.status_code == 200:
            # Payment verified successfully
            verify_data = verify_response.json()
            if verify_data.get('data', {}).get('status') == 'success':
                # Payment successful, create subscription
                subscription_url = "https://api.paystack.co/subscription"
                subscription_data = {
                    "customer": request.data.get('customer'),
                    "plan": request.data.get('plan'),
                    "authorization": request.data.get('authorization')
                }
                subscription_response = requests.post(subscription_url, headers=headers, json=subscription_data)

                if subscription_response.status_code == 200:
                    # Subscription created successfully
                    Subscription.objects.create(
                        user=request.user,
                        plan=request.data.get('plan'),
                        amount=request.data.get('amount'),
                        purchased_date=verify_data.get('data', {}).get('transaction_date'),
                        expiry_date=verify_data.get('data', {}).get('authorization', {}).get('expires_at'),
                        status=verify_data.get('data', {}).get('status'),
                        created_by=request.user,
                        last_updated_by=request.user,
                        created_at=verify_data.get('data', {}).get('transaction_date'),
                        last_updated_at=verify_data.get('data', {}).get('transaction_date'),
                    )
                    return Response({"message": "Subscription created successfully"}, status=status.HTTP_200_OK)
                else:
                    # Error creating subscription
                    return Response({"error": "Error creating subscription", "data": subscription_response.json()}, status=subscription_response.status_code)

        # Payment verification failed
        return Response({"error": "Payment verification failed", "data": verify_response.json()}, status=verify_response.status_code)

        # if verify_response.status_code == 200:
        #     # Payment verified successfully
        #     verify_data = verify_response.json()
        #     if verify_data.get('data', {}).get('status') == 'success':
        #         # Payment successful, create subscription
        #         Subscription.objects.create(
        #             user=request.user,
        #             plan=request.data.get('plan'),
        #             amount=request.data.get('amount'),
        #             purchased_date=verify_data.get('data', {}).get('transaction_date'),
        #             expiry_date=verify_data.get('data', {}).get('authorization', {}).get('expires_at')
        #         )
        #         return Response({"message": "Subscription created successfully"}, status=status.HTTP_200_OK)

        # # Payment verification failed
        # return Response({"error": "Payment verification failed", "data": verify_response.json()}, status=verify_response.status_code)
    
    def list(self, request):
        # Endpoint and secret key
        url = "https://api.paystack.co/subscription"
        secret_key = settings.PAYSTACK_PRIVATE_KEY
        
        # Headers
        headers = {
            "Authorization": f"Bearer {secret_key}"
        }
        
        # Make the request to Paystack
        response = requests.get(url, headers=headers)

        # if response.status_code != 200:
        #     return Response(response.json(), status=response.status_code)
        # subscriptions = Subscription.objects.all()
        # # return subscription from paystack and database
        # return Response({
        #     'paystack_subscriptions': response.json(), 
        #     'local_subscriptions': SubscriptionSerializer(subscriptions, many=True).data}, status=status.HTTP_200_OK)
        if response.status_code == 200:
            subscription_data = response.json()
            return Response(subscription_data, status=status.HTTP_200_OK)
        else:
            error_data = response.json()
            return Response(error_data, status=response.status_code)

class PaystackCustomerViewSet(ViewSet):
    def create(self, request):
        url = "https://api.paystack.co/customer"
        secret_key = settings.PAYSTACK_PRIVATE_KEY
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json"
        }
        data = {
            "email": request.data.get('email'),
            "first_name": request.data.get('first_name'),
            "last_name": request.data.get('last_name'),
            "phone": request.data.get('phone'),
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            # Customer created successfully in Paystack
            customer_data = response.json()
            # Store customer data in the Customer table
            customer = Customer.objects.create(
                email=customer_data.get('data').get('email'),
                first_name=customer_data.get('data').get('first_name'),
                last_name=customer_data.get('data').get('last_name'),
                phone=customer_data.get('data').get('phone')
            )
            return Response(customer_data, status=status.HTTP_201_CREATED)
        else:
            # Error creating customer in Paystack
            error_data = response.json()
            return Response(error_data, status=response.status_code)
    
    def retrieve(self, request, email_or_code):
        url = f"https://api.paystack.co/customer/{email_or_code}"
        secret_key = settings.PAYSTACK_PRIVATE_KEY
        headers = {
            "Authorization": f"Bearer {secret_key}"
        }

        # Making the request to Paystack
        response = requests.get(url, headers=headers)

        # Checking response status and returning appropriate response
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(response.json(), status=response.status_code)
    
    def update_customer(self, request, code):
        url = f"https://api.paystack.co/customer/{code}"
        secret_key = settings.PAYSTACK_PRIVATE_KEY
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json"
        }
        data = { 
            "first_name": request.data.get('first_name'),
            "last_name": request.data.get('last_name'),
            "phone": request.data.get('phone') 
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code == 200:
            # Customer updated successfully in Paystack
            updated_customer_data = response.json()

            # Update customer data in the Customer table
            customer = Customer.objects.get(email=updated_customer_data.get('data').get('email'))
            customer.first_name = updated_customer_data.get('data').get('first_name')
            customer.last_name = updated_customer_data.get('data').get('last_name')
            customer.phone = updated_customer_data.get('data').get('phone')
            customer.save()

            return Response(updated_customer_data, status=status.HTTP_200_OK)
        else:
            # Error updating customer in Paystack
            error_data = response.json()
            return Response(error_data, status=response.status_code)