import json
from flask import Flask, render_template, request, redirect, url_for

def init_app(app):
    def carregar_alunos():
        try:
            with open("alunos.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def salvar_alunos(alunos):
        with open("alunos.json", "w", encoding="utf-8") as f:
            json.dump(alunos, f, ensure_ascii=False, indent=4)

    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            matricula = request.form.get("matricula")
            senha = request.form.get("senha")

            alunos = carregar_alunos()
            for aluno in alunos:
                if aluno["matricula"] == matricula and aluno["senha"] == senha:
                    if aluno["acesso"] == "admin":
                        return redirect(url_for("admin"))
                    else:
                        return redirect(url_for("visualizar"))
            return "<h2>Login inválido!</h2><a href='/'>Voltar</a>"

        return render_template("login.html")

    @app.route("/admin", methods=["GET", "POST"])
    def admin():
        if request.method == "POST":
            escolha = request.form.get("escolha")
            if escolha == "cadastrar":
                return redirect(url_for("cadastrar"))
            else:
                return redirect(url_for("visualizar"))
        return render_template("admin.html")

    @app.route("/cadastrar", methods=["GET", "POST"])
    def cadastrar():
        if request.method == "POST":
            nome = request.form.get("nome")
            matricula = request.form.get("matricula")
            senha = request.form.get("senha")

            alunos = carregar_alunos()
            novo = {"nome": nome, "matricula": matricula, "senha": senha, "acesso": "comum"}
            alunos.append(novo)
            salvar_alunos(alunos)

            return redirect(url_for("visualizar"))

        return render_template("cadastrar.html")

    @app.route("/visualizar")
    def visualizar():
        alunos = carregar_alunos()
        return render_template("visualizar.html", alunos=alunos)
