from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session

casaos = Blueprint('casaos', __name__)

@casaos.route('/')
def index():
    return render_template('casaos.html')