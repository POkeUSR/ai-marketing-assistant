import os
import streamlit as st
import openai
import random
from prompt_templates import PROMPT_MODELS

# Настройка OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI-креативы", page_icon="🎯", layout="centered")
st.title("🎯 AI‑генератор креативов по 13 технологиям продающего текста")

# Кнопка помощи
if st.button("ℹ Как это работает"):
    st.session_state.show_help = not st.session_state.get("show_help", False)

if st.session_state.get("show_help", False):
    st.markdown("---")
    st.markdown("## ❓ Как работает AI-ассистент")
    st.markdown("""
    1. **Введите:**
       - 🎯 ЦА
       - 💢 Проблему
       - 📦 Продукт

    2. **Выберите модель копирайтинга**
    3. **Нажмите “Сгенерировать”**
    """)
    st.markdown("---")

# Случайные портреты
random_profiles = [
    {"audience": "Молодая мама, 28 лет", "problem": "Устаёт и не успевает следить за домом", "product": "Робот-пылесос"},
    {"audience": "Фрилансер-дизайнер, 32 года", "problem": "Нет личного бренда", "product": "Курс по брендингу"},
]

if st.button("🎲 Случайный портрет клиента"):
    profile = random.choice(random_profiles)
    st.session_state["audience"] = profile["audience"]
    st.session_state["problem"] = profile["problem"]
    st.session_state["product"] = profile["product"]

audience = st.text_input("👥 Целевая аудитория", value=st.session_state.get("audience", ""))
problem = st.text_area("💢 Проблема клиента", value=st.session_state.get("problem", ""))
product = st.text_input("📦 Продукт/услуга", value=st.session_state.get("product", ""))

model_option = st.selectbox("📌 Модель копирайтинга", ["Сгенерировать по всем"] + list(PROMPT_MODELS.keys()))

if st.button("🚀 Сгенерировать креатив"):
    with st.spinner("Генерация текста..."):
        system_prompt = (
            f"Ты — копирайтер. На основе информации:\n"
            f"- Аудитория: {audience}\n"
            f"- Проблема: {problem}\n"
            f"- Продукт: {product}\n"
        )

        if model_option == "Сгенерировать по всем":
            for model_name, model_prompt in PROMPT_MODELS.items():
                full_prompt = system_prompt + model_prompt + """
Сформируй креатив:
1. Заголовок — до 56 символов
2. Оффер — до 81 символ
3. Призыв — до 50 символов
4. Описание — до 81 символа для Яндекс Директ
"""
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": full_prompt}]
                )
                answer = response.choices[0].message.content
                st.subheader(model_name)
                st.markdown(f"```text\n{answer}\n```")
        else:
            model_prompt = PROMPT_MODELS[model_option]
            full_prompt = system_prompt + model_prompt
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": full_prompt}]
            )
            answer = response.choices[0].message.content
            st.markdown("### ✨ Результат:")
            st.markdown(f"```text\n{answer}\n```")

# Блок отзыва
with st.expander("💬 Мне не хватает..."):
    st.markdown("Что добавить в ассистент? Напиши 👇")
    feedback = st.text_area("Ваше предложение")
    user_email = st.text_input("Почта (необязательно)")
    if st.button("📨 Отправить отзыв"):
        with open("feedback_log.txt", "a", encoding="utf-8") as f:
            f.write(f"Отзыв:\n{feedback}\nEmail: {user_email}\n---\n")
        st.success("Спасибо за ваш отзыв!")
        
        st.markdown("---")
        st.markdown("---")
# Кнопка заказать настройку
st.markdown(
    """
    <div style='text-align: center; font-size: 16px; margin-top: 30px;'>
        <a href="https://promarketer.tilda.ws/" target="_blank" style="text-decoration: none; color: #1f77b4;">
            👉 Заказать настройку Яндекс Директ
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

                
