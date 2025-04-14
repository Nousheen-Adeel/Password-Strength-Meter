import re
import streamlit as st
import random

# weak passwords
blacklist = ["password", "123456", "123456789", "password123", "qwerty", "abc123", "111111"]

#custom weighta for scoring
Weights={
    "length":2,
    "case":2,
    "digit":2,
    "special":2
}

def check_password_strength(password):
    score = 0 
    messages = []

    #check if password is blacklisted
    if password.lower() in blacklist:
        messages.append("❌ This password is too common. Please try another.")
        return 0, messages
    
    #check password length
    if len(password) >= 8:
        score += Weights["length"]
    else:
        messages.append("❌ Password must be at least 8 characters.")
    
    #check for uppercase and lowercase letters
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]",password):
        score += Weights["case"]
    else:
        messages.append("❌ Include both uppercase and lowercase letters.")
    
      # Check for digits
    if re.search(r"\d", password):
        score += Weights["digit"]
    else:
        messages.append("❌ Add at least one digit (0-9).")

    # Check for special characters
    if re.search(r"[!@#$%^&*]", password):
        score += Weights["special"]
    else:
        messages.append("❌ Add at least one special character (!@#$%^&*).")

    return score, messages

#Generate a strong random passwrod
def generate_strong_password(length=12):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))
    
#streamlit UI
st.title("🔐 Password Strength Checker")

user_password = st.text_input("Enter Your Password:", type= "password")

if st.button("check password"):
    score, feedback = check_password_strength(user_password)
    max_score = sum(Weights.values())

    if score == max_score:
        st.success("✅ Strong password!")
    elif score >= max_score * 0.6:
        st.warning("⚠️ Moderate password - consider strengthening it.")
    else:
        st.error("❌ Weak password. Suggestions:")
        for msg in feedback:
            st.write(msg)

if st.button("Suggest a Strong Password"):
    suggestion = generate_strong_password()
    st.info(f"Suggested password: `{suggestion}`")

        
