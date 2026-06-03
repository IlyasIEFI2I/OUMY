import os
from datetime import datetime
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


class MailService:
    """Service d'envoi d'e-mail pour les rapports de réponses"""

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL", "ilyas.elaoufirpro@gmail.com")

    async def send_report(self, answers: dict, user_ip: str):
        """
        Envoie le rapport complet des réponses par e-mail

        Args:
            answers: Dictionnaire contenant les réponses
            user_ip: Adresse IP de l'utilisateur
        """
        try:
            # Créer le rapport formaté
            report = self._format_report(answers, user_ip)

            # Créer le message e-mail HTML
            html_body = self._create_html_email(answers, user_ip)

            # Configurer le message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Nouvelles réponses de Oumaima ❤️"
            message["From"] = self.smtp_username
            message["To"] = self.recipient_email

            # Ajouter les parties du message
            part1 = MIMEText(report, "plain")
            part2 = MIMEText(html_body, "html")
            message.attach(part1)
            message.attach(part2)

            # Envoyer l'e-mail
            if self.smtp_username and self.smtp_password:
                async with aiosmtplib.SMTP(hostname=self.smtp_server, port=465, use_tls=True) as smtp:
                    await smtp.login(self.smtp_username, self.smtp_password)
                    await smtp.send_message(message)
                return True
            else:
                print("⚠️  Configuration SMTP manquante - e-mail non envoyé")
                print(f"Rapport:\n{report}")
                return False

        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de l'e-mail: {str(e)}")
            return False

    def _format_report(self, answers: dict, user_ip: str) -> str:
        """Formate le rapport en texte brut"""
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M")

        report = "===== RAPPORT OUMAIMA ❤️ =====\n\n"
        report += f"Date : {date_str}\n"
        report += f"Heure : {time_str}\n"
        report += f"Adresse IP : {user_ip}\n"
        report += "\n" + "=" * 50 + "\n\n"

        questions = [
            "1. OUMI ZOUMI 🥰, wach kanḍ7k ? 😄",
            "2. Wach kat3jbek les moments li kandouzou m3a ba3diyatna ? ❤️",
            "3. Mlli katchoufi message menni, wach katferr7i ? 📱💕",
            "4. Wach kat7essi belli kayna complicité zwina binatna ? ✨",
            "5. Wach bghiti n3ichou encore plus de souvenirs ensemble ? 🌹",
            "6. Wach walit chi wa7ed important f 7yatk ? ❤️",
            "7. Ila gltlik nbdaw aventure jdida ana w nti, wach twaf9i ? 🥰",
            "8. Wach katchoufi belli n9dro nkounou un joli couple ? 💖",
            "9. Wach bghiti twelli ma copine ? 💍❤️",
        ]

        for i, question in enumerate(questions, 1):
            answer = answers.get(f"q{i}", "Non répondue")
            report += f"Question {i}:\n{question}\nRéponse: {answer}\n\n"

        report += "=" * 50 + "\n"
        report += "OUMI ZOUMI lhoub diali ❤️\n"

        return report

    def _create_html_email(self, answers: dict, user_ip: str) -> str:
        """Crée un corps d'e-mail HTML présenté"""
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M")

        questions = [
            "OUMI ZOUMI 🥰, wach kanḍ7k ? 😄",
            "Wach kat3jbek les moments li kandouzou m3a ba3diyatna ? ❤️",
            "Mlli katchoufi message menni, wach katferr7i ? 📱💕",
            "Wach kat7essi belli kayna complicité zwina binatna ? ✨",
            "Wach bghiti n3ichou encore plus de souvenirs ensemble ? 🌹",
            "Wach walit chi wa7ed important f 7yatk ? ❤️",
            "Ila gltlik nbdaw aventure jdida ana w nti, wach twaf9i ? 🥰",
            "Wach katchoufi belli n9dro nkounou un joli couple ? 💖",
            "Wach bghiti twelli ma copine ? 💍❤️",
        ]

        html = f"""
        <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: #333;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 15px;
                        padding: 30px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    }}
                    .header {{
                        text-align: center;
                        color: #e91e63;
                        margin-bottom: 30px;
                        font-size: 24px;
                        font-weight: bold;
                    }}
                    .info {{
                        background: #f5f5f5;
                        padding: 15px;
                        border-radius: 8px;
                        margin-bottom: 20px;
                        font-size: 14px;
                    }}
                    .question-block {{
                        margin-bottom: 20px;
                        border-left: 4px solid #e91e63;
                        padding-left: 15px;
                    }}
                    .question {{
                        font-weight: bold;
                        color: #333;
                        margin-bottom: 5px;
                    }}
                    .answer {{
                        color: #666;
                        font-style: italic;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        color: #e91e63;
                        font-size: 16px;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">❤️ Rapport des Réponses d'Oumaima ❤️</div>
                    
                    <div class="info">
                        <strong>Date:</strong> {date_str}<br>
                        <strong>Heure:</strong> {time_str}<br>
                        <strong>Adresse IP:</strong> {user_ip}
                    </div>

                    <div style="border-top: 2px solid #e91e63; padding-top: 20px;">
        """

        for i, question in enumerate(questions, 1):
            answer = answers.get(f"q{i}", "Non répondue")
            html += f"""
                        <div class="question-block">
                            <div class="question">Question {i}: {question}</div>
                            <div class="answer">✓ {answer}</div>
                        </div>
            """

        html += """
                    </div>

                    <div class="footer">
                        💕 OUMI ZOUMI lhoub diali ❤️ 💕<br>
                        Merci d'avoir dit oui 🥰
                    </div>
                </div>
            </body>
        </html>
        """

        return html


# Créer une instance du service
mail_service = MailService()
