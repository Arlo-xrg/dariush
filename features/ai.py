from groq import Groq

client = Groq(api_key="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")


messages_history = [
    {
        "role": "system", 
        "content": "You are Jarvis, a highly intelligent, witty, and helpful AI assistant. Keep your answers concise, professional, and powerful. you sed just a very shor ansowr  im from iran"
        
    }
]
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break
        
    messages_history.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=messages_history
        )
        
        bot_reply = response.choices[0].message.content
        print(f"\nJarvis: {bot_reply}\n")
        print("-" * 50)
        
        messages_history.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        print(f"Error: {e}")