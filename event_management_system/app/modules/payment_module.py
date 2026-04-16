"""
Payment Processing Module
Razorpay integration for payment handling
"""
import razorpay
import os
from utils.database import insert, update, get_one


class PaymentManager:
    """Manages payment processing and Razorpay integration"""
    
    def __init__(self, key_id, key_secret):
        """Initialize Razorpay client"""
        self.client = razorpay.Client(auth=(key_id, key_secret))
        self.key_id = key_id
    
    def create_order(self, amount, currency='INR', receipt_id='', notes=None):
        """
        Create a Razorpay order
        
        Args:
            amount: Amount in paise (multiply by 100 for rupees)
            currency: Currency code (default: INR)
            receipt_id: Receipt identifier
            notes: Additional notes/metadata
        
        Returns:
            Order data or None
        """
        try:
            order_data = {
                'amount': int(amount * 100),  # Convert to paise
                'currency': currency,
                'receipt': receipt_id,
                'payment_capture': 1  # Auto-capture payment
            }
            
            if notes:
                order_data['notes'] = notes
            
            order = self.client.order.create(order_data)
            return order
        
        except Exception as e:
            print(f"Error creating order: {e}")
            return None
    
    def verify_payment_signature(self, razorpay_order_id, razorpay_payment_id, razorpay_signature, key_secret):
        """
        Verify payment signature from Razorpay
        
        Args:
            razorpay_order_id: Order ID from Razorpay
            razorpay_payment_id: Payment ID from Razorpay
            razorpay_signature: Signature provided by Razorpay
            key_secret: Razorpay API secret
        
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            from hashlib import sha256
            import hmac
            
            # Generate message
            message = f"{razorpay_order_id}|{razorpay_payment_id}"
            
            # Create signature
            generated_signature = hmac.new(
                key_secret.encode(),
                message.encode(),
                sha256
            ).hexdigest()
            
            # Compare signatures
            return generated_signature == razorpay_signature
        
        except Exception as e:
            print(f"Error verifying signature: {e}")
            return False
    
    def verify_payment(self, razorpay_payment_id):
        """
        Verify payment details from Razorpay
        
        Args:
            razorpay_payment_id: Payment ID
        
        Returns:
            Payment details or None
        """
        try:
            payment = self.client.payment.fetch(razorpay_payment_id)
            return payment
        
        except Exception as e:
            print(f"Error fetching payment: {e}")
            return None
    
    def capture_payment(self, razorpay_payment_id, amount):
        """
        Capture an authorized payment
        
        Args:
            razorpay_payment_id: Payment ID
            amount: Amount to capture in paise
        
        Returns:
            Payment data or None
        """
        try:
            payment = self.client.payment.capture(razorpay_payment_id, amount)
            return payment
        
        except Exception as e:
            print(f"Error capturing payment: {e}")
            return None
    
    def refund_payment(self, razorpay_payment_id, amount=None):
        """
        Refund a payment
        
        Args:
            razorpay_payment_id: Payment ID
            amount: Amount to refund (if not specified, refund full amount)
        
        Returns:
            Refund data or None
        """
        try:
            refund_data = {}
            if amount:
                refund_data['amount'] = int(amount * 100)
            
            refund = self.client.payment.refund(razorpay_payment_id, refund_data)
            return refund
        
        except Exception as e:
            print(f"Error refunding payment: {e}")
            return None
    
    def get_payment_details(self, razorpay_payment_id):
        """Get detailed information about a payment"""
        try:
            return self.client.payment.fetch(razorpay_payment_id)
        
        except Exception as e:
            print(f"Error getting payment details: {e}")
            return None
    
    def process_webhook(self, event_data):
        """
        Process Razorpay webhook
        
        Args:
            event_data: Webhook payload from Razorpay
        
        Returns:
            Success status and message
        """
        try:
            event_type = event_data.get('event')
            
            if event_type == 'payment.authorized':
                return self._handle_payment_authorized(event_data)
            
            elif event_type == 'payment.failed':
                return self._handle_payment_failed(event_data)
            
            elif event_type == 'payment.captured':
                return self._handle_payment_captured(event_data)
            
            return True, "Event processed"
        
        except Exception as e:
            print(f"Error processing webhook: {e}")
            return False, str(e)
    
    def _handle_payment_authorized(self, event_data):
        """Handle payment authorized event"""
        # Implement logic to handle authorized payment
        return True, "Payment authorized"
    
    def _handle_payment_failed(self, event_data):
        """Handle payment failed event"""
        # Implement logic to handle failed payment
        return True, "Payment failed handled"
    
    def _handle_payment_captured(self, event_data):
        """Handle payment captured event"""
        # Implement logic to handle captured payment
        return True, "Payment captured"


def get_payment_manager(app):
    """Factory function to get PaymentManager instance"""
    key_id = app.config.get('RAZORPAY_KEY_ID')
    key_secret = app.config.get('RAZORPAY_KEY_SECRET')
    
    if not key_id or not key_secret:
        raise ValueError("Razorpay credentials not configured")
    
    return PaymentManager(key_id, key_secret)
