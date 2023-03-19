import openai
import os
import json
import pandas as pd
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

openai.api_key = "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" # 替换为你的OpenAI API密钥

def generate_survey_responses(survey_questions, num_responses=20):
    prompt = f"以下是一份问卷调查：\n\n{survey_questions}\n\n请根据问卷内容自行判断扮演合适的角色，完成20份问卷调查。每份问卷回答请用'问卷:'为开头。\n"

    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=num_responses,
        stop=None,
        temperature=0.7,
    )

    responses = [choice.text.strip() for choice in completions.choices]
    return responses


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        survey_questions = request.form["survey_questions"]
        prompt = f"请根据问卷内容自行判断扮演合适的角色，完成问卷:\n\n{survey_questions}\n回答："
        responses = generate_survey_responses(prompt)

        data = {
            "Questions": [survey_questions] * 20,
            "Responses": responses,
        }

        df = pd.DataFrame(data)
        df.to_excel("survey_responses.xlsx", index=False)

        return send_file("survey_responses.xlsx", as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)