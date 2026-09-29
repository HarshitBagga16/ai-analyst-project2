from analyzer import analyze_csv
from llm import ask_llm


file_path = "dataset/sales.csv"

df, results = analyze_csv(file_path)

question = input("\nAsk a question about the dataset: ")

answer = ask_llm(question, results)

print("\n===== AI ANALYSIS =====")
print(answer)