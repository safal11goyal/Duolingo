import json
from datetime import datetime, date, timedelta, timezone
from .database import engine, SessionLocal, Base
from .auth.security import hash_password
from .models import (
    User, Course, Unit, Skill, Lesson, Exercise, ExerciseOption,
    UserSkillProgress, DailyActivity, Achievement, UserAchievement, LessonAttempt
)

def seed_database():
    print("Recreating database tables with updated authentication schema...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:

        print("Seeding achievements...")
        achievements_data = [
            {
                "name": "First Step",
                "description": "Complete your very first lesson",
                "icon": "zap",
                "requirement_type": "first_lesson",
                "requirement_value": 1
            },
            {
                "name": "Wildfire",
                "description": "Reach a 3-day learning streak",
                "icon": "flame",
                "requirement_type": "streak",
                "requirement_value": 3
            },
            {
                "name": "Sage",
                "description": "Reach a 7-day learning streak",
                "icon": "calendar",
                "requirement_type": "streak",
                "requirement_value": 7
            },
            {
                "name": "Scholar",
                "description": "Earn 100 total XP",
                "icon": "book-open",
                "requirement_type": "xp",
                "requirement_value": 100
            },
            {
                "name": "Legend",
                "description": "Earn 500 total XP",
                "icon": "award",
                "requirement_type": "xp",
                "requirement_value": 500
            },
            {
                "name": "Sharpshooter",
                "description": "Finish a lesson with 100% accuracy without losing any hearts",
                "icon": "target",
                "requirement_type": "perfect_lesson",
                "requirement_value": 1
            },
            {
                "name": "Crown Collector",
                "description": "Earn 3 crowns across your skills",
                "icon": "crown",
                "requirement_type": "crowns",
                "requirement_value": 3
            }
        ]
        created_achievements = []
        for ach in achievements_data:
            a = Achievement(**ach)
            db.add(a)
            created_achievements.append(a)
        db.commit()

        print("Seeding default learner & leaderboard users...")
        default_pwd_hash = hash_password("Demo123!")
        users_data = [
            {"username": "sofia_r", "email": "sofia@example.com", "display_name": "Sofia Ramos", "avatar": "/avatars/sofia.png", "xp": 1820, "gems": 1200, "hearts": 5, "streak": 14},
            {"username": "daniel_k", "email": "daniel@example.com", "display_name": "Daniel Kim", "avatar": "/avatars/daniel.png", "xp": 1430, "gems": 850, "hearts": 4, "streak": 9},
            {"username": "maria_g", "email": "maria@example.com", "display_name": "Maria Garcia", "avatar": "/avatars/maria.png", "xp": 980, "gems": 620, "hearts": 5, "streak": 6},
            {"username": "carlos_o", "email": "carlos@example.com", "display_name": "Carlos Ortiz", "avatar": "/avatars/carlos.png", "xp": 740, "gems": 450, "hearts": 3, "streak": 4},
            {"username": "elena_r", "email": "elena@example.com", "display_name": "Elena Rostova", "avatar": "/avatars/elena.png", "xp": 610, "gems": 390, "hearts": 5, "streak": 5},
            {"username": "liam_s", "email": "liam@example.com", "display_name": "Liam Smith", "avatar": "/avatars/liam.png", "xp": 430, "gems": 300, "hearts": 5, "streak": 2},
            {"username": "chloe_d", "email": "chloe@example.com", "display_name": "Chloe Dupont", "avatar": "/avatars/chloe.png", "xp": 290, "gems": 200, "hearts": 2, "streak": 1},
        ]
        for u in users_data:
            db.add(User(
                username=u["username"],
                email=u["email"],
                password_hash=default_pwd_hash,
                display_name=u["display_name"],
                avatar=u["avatar"],
                xp=u["xp"],
                gems=u["gems"],
                hearts=u["hearts"],
                streak=u["streak"],
                daily_goal=20,
                last_active_at=datetime.now(timezone.utc),
                created_at=datetime.now(timezone.utc) - timedelta(days=20),
                updated_at=datetime.now(timezone.utc)
            ))

        # Main demo learner Alex
        alex = User(
            username="alex",
            email="demo@example.com",
            password_hash=default_pwd_hash,
            display_name="Alex Rivera",
            avatar="/avatars/alex.png",
            xp=150,
            gems=500,
            hearts=5,
            streak=3,
            daily_goal=20,
            last_active_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc) - timedelta(days=10),
            updated_at=datetime.now(timezone.utc)
        )
        db.add(alex)
        db.commit()
        db.refresh(alex)

        # Seed recent activity for Alex to support 3-day streak
        today = date.today()
        for i in range(3):
            act_date = today - timedelta(days=(2 - i))
            db.add(DailyActivity(
                user_id=alex.id,
                activity_date=act_date,
                xp_earned=25,
                lessons_completed=2
            ))
        db.commit()

        # Seed course
        print("Seeding Spanish course, units, skills, lessons, and exercises...")
        course = Course(
            name="Spanish",
            source_language="English",
            target_language="Spanish"
        )
        db.add(course)
        db.commit()
        db.refresh(course)

        # 3 Units
        units_structure = [
            {
                "title": "Unit 1: The Essentials",
                "description": "Form basic sentences, order food, and greet friends",
                "order_index": 1,
                "skills": [
                    {
                        "title": "Greetings",
                        "description": "Say hello, ask how someone is, and say goodbye",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "Basic Hellos & Goodbyes",
                                "order_index": 1,
                                "exercises": [
                                    {
                                        "type": "multiple_choice",
                                        "question": "How do you say 'Hello' in Spanish?",
                                        "correct_answer": "Hola",
                                        "explanation": "'Hola' is the universal Spanish greeting for hello.",
                                        "xp": 2,
                                        "options": [
                                            ("Hola", True),
                                            ("Adios", False),
                                            ("Gracias", False),
                                            ("Por favor", False)
                                        ]
                                    },
                                    {
                                        "type": "translate",
                                        "question": "Translate: 'Good morning'",
                                        "correct_answer": "Buenos dias / Buenos días",
                                        "explanation": "'Buenos días' translates directly to good day or good morning.",
                                        "xp": 2,
                                        "options": []
                                    },
                                    {
                                        "type": "word_bank",
                                        "question": "Build the sentence: 'Hello, how are you?'",
                                        "correct_answer": "Hola como estas / Hola cómo estás",
                                        "explanation": "'Hola, ¿cómo estás?' is the informal way to ask how someone is doing.",
                                        "xp": 3,
                                        "options": [
                                            ("Hola", True),
                                            ("como", True),
                                            ("estas", True),
                                            ("adios", False),
                                            ("gracias", False),
                                            ("bien", False)
                                        ]
                                    },
                                    {
                                        "type": "match_pairs",
                                        "question": "Tap the matching pairs",
                                        "correct_answer": json.dumps({
                                            "Hello": "Hola",
                                            "Goodbye": "Adios",
                                            "Please": "Por favor",
                                            "Thank you": "Gracias"
                                        }),
                                        "explanation": "Essential courtesy words in Spanish.",
                                        "xp": 3,
                                        "options": []
                                    },
                                    {
                                        "type": "fill_blank",
                                        "question": "Muchas ___ por su ayuda.",
                                        "correct_answer": "gracias",
                                        "explanation": "'Muchas gracias' means 'Many thanks' or 'Thank you very much'.",
                                        "xp": 2,
                                        "options": [
                                            ("gracias", True),
                                            ("hola", False),
                                            ("por favor", False)
                                        ]
                                    },
                                    {
                                        "type": "type_answer",
                                        "question": "Type the Spanish word for 'Goodbye':",
                                        "correct_answer": "Adios / Adiós",
                                        "explanation": "'Adiós' means goodbye.",
                                        "xp": 2,
                                        "options": []
                                    }
                                ]
                            },
                            {
                                "title": "Polite Expressions",
                                "order_index": 2,
                                "exercises": [
                                    {
                                        "type": "multiple_choice",
                                        "question": "Which word means 'Thank you'?",
                                        "correct_answer": "Gracias",
                                        "explanation": "'Gracias' means thank you.",
                                        "xp": 2,
                                        "options": [
                                            ("Gracias", True),
                                            ("De nada", False),
                                            ("Disculpe", False),
                                            ("Perdon", False)
                                        ]
                                    },
                                    {
                                        "type": "translate",
                                        "question": "Translate: 'You are welcome'",
                                        "correct_answer": "De nada",
                                        "explanation": "'De nada' is literally 'of nothing', meaning you're welcome.",
                                        "xp": 2,
                                        "options": []
                                    },
                                    {
                                        "type": "word_bank",
                                        "question": "Build: 'Excuse me, please'",
                                        "correct_answer": "Disculpe por favor / Perdón por favor",
                                        "explanation": "'Disculpe, por favor' is polite Spanish.",
                                        "xp": 3,
                                        "options": [
                                            ("Disculpe", True),
                                            ("por", True),
                                            ("favor", True),
                                            ("gracias", False),
                                            ("hola", False)
                                        ]
                                    },
                                    {
                                        "type": "match_pairs",
                                        "question": "Match the polite greetings",
                                        "correct_answer": json.dumps({
                                            "Good afternoon": "Buenas tardes",
                                            "Good night": "Buenas noches",
                                            "See you later": "Hasta luego",
                                            "See you tomorrow": "Hasta manana"
                                        }),
                                        "explanation": "Standard time-of-day greetings.",
                                        "xp": 3,
                                        "options": []
                                    },
                                    {
                                        "type": "fill_blank",
                                        "question": "Buenas ___, que descanses.",
                                        "correct_answer": "noches",
                                        "explanation": "'Buenas noches' means good evening or good night.",
                                        "xp": 2,
                                        "options": [
                                            ("noches", True),
                                            ("tardes", False),
                                            ("dias", False)
                                        ]
                                    },
                                    {
                                        "type": "type_answer",
                                        "question": "Type 'Please' in Spanish:",
                                        "correct_answer": "Por favor",
                                        "explanation": "'Por favor' translates to please.",
                                        "xp": 2,
                                        "options": []
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "title": "Food & Drink",
                        "description": "Order coffee, water, bread, and fruits",
                        "order_index": 2,
                        "lessons": [
                            {
                                "title": "Café Essentials",
                                "order_index": 1,
                                "exercises": [
                                    {
                                        "type": "multiple_choice",
                                        "question": "What is 'Coffee' in Spanish?",
                                        "correct_answer": "Café",
                                        "explanation": "'El café' means coffee.",
                                        "xp": 2,
                                        "options": [
                                            ("Café", True),
                                            ("Agua", False),
                                            ("Pan", False),
                                            ("Leche", False)
                                        ]
                                    },
                                    {
                                        "type": "translate",
                                        "question": "Translate: 'A coffee with milk'",
                                        "correct_answer": "Un café con leche / Un cafe con leche",
                                        "explanation": "'Un café con leche' is a very popular drink in Spain and Latin America.",
                                        "xp": 2,
                                        "options": []
                                    },
                                    {
                                        "type": "word_bank",
                                        "question": "Build: 'I want water, please'",
                                        "correct_answer": "Yo quiero agua por favor / Quiero agua por favor",
                                        "explanation": "'(Yo) quiero agua, por favor.'",
                                        "xp": 3,
                                        "options": [
                                            ("Yo", True),
                                            ("quiero", True),
                                            ("agua", True),
                                            ("por", True),
                                            ("favor", True),
                                            ("pan", False),
                                            ("leche", False)
                                        ]
                                    },
                                    {
                                        "type": "match_pairs",
                                        "question": "Match the breakfast items",
                                        "correct_answer": json.dumps({
                                            "Water": "Agua",
                                            "Bread": "Pan",
                                            "Milk": "Leche",
                                            "Coffee": "Cafe"
                                        }),
                                        "explanation": "Common food vocabulary.",
                                        "xp": 3,
                                        "options": []
                                    },
                                    {
                                        "type": "fill_blank",
                                        "question": "El vaso de ___ está frío.",
                                        "correct_answer": "agua",
                                        "explanation": "'El vaso de agua' = The glass of water.",
                                        "xp": 2,
                                        "options": [
                                            ("agua", True),
                                            ("pan", False),
                                            ("mesa", False)
                                        ]
                                    },
                                    {
                                        "type": "type_answer",
                                        "question": "Type the Spanish word for 'Bread':",
                                        "correct_answer": "Pan",
                                        "explanation": "'Pan' is bread in Spanish.",
                                        "xp": 2,
                                        "options": []
                                    }
                                ]
                            },
                            {
                                "title": "At the Restaurant",
                                "order_index": 2,
                                "exercises": [
                                    {
                                        "type": "multiple_choice",
                                        "question": "How do you ask for 'The bill'?",
                                        "correct_answer": "La cuenta",
                                        "explanation": "'La cuenta, por favor' means 'The check/bill, please.'",
                                        "xp": 2,
                                        "options": [
                                            ("La cuenta", True),
                                            ("La comida", False),
                                            ("La mesa", False),
                                            ("El vaso", False)
                                        ]
                                    },
                                    {
                                        "type": "translate",
                                        "question": "Translate: 'A table for two'",
                                        "correct_answer": "Una mesa para dos",
                                        "explanation": "'Una mesa para dos' is how you request seating at a restaurant.",
                                        "xp": 2,
                                        "options": []
                                    },
                                    {
                                        "type": "word_bank",
                                        "question": "Build: 'The food is delicious'",
                                        "correct_answer": "La comida es deliciosa / La comida esta deliciosa",
                                        "explanation": "'La comida es deliciosa.'",
                                        "xp": 3,
                                        "options": [
                                            ("La", True),
                                            ("comida", True),
                                            ("es", True),
                                            ("deliciosa", True),
                                            ("dos", False),
                                            ("cuenta", False)
                                        ]
                                    },
                                    {
                                        "type": "match_pairs",
                                        "question": "Match dining vocabulary",
                                        "correct_answer": json.dumps({
                                            "Food": "Comida",
                                            "Table": "Mesa",
                                            "Bill": "Cuenta",
                                            "Delicious": "Delicioso"
                                        }),
                                        "explanation": "Restaurant terms.",
                                        "xp": 3,
                                        "options": []
                                    },
                                    {
                                        "type": "fill_blank",
                                        "question": "La ___ por favor, queremos pagar.",
                                        "correct_answer": "cuenta",
                                        "explanation": "'La cuenta por favor' asks for the bill.",
                                        "xp": 2,
                                        "options": [
                                            ("cuenta", True),
                                            ("comida", False),
                                            ("leche", False)
                                        ]
                                    },
                                    {
                                        "type": "type_answer",
                                        "question": "Type 'Table' in Spanish:",
                                        "correct_answer": "Mesa",
                                        "explanation": "'Mesa' is table.",
                                        "xp": 2,
                                        "options": []
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "title": "People",
                        "description": "Talk about people, friends, and pronouns",
                        "order_index": 3,
                        "lessons": [
                            {
                                "title": "Pronouns & Introductions",
                                "order_index": 1,
                                "exercises": [
                                    {
                                        "type": "multiple_choice",
                                        "question": "What does 'Yo soy' mean?",
                                        "correct_answer": "I am",
                                        "explanation": "'Yo soy' translates to 'I am'.",
                                        "xp": 2,
                                        "options": [
                                            ("I am", True),
                                            ("You are", False),
                                            ("He is", False),
                                            ("We are", False)
                                        ]
                                    },
                                    {
                                        "type": "translate",
                                        "question": "Translate: 'I am a student'",
                                        "correct_answer": "Yo soy un estudiante / Soy un estudiante / Soy estudiante",
                                        "explanation": "'(Yo) soy un estudiante' = I am a student.",
                                        "xp": 2,
                                        "options": []
                                    },
                                    {
                                        "type": "word_bank",
                                        "question": "Build: 'She is my friend'",
                                        "correct_answer": "Ella es mi amiga / Ella es mi amigo",
                                        "explanation": "'Ella es mi amiga.'",
                                        "xp": 3,
                                        "options": [
                                            ("Ella", True),
                                            ("es", True),
                                            ("mi", True),
                                            ("amiga", True),
                                            ("yo", False),
                                            ("tu", False)
                                        ]
                                    },
                                    {
                                        "type": "match_pairs",
                                        "question": "Match pronouns and people",
                                        "correct_answer": json.dumps({
                                            "I": "Yo",
                                            "You": "Tu",
                                            "He": "El",
                                            "She": "Ella"
                                        }),
                                        "explanation": "Subject pronouns in Spanish.",
                                        "xp": 3,
                                        "options": []
                                    },
                                    {
                                        "type": "fill_blank",
                                        "question": "Él ___ mi profesor de español.",
                                        "correct_answer": "es",
                                        "explanation": "'Él es' = He is.",
                                        "xp": 2,
                                        "options": [
                                            ("es", True),
                                            ("soy", False),
                                            ("eres", False)
                                        ]
                                    },
                                    {
                                        "type": "type_answer",
                                        "question": "Type the Spanish word for 'Friend' (feminine):",
                                        "correct_answer": "Amiga",
                                        "explanation": "'Amiga' is female friend.",
                                        "xp": 2,
                                        "options": []
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Unit 2: Daily Life & Surroundings",
                "description": "Describe your family, navigate places, and talk about routines",
                "order_index": 2,
                "skills": [
                    {
                        "title": "Family",
                        "description": "Talk about parents, siblings, and pets",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "Immediate Family",
                                "order_index": 1,
                                "exercises": [
                                    {
                                        "type": "multiple_choice",
                                        "question": "How do you say 'Mother' in Spanish?",
                                        "correct_answer": "Madre",
                                        "explanation": "'Madre' or 'Mamá' means mother.",
                                        "xp": 2,
                                        "options": [
                                            ("Madre", True),
                                            ("Padre", False),
                                            ("Hermano", False),
                                            ("Hijo", False)
                                        ]
                                    },
                                    {
                                        "type": "translate",
                                        "question": "Translate: 'My father and my mother'",
                                        "correct_answer": "Mi padre y mi madre / Mi papa y mi mama",
                                        "explanation": "'Mi padre y mi madre'.",
                                        "xp": 2,
                                        "options": []
                                    },
                                    {
                                        "type": "word_bank",
                                        "question": "Build: 'I have a brother'",
                                        "correct_answer": "Yo tengo un hermano / Tengo un hermano",
                                        "explanation": "'Tengo un hermano.'",
                                        "xp": 3,
                                        "options": [
                                            ("Yo", True),
                                            ("tengo", True),
                                            ("un", True),
                                            ("hermano", True),
                                            ("madre", False),
                                            ("gato", False)
                                        ]
                                    },
                                    {
                                        "type": "match_pairs",
                                        "question": "Match family members",
                                        "correct_answer": json.dumps({
                                            "Father": "Padre",
                                            "Mother": "Madre",
                                            "Brother": "Hermano",
                                            "Sister": "Hermana"
                                        }),
                                        "explanation": "Core family vocabulary.",
                                        "xp": 3,
                                        "options": []
                                    },
                                    {
                                        "type": "fill_blank",
                                        "question": "Mi ___ se llama Carmen y es muy cariñosa.",
                                        "correct_answer": "madre",
                                        "explanation": "'Mi madre' fits the feminine sentence.",
                                        "xp": 2,
                                        "options": [
                                            ("madre", True),
                                            ("padre", False),
                                            ("hermano", False)
                                        ]
                                    },
                                    {
                                        "type": "type_answer",
                                        "question": "Type the Spanish word for 'Sister':",
                                        "correct_answer": "Hermana",
                                        "explanation": "'Hermana' is sister.",
                                        "xp": 2,
                                        "options": []
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "title": "Places in Town",
                        "description": "Locate banks, parks, hotels, and schools",
                        "order_index": 2,
                        "lessons": [
                            {
                                "title": "Around Town",
                                "order_index": 1,
                                "exercises": [
                                    {
                                        "type": "multiple_choice",
                                        "question": "Where do you stay when traveling?",
                                        "correct_answer": "El hotel",
                                        "explanation": "'El hotel' is hotel.",
                                        "xp": 2,
                                        "options": [
                                            ("El hotel", True),
                                            ("El parque", False),
                                            ("El banco", False),
                                            ("La escuela", False)
                                        ]
                                    },
                                    {
                                        "type": "translate",
                                        "question": "Translate: 'Where is the bank?'",
                                        "correct_answer": "Donde esta el banco / Dónde está el banco",
                                        "explanation": "'¿Dónde está el banco?'",
                                        "xp": 2,
                                        "options": []
                                    },
                                    {
                                        "type": "word_bank",
                                        "question": "Build: 'The hotel is very close'",
                                        "correct_answer": "El hotel esta muy cerca / El hotel está muy cerca",
                                        "explanation": "'El hotel está muy cerca.'",
                                        "xp": 3,
                                        "options": [
                                            ("El", True),
                                            ("hotel", True),
                                            ("esta", True),
                                            ("muy", True),
                                            ("cerca", True),
                                            ("lejos", False),
                                            ("banco", False)
                                        ]
                                    },
                                    {
                                        "type": "match_pairs",
                                        "question": "Match city locations",
                                        "correct_answer": json.dumps({
                                            "Bank": "Banco",
                                            "Park": "Parque",
                                            "Hotel": "Hotel",
                                            "Street": "Calle"
                                        }),
                                        "explanation": "City places.",
                                        "xp": 3,
                                        "options": []
                                    },
                                    {
                                        "type": "fill_blank",
                                        "question": "Los niños juegan en el ___.",
                                        "correct_answer": "parque",
                                        "explanation": "'El parque' is the park.",
                                        "xp": 2,
                                        "options": [
                                            ("parque", True),
                                            ("banco", False),
                                            ("hotel", False)
                                        ]
                                    },
                                    {
                                        "type": "type_answer",
                                        "question": "Type the Spanish word for 'Street':",
                                        "correct_answer": "Calle",
                                        "explanation": "'Calle' means street.",
                                        "xp": 2,
                                        "options": []
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "title": "Activities",
                        "description": "Common verbs like to read, to speak, to walk",
                        "order_index": 3,
                        "lessons": [
                            {
                                "title": "Common Verbs",
                                "order_index": 1,
                                "exercises": [
                                    {
                                        "type": "multiple_choice",
                                        "question": "What verb means 'To speak'?",
                                        "correct_answer": "Hablar",
                                        "explanation": "'Hablar' means to speak or talk.",
                                        "xp": 2,
                                        "options": [
                                            ("Hablar", True),
                                            ("Comer", False),
                                            ("Vivir", False),
                                            ("Escribir", False)
                                        ]
                                    },
                                    {
                                        "type": "translate",
                                        "question": "Translate: 'I speak Spanish'",
                                        "correct_answer": "Yo hablo espanol / Yo hablo español / Hablo espanol / Hablo español",
                                        "explanation": "'(Yo) hablo español.'",
                                        "xp": 2,
                                        "options": []
                                    },
                                    {
                                        "type": "word_bank",
                                        "question": "Build: 'We want to learn Spanish'",
                                        "correct_answer": "Nosotros queremos aprender espanol / Queremos aprender español",
                                        "explanation": "'(Nosotros) queremos aprender español.'",
                                        "xp": 3,
                                        "options": [
                                            ("Nosotros", True),
                                            ("queremos", True),
                                            ("aprender", True),
                                            ("espanol", True),
                                            ("comer", False),
                                            ("hablar", False)
                                        ]
                                    },
                                    {
                                        "type": "match_pairs",
                                        "question": "Match actions",
                                        "correct_answer": json.dumps({
                                            "To eat": "Comer",
                                            "To drink": "Beber",
                                            "To live": "Vivir",
                                            "To read": "Leer"
                                        }),
                                        "explanation": "Essential Spanish verbs.",
                                        "xp": 3,
                                        "options": []
                                    },
                                    {
                                        "type": "fill_blank",
                                        "question": "Me gusta ___ libros en la biblioteca.",
                                        "correct_answer": "leer",
                                        "explanation": "'Leer' = to read.",
                                        "xp": 2,
                                        "options": [
                                            ("leer", True),
                                            ("beber", False),
                                            ("hablar", False)
                                        ]
                                    },
                                    {
                                        "type": "type_answer",
                                        "question": "Type 'To eat' in Spanish:",
                                        "correct_answer": "Comer",
                                        "explanation": "'Comer' is to eat.",
                                        "xp": 2,
                                        "options": []
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Unit 3: Exploring the World",
                "description": "Travel the world, shop for souvenirs, and hold confident conversations",
                "order_index": 3,
                "skills": [
                    {
                        "title": "Travel",
                        "description": "Airports, trains, luggage, and tickets",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "At the Airport",
                                "order_index": 1,
                                "exercises": [
                                    {
                                        "type": "multiple_choice",
                                        "question": "What is 'Airplane' in Spanish?",
                                        "correct_answer": "Avión",
                                        "explanation": "'El avión' = the airplane.",
                                        "xp": 2,
                                        "options": [
                                            ("Avión", True),
                                            ("Tren", False),
                                            ("Carro", False),
                                            ("Bicicleta", False)
                                        ]
                                    },
                                    {
                                        "type": "translate",
                                        "question": "Translate: 'A ticket to Madrid'",
                                        "correct_answer": "Un boleto a Madrid / Un billete para Madrid / Un pasaje a Madrid",
                                        "explanation": "'Un boleto a Madrid.'",
                                        "xp": 2,
                                        "options": []
                                    },
                                    {
                                        "type": "word_bank",
                                        "question": "Build: 'Where is my passport?'",
                                        "correct_answer": "Donde esta mi pasaporte / Dónde está mi pasaporte",
                                        "explanation": "'¿Dónde está mi pasaporte?'",
                                        "xp": 3,
                                        "options": [
                                            ("Donde", True),
                                            ("esta", True),
                                            ("mi", True),
                                            ("pasaporte", True),
                                            ("avion", False),
                                            ("maleta", False)
                                        ]
                                    },
                                    {
                                        "type": "match_pairs",
                                        "question": "Match travel terms",
                                        "correct_answer": json.dumps({
                                            "Passport": "Pasaporte",
                                            "Ticket": "Boleto",
                                            "Luggage": "Maleta",
                                            "Airport": "Aeropuerto"
                                        }),
                                        "explanation": "Travel essentials.",
                                        "xp": 3,
                                        "options": []
                                    },
                                    {
                                        "type": "fill_blank",
                                        "question": "Tengo mi ___ lista para viajar.",
                                        "correct_answer": "maleta",
                                        "explanation": "'La maleta' = suitcase.",
                                        "xp": 2,
                                        "options": [
                                            ("maleta", True),
                                            ("tren", False),
                                            ("avion", False)
                                        ]
                                    },
                                    {
                                        "type": "type_answer",
                                        "question": "Type 'Passport' in Spanish:",
                                        "correct_answer": "Pasaporte",
                                        "explanation": "'Pasaporte' is passport.",
                                        "xp": 2,
                                        "options": []
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "title": "Shopping",
                        "description": "Prices, colors, clothes, and bargaining",
                        "order_index": 2,
                        "lessons": [
                            {
                                "title": "Clothes & Prices",
                                "order_index": 1,
                                "exercises": [
                                    {
                                        "type": "multiple_choice",
                                        "question": "How do you ask 'How much does it cost?'",
                                        "correct_answer": "¿Cuánto cuesta?",
                                        "explanation": "'¿Cuánto cuesta?' asks for price.",
                                        "xp": 2,
                                        "options": [
                                            ("¿Cuánto cuesta?", True),
                                            ("¿Qué hora es?", False),
                                            ("¿Cómo estás?", False),
                                            ("¿Dónde queda?", False)
                                        ]
                                    },
                                    {
                                        "type": "translate",
                                        "question": "Translate: 'The red shirt is expensive'",
                                        "correct_answer": "La camisa roja es cara",
                                        "explanation": "'La camisa roja es cara.'",
                                        "xp": 2,
                                        "options": []
                                    },
                                    {
                                        "type": "word_bank",
                                        "question": "Build: 'I want to buy this hat'",
                                        "correct_answer": "Quiero comprar este sombrero / Yo quiero comprar este sombrero",
                                        "explanation": "'(Yo) quiero comprar este sombrero.'",
                                        "xp": 3,
                                        "options": [
                                            ("Quiero", True),
                                            ("comprar", True),
                                            ("este", True),
                                            ("sombrero", True),
                                            ("camisa", False),
                                            ("caro", False)
                                        ]
                                    },
                                    {
                                        "type": "match_pairs",
                                        "question": "Match shopping words",
                                        "correct_answer": json.dumps({
                                            "Shirt": "Camisa",
                                            "Shoes": "Zapatos",
                                            "Expensive": "Caro",
                                            "Cheap": "Barato"
                                        }),
                                        "explanation": "Clothing and shopping vocabulary.",
                                        "xp": 3,
                                        "options": []
                                    },
                                    {
                                        "type": "fill_blank",
                                        "question": "Este vestido es muy bonito y ___.",
                                        "correct_answer": "barato",
                                        "explanation": "'Barato' = inexpensive / cheap.",
                                        "xp": 2,
                                        "options": [
                                            ("barato", True),
                                            ("hola", False),
                                            ("sombrero", False)
                                        ]
                                    },
                                    {
                                        "type": "type_answer",
                                        "question": "Type 'Shoes' in Spanish:",
                                        "correct_answer": "Zapatos",
                                        "explanation": "'Zapatos' = shoes.",
                                        "xp": 2,
                                        "options": []
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "title": "Conversations",
                        "description": "Tell stories, express opinions, and share plans",
                        "order_index": 3,
                        "lessons": [
                            {
                                "title": "Social Chit-Chat",
                                "order_index": 1,
                                "exercises": [
                                    {
                                        "type": "multiple_choice",
                                        "question": "How do you say 'Nice to meet you'?",
                                        "correct_answer": "Mucho gusto",
                                        "explanation": "'Mucho gusto' means nice to meet you.",
                                        "xp": 2,
                                        "options": [
                                            ("Mucho gusto", True),
                                            ("Por favor", False),
                                            ("Buen provecho", False),
                                            ("Salud", False)
                                        ]
                                    },
                                    {
                                        "type": "translate",
                                        "question": "Translate: 'What is your name?'",
                                        "correct_answer": "Como te llamas / Cómo te llamas / Cual es tu nombre",
                                        "explanation": "'¿Cómo te llamas?' is the common informal question.",
                                        "xp": 2,
                                        "options": []
                                    },
                                    {
                                        "type": "word_bank",
                                        "question": "Build: 'My name is Alex'",
                                        "correct_answer": "Mi nombre es Alex / Me llamo Alex",
                                        "explanation": "'Me llamo Alex' or 'Mi nombre es Alex'.",
                                        "xp": 3,
                                        "options": [
                                            ("Mi", True),
                                            ("nombre", True),
                                            ("es", True),
                                            ("Alex", True),
                                            ("mucho", False),
                                            ("gusto", False)
                                        ]
                                    },
                                    {
                                        "type": "match_pairs",
                                        "question": "Match conversational phrases",
                                        "correct_answer": json.dumps({
                                            "Nice to meet you": "Mucho gusto",
                                            "How are you": "Como estas",
                                            "Everything good": "Todo bien",
                                            "See you soon": "Hasta pronto"
                                        }),
                                        "explanation": "Key conversation phrases.",
                                        "xp": 3,
                                        "options": []
                                    },
                                    {
                                        "type": "fill_blank",
                                        "question": "Encantado de conocerte, mucho ___.",
                                        "correct_answer": "gusto",
                                        "explanation": "'Mucho gusto' = a pleasure.",
                                        "xp": 2,
                                        "options": [
                                            ("gusto", True),
                                            ("nombre", False),
                                            ("bien", False)
                                        ]
                                    },
                                    {
                                        "type": "type_answer",
                                        "question": "Type 'Everything good' in Spanish:",
                                        "correct_answer": "Todo bien",
                                        "explanation": "'Todo bien' translates to everything good.",
                                        "xp": 2,
                                        "options": []
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]

        all_created_skills = []
        for u_data in units_structure:
            unit = Unit(
                course_id=course.id,
                title=u_data["title"],
                description=u_data["description"],
                order_index=u_data["order_index"]
            )
            db.add(unit)
            db.commit()
            db.refresh(unit)

            for s_data in u_data["skills"]:
                skill = Skill(
                    unit_id=unit.id,
                    title=s_data["title"],
                    description=s_data["description"],
                    order_index=s_data["order_index"],
                    xp_reward=10
                )
                db.add(skill)
                db.commit()
                db.refresh(skill)
                all_created_skills.append(skill)

                for l_data in s_data["lessons"]:
                    lesson = Lesson(
                        skill_id=skill.id,
                        title=l_data["title"],
                        order_index=l_data["order_index"],
                        xp_reward=10
                    )
                    db.add(lesson)
                    db.commit()
                    db.refresh(lesson)

                    for ex_idx, ex_data in enumerate(l_data["exercises"], start=1):
                        exercise = Exercise(
                            lesson_id=lesson.id,
                            type=ex_data["type"],
                            question=ex_data["question"],
                            correct_answer=ex_data["correct_answer"],
                            explanation=ex_data.get("explanation"),
                            order_index=ex_idx,
                            xp=ex_data.get("xp", 2)
                        )
                        db.add(exercise)
                        db.commit()
                        db.refresh(exercise)

                        for opt_text, opt_is_correct in ex_data.get("options", []):
                            option = ExerciseOption(
                                exercise_id=exercise.id,
                                text=opt_text,
                                is_correct=opt_is_correct
                            )
                            db.add(option)
                        db.commit()

        # Seed initial progress for default learner Alex
        # Skill 1 (Greetings) is completed (2/2 lessons, 1 crown)
        # Skill 2 (Food & Drink) is available (in_progress, 0/2 lessons)
        # Remaining skills are locked
        print("Setting initial progression for learner Alex...")
        for idx, skill in enumerate(all_created_skills):
            if idx == 0:
                # Skill 1 completed
                prog = UserSkillProgress(
                    user_id=alex.id,
                    skill_id=skill.id,
                    status="completed",
                    xp=20,
                    crown_level=1,
                    completed_lessons=len(skill.lessons)
                )
                db.add(prog)
                # Add completed lesson attempts for history
                for l in skill.lessons:
                    db.add(LessonAttempt(
                        user_id=alex.id,
                        lesson_id=l.id,
                        started_at=datetime.now(timezone.utc) - timedelta(days=1),
                        completed_at=datetime.now(timezone.utc) - timedelta(days=1),
                        score=100,
                        correct_answers=6,
                        wrong_answers=0,
                        xp_earned=22,
                        hearts_lost=0,
                        completed=True
                    ))
            elif idx == 1:
                # Skill 2 is unlocked & available to play
                prog = UserSkillProgress(
                    user_id=alex.id,
                    skill_id=skill.id,
                    status="available",
                    xp=0,
                    crown_level=0,
                    completed_lessons=0
                )
                db.add(prog)
            else:
                # Rest are locked
                prog = UserSkillProgress(
                    user_id=alex.id,
                    skill_id=skill.id,
                    status="locked",
                    xp=0,
                    crown_level=0,
                    completed_lessons=0
                )
                db.add(prog)

        # Grant Alex "First Step", "Wildfire", and "Scholar" achievements
        first_step_ach = next((a for a in created_achievements if a.requirement_type == "first_lesson"), None)
        if first_step_ach:
            db.add(UserAchievement(user_id=alex.id, achievement_id=first_step_ach.id, unlocked_at=datetime.now(timezone.utc) - timedelta(days=2)))

        wildfire_ach = next((a for a in created_achievements if a.requirement_type == "streak"), None)
        if wildfire_ach:
            db.add(UserAchievement(user_id=alex.id, achievement_id=wildfire_ach.id, unlocked_at=datetime.now(timezone.utc) - timedelta(days=1)))

        scholar_ach = next((a for a in created_achievements if a.requirement_type == "xp"), None)
        if scholar_ach:
            db.add(UserAchievement(user_id=alex.id, achievement_id=scholar_ach.id, unlocked_at=datetime.now(timezone.utc) - timedelta(days=1)))

        db.commit()
        print("Database seeded successfully with rich Spanish curriculum and initial progress!")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
