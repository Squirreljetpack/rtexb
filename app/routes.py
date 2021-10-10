from app import app
from flask import render_template, request, jsonify, url_for, redirect
import jinja2
import time

@app.route("/")
def main():
    return "<p>Hello, World!</p>"

@app.route("/mathjax/<encodedtext>")
def mathjax(encodedtext):
    return render_template("mathjax.html",x=encodedtext)

@app.route("/tex/<encodedtext>")
def tex(encodedtext):
    template = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    ).get_template('rendered_tex.tex')
    print(template.render(x=encodedtext))
    time.sleep(3)
    with open('/tex-renders/1.pdf', 'rb') as static_file:
        return send_file(static_file, attachment_filename='rendered_tex.pdf')