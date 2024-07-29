from django.core.mail import send_mail

def send_confirmation_email(email, code):
    text_message = f'Your confirmation code is {code}'
    
    html_message = f'''
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@200..1000&display=swap');
            body {{
                font-family: "Cairo", sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 50px auto;
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{
                background-color: #007bff;
                color: #ffffff;
                padding: 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
            }}
            .content {{
                padding: 20px;
                text-align: center;
            }}
            .content p {{
                font-size: 16px;
                line-height: 1.6;
            }}
            .content .code {{
                display: inline-block;
                padding: 10px 20px;
                margin: 20px 0;
                font-size: 24px;
                font-weight: bold;
                color: #ffffff;
                background-color: #007bff;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s;
            }}
            .footer {{
                background-color: #f4f4f4;
                color: #888888;
                text-align: center;
                padding: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>تأكيد البريد الإلكتروني</h1>
            </div>
            <div class="content">
                <p>مرحبًا،</p>
                <p>شكرًا لتسجيلك معنا. يرجى استخدام رمز التحقق أدناه لإكمال عملية التحقق من بريدك الإلكتروني.</p>
                <div class="code">{code}</div>
                <p id="confirmationMessage" style="display: none; color: #28a745;">تم نسخ رمز التحقق إلى الحافظة!</p>
                <p>إذا لم تكن قد طلبت هذا الرمز، يرجى تجاهل هذا البريد الإلكتروني.</p>
                <p>مع أطيب التحيات،<br>فريق LearnGpt</p>
            </div>
            <div class="footer">
                &copy; 2024 LearnGpt. جميع الحقوق محفوظة.
            </div>
        </div>
    </body>
    </html>
    '''
    
    send_mail(
        'تأكيد البريد الإلكتروني',
        text_message,
        'example@gmail.com',
        [email],
        fail_silently=False,
        html_message=html_message
    )
