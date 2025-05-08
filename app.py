from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import os
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = PromptTemplate.from_template("Tell me a random, interesting, and true fact about {topic}.")

@app.route("/", methods=["GET", "POST"])
def index():
    fact = None
    error = None

    if request.method == "POST":
        topic = request.form.get("topic")
        if not topic:
            error = "Please enter a topic."
        else:
            try:
                chain = prompt | llm
                result = chain.invoke({"topic": topic})
                fact = result.content if hasattr(result, "content") else str(result)
            except Exception as e:
                error = f"Error: {str(e)}"

    return render_template("index.html", fact=fact, error=error)

if __name__ == "__main__":
    app.run(debug=True)




