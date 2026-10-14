from app.agent.agent import ask_agent

print("\n--- ORDER ---")
print(ask_agent("What is the status of order 1?"))

print("\n--- TICKET ---")
print(ask_agent("What is the status of ticket 1?"))

print("\n--- POLICY ---")
print(ask_agent("My package arrived broken. What should I do?"))