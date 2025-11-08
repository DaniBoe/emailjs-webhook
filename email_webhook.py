"""
Webhook server for Retell AI → EmailJS integration
Deploy this to Render, Railway, or similar hosting service
"""

from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/webhook/email', methods=['POST'])
def send_email():
    """
    Webhook endpoint for Retell AI to send emails via EmailJS
    """
    try:
        data = request.json
        
        # Extract reservation data from Retell AI
        reservation_name = data.get('reservation_name', 'Guest')
        reservation_date = data.get('reservation_date', '')
        reservation_time = data.get('reservation_time', '')
        reservation_people = data.get('reservation_people', '')
        reservation_phone = data.get('reservation_phone', '')
        reservation_notes = data.get('reservation_notes', 'None')
        
        # EmailJS payload (try with both keys for server-side)
        emailjs_data = {
            "service_id": "service_z0tw43m",
            "template_id": "template_pkposkm",
            "user_id": "cEXwDy_CPYaDDhUFk",
            "accessToken": "yPs9Q0wM5gKDzXZXmJg5s",
            "template_params": {
                "to_email": "daniel.boettcher89@gmail.com",
                "customer_name": reservation_name,
                "reservation_date": reservation_date,
                "reservation_time": reservation_time,
                "party_size": reservation_people,
                "phone_number": reservation_phone,
                "special_requests": reservation_notes,
                "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p")
            }
        }
        
        # Send to EmailJS with browser-like headers to avoid 403
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Origin": "https://dashboard.emailjs.com",
            "Referer": "https://dashboard.emailjs.com/"
        }
        
        response = requests.post(
            "https://api.emailjs.com/api/v1.0/email/send",
            headers=headers,
            json=emailjs_data
        )
        
        if response.status_code == 200:
            return jsonify({
                "success": True,
                "message": "Email sent successfully"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": response.text,
                "status_code": response.status_code
            }), response.status_code
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

