import streamlit as st
from prompt_templates import PROMPT_MODELS
import openai

# Настройка клиента OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Кнопка с флагом
if st.button("ℹ Как это работает"):
    st.session_state.show_help = not st.session_state.get("show_help", False)

# Условный блок — псевдо-popup
if st.session_state.get("show_help", False):
    st.markdown("---")
    st.markdown("## ❓ Как работает AI-ассистент")
    st.markdown("""
    1. **Введите:**
       - 🎯 ЦА (например: молодая мама, бизнесмен, подросток и т.д.)
       - 💢 Проблему (что беспокоит клиента)
       - 📦 Ваш продукт/услугу

    2. **Выберите модель копирайтинга:**
       - AIDA, PAS, BAB, 4U и другие

    3. **Нажмите “Сгенерировать”**

    4. 🤖 AI-ассистент создаст:
       - Заголовок
       - Оффер
       - Призыв к действию
       - Описание под рекламу Яндекс Директ
 
    """)
    st.markdown("---")



st.set_page_config(page_title="AI-креативы для маркетинга", page_icon="🎯", layout="centered")

st.title("🎯 AI‑генератор креативов по 13 технологиям продающего текста")


import random

# 🎲 Список случайных портретов
random_profiles = [
    {
        "audience": "Молодая мама, 28 лет",
        "problem": "Устаёт и не успевает следить за домом",
        "product": "Робот-пылесос с голосовым управлением"
    },
    {
        "audience": "Фрилансер-дизайнер, 32 года",
        "problem": "Нужен поток заказов, но нет личного бренда",
        "product": "Онлайн-курс по личному бренду"
    },
    {
        "audience": "Предприниматель, 45 лет",
        "problem": "Много рутинных задач отнимает время",
        "product": "AI-ассистент для бизнеса"
    },
    {
        "audience": "Школьник, 15 лет",
        "problem": "Сложно понять алгебру",
        "product": "Геймифицированный курс по математике"
    },
]

# 🔁 Кнопка генерации случайного примера
if st.button("🎲 Случайный портрет клиента"):
    profile = random.choice(random_profiles)
    st.session_state["audience"] = profile["audience"]
    st.session_state["problem"] = profile["problem"]
    st.session_state["product"] = profile["product"]

# 📥 Поля ввода с автозаполнением из session_state
audience = st.text_input("👥 Целевая аудитория", value=st.session_state.get("audience", ""))
problem = st.text_area("💢 Проблема или боль клиента", value=st.session_state.get("problem", ""))
product = st.text_input("📦 Продукт/услуга", value=st.session_state.get("product", ""))


model_option = st.selectbox("📌 Выберите модель копирайтинга", ["Сгенерировать по всем"] + list(PROMPT_MODELS.keys()))

if st.button("🚀 Сгенерировать креатив"):
    with st.spinner("Генерация текста..."):
        system_prompt = (
            f"Ты — профессиональный копирайтер. На основе информации:\n"
            f"- Аудитория: {audience}\n"
            f"- Проблема: {problem}\n"
            f"- Продукт: {product}\n"
        )

        if model_option == "Сгенерировать по всем":
            for model_name, model_prompt in PROMPT_MODELS.items():
                full_prompt = system_prompt + f"{model_prompt}\nСформируй креатив в формате:\n1. Заголовок — максимум 56 символов\n2. Оффер — максимум 81 символ\n3. Призыв к действию — до 50 символов\n4. Описание — до 81 символа, подходит для Яндекс Директ\n\nПиши чётко, конкретно, по делу. Без воды и общих слов."
                client = openai.OpenAI(api_key=openai.api_key)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": full_prompt}]
                )
                answer = response.choices[0].message.content
                st.subheader(model_name)
                st.markdown(f"```text\n{answer}\n```")
        else:
            model_prompt = PROMPT_MODELS[model_option]
            full_prompt = system_prompt + f"{model_prompt}\nСоздай креатив в формате: заголовок, оффер, призыв, описание для Яндекс Директ."
            client = openai.OpenAI(api_key=openai.api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": full_prompt}]
            )
            answer = response.choices[0].message.content
            st.markdown("### ✨ Результат:")
            st.markdown(f"```text\n{answer}\n```")
            
            
            import streamlit as st

with st.expander("💬 Мне не хватает..."):
    st.markdown("Если вам чего-то не хватает в этом ассистенте — напишите, и я постараюсь это добавить 🙌")
    feedback = st.text_area("Что бы вы хотели добавить?", placeholder="Например: экспорт в PDF, больше шаблонов, автоподбор картинок...")
    user_email = st.text_input("Ваша почта (необязательно)", placeholder="example@mail.com")

    if st.button("📨 Отправить отзыв"):
        with open("feedback_log.txt", "a", encoding="utf-8") as f:
            f.write(f"Отзыв:\n{feedback}\nEmail: {user_email}\n---\n")
        st.success("Спасибо! Ваше сообщение получено 🙏")

