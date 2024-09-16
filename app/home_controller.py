from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session

home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('home.html')