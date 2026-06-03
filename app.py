from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
import uuid
from services.mail_service import mail_service

# Charger les variables d'environnement
load_dotenv()

# Initialiser FastAPI
app = FastAPI(title="Oumaima - OUMI ZOUMI ❤️", description="Application romantique spéciale")

# Configurer les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurer les templates
templates = Jinja2Templates(directory="templates")

# Dictionnaire pour gérer les sessions
sessions = {}

# Questions du questionnaire
QUESTIONS = [
    {
        "id": 1,
        "question": "OUMI ZOUMI 🥰, wach kanḍ7k ? 😄",
        "answers": ["Oui", "Non"],
    },
    {
        "id": 2,
        "question": "Wach kat3jbek les moments li kandouzou m3a ba3diyatna ? ❤️",
        "answers": ["Oui", "Non"],
    },
    {
        "id": 3,
        "question": "Mlli katchoufi message menni, wach katferr7i ? 📱💕",
        "answers": ["Oui", "Non"],
    },
    {
        "id": 4,
        "question": "Wach kat7essi belli kayna complicité zwina binatna ? ✨",
        "answers": ["Oui", "Non"],
    },
    {
        "id": 5,
        "question": "Wach bghiti n3ichou encore plus de souvenirs ensemble ? 🌹",
        "answers": ["Oui", "Non"],
    },
    {
        "id": 6,
        "question": "Wach walit chi wa7ed important f 7yatk ? ❤️",
        "answers": ["Oui", "Non"],
    },
    {
        "id": 7,
        "question": "Ila gltlik nbdaw aventure jdida ana w nti, wach twaf9i ? 🥰",
        "answers": ["Oui", "Non"],
    },
    {
        "id": 8,
        "question": "Wach katchoufi belli n9dro nkounou un joli couple ? 💖",
        "answers": ["Oui", "Non"],
    },
]


def get_client_ip(request: Request) -> str:
    """Récupère l'adresse IP du client"""
    if request.client:
        return request.client.host
    return "127.0.0.1"


def get_or_create_session(request: Request) -> str:
    """Crée ou récupère une session utilisateur"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "answers": {},
            "ip": get_client_ip(request),
            "completed": False,
        }
    return session_id


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Page d'accueil avec animation d'introduction"""
    session_id = get_or_create_session(request)
    response = templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "nickname": "OUMI ZOUMI",
            "name": "Oumaima Dahhou",
        },
    )
    response.set_cookie("session_id", session_id, max_age=3600 * 24)
    return response


@app.get("/question/{question_id}", response_class=HTMLResponse)
async def get_question(request: Request, question_id: int):
    """Affiche une question"""
    session_id = request.cookies.get("session_id")

    # Créer ou récupérer la session
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "answers": {},
            "ip": get_client_ip(request),
            "completed": False,
        }

    # Vérifier que la question est valide
    if question_id < 1 or question_id > len(QUESTIONS):
        return RedirectResponse(url="/question/1", status_code=302)

    # Vérifier que nous n'avons pas sauté d'étapes
    session_data = sessions[session_id]
    if question_id > 1 and f"q{question_id - 1}" not in session_data["answers"]:
        return RedirectResponse(url="/question/1", status_code=302)

    question = QUESTIONS[question_id - 1]

    response = templates.TemplateResponse(
        request=request,
        name="question.html",
        context={
            "question": question,
            "question_number": question_id,
            "total_questions": len(QUESTIONS),
            "progress": int((question_id / (len(QUESTIONS) + 1)) * 100),
        },
    )
    response.set_cookie("session_id", session_id, max_age=3600 * 24)
    return response


@app.post("/answer/{question_id}")
async def submit_answer(request: Request, question_id: int):
    """Enregistre une réponse et redirige vers la question suivante"""
    session_id = request.cookies.get("session_id")

    # Vérifier la session
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=401, detail="Session invalide")

    # Vérifier la question
    if question_id < 1 or question_id > len(QUESTIONS):
        raise HTTPException(status_code=400, detail="Question invalide")

    # Récupérer la réponse
    form_data = await request.form()
    answer = form_data.get("answer")

    # Valider la réponse
    valid_answers = QUESTIONS[question_id - 1]["answers"]
    if answer not in valid_answers:
        raise HTTPException(status_code=400, detail="Réponse invalide")

    # Enregistrer la réponse
    sessions[session_id]["answers"][f"q{question_id}"] = answer

    # Si c'est la dernière question, rediriger vers la question finale
    if question_id >= len(QUESTIONS):
        return RedirectResponse(url="/final-question", status_code=302)

    # Sinon, rediriger vers la question suivante
    return RedirectResponse(url=f"/question/{question_id + 1}", status_code=302)


@app.get("/final-question", response_class=HTMLResponse)
async def final_question(request: Request):
    """Page de la question finale"""
    session_id = request.cookies.get("session_id")

    # Vérifier la session
    if not session_id or session_id not in sessions:
        return RedirectResponse(url="/", status_code=302)

    session_data = sessions[session_id]

    # Vérifier que toutes les questions précédentes ont été répondues
    if len(session_data["answers"]) < len(QUESTIONS):
        return RedirectResponse(url="/question/1", status_code=302)

    return templates.TemplateResponse(
        request=request,
        name="final_question.html",
        context={
            "progress": 100,
        },
    )


@app.post("/final-answer")
async def submit_final_answer(request: Request):
    """Enregistre la réponse finale et affiche la page de succès"""
    session_id = request.cookies.get("session_id")

    # Vérifier la session
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=401, detail="Session invalide")

    # Récupérer la réponse
    form_data = await request.form()
    answer = form_data.get("answer")

    # Les seules réponses valides sont Oui ou Bien sûr
    if answer not in ["❤️ Oui", "🥰 Bien sûr"]:
        raise HTTPException(status_code=400, detail="Réponse invalide")

    # Enregistrer la réponse finale
    sessions[session_id]["answers"]["q6"] = answer
    sessions[session_id]["completed"] = True

    # Envoyer l'e-mail avec le rapport

    return RedirectResponse(url="/success", status_code=302)


@app.get("/success", response_class=HTMLResponse)
async def success(request: Request):
    """Page de succès avec animations de célébration"""
    session_id = request.cookies.get("session_id")

    # Vérifier la session
    if not session_id or session_id not in sessions:
        return RedirectResponse(url="/", status_code=302)

    session_data = sessions[session_id]

    # Vérifier que le questionnaire a été complété
    if not session_data["completed"]:
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={
            "name": "Oumaima",
            "nickname": "OUMI ZOUMI",
        },
    )


@app.get("/reset")
async def reset(request: Request):
    """Réinitialise la session (pour tester)"""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        del sessions[session_id]

    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("session_id")
    return response


# Point d'entrée
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
