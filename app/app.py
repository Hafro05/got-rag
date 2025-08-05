import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request
from got_rag.loader import load_and_split
from got_rag.embedder import create_vectorstore
from got_rag.rag_chain import build_qa_chain

app = Flask(__name__)
docs = load_and_split("data/got.txt")
vectorstore = create_vectorstore(docs)
qa_chain = build_qa_chain(vectorstore)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    if request.method == "POST":
        question = request.form.get("question", "")
        if question:
            result = qa_chain.run(question)
            answer = result
    return render_template("index.html", question=question, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
