from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session

changelog = Blueprint('changelog', __name__)

@changelog.route('/')
def index():
    #give update.md to the template
    with open('update.md') as f:
        update = f.read()
    return render_template('changelog.html', update=update)
