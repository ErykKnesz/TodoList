from flask import Flask, request, render_template, redirect, url_for
from forms import TodoForm
from models import todos


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/todos/", methods=["GET", "POST"])
def todos_list():
    form = TodoForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            todos.create(form.data)
        return redirect(url_for("todos_list"))

    return render_template(
        "todos.html",
        form=form,
        todos=todos.all(),
        error=error)


@app.route("/todos/<int:todo_id>/", methods=["GET", "POST"])
def todo_details(todo_id):
    todo = todos.get(todo_id)
    todo_id, title, description, done = todo
    todo = {
        'title': title,
        'description': description,
        'done': done
    }
    form = TodoForm(data=todo)
    if request.method == "POST":
        if form.validate_on_submit():
            todos.update(todo_id, form.data)
        return redirect(url_for("todos_list"))
    return render_template("todo.html", form=form, todo_id=todo_id)


@app.route("/todos/delete/<int:todo_id>/", methods=["GET"])
def todo_delete(todo_id):
    todos.delete(todo_id)
    return redirect(url_for("todos_list"))


if __name__ == "__main__":
    app.run(debug=True)
