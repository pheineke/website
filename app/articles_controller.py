from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session

articles = Blueprint('articles', __name__)




articles = [
    {
        "title" : "Congo takes on Apple",
        "url" : "https://www.fairplanet.org/story/congo-lawsuit-apple-minerals-child-labour-iphone/",
        "embed" : '<a id="republish_embed" href="https://www.fairplanet.org/story/congo-lawsuit-apple-minerals-child-labour-iphone/" target="_blank" data-id="58672" data-pid="19ab23eaf68407f84b4638a29ee62c54" data-headline="1">Embed from FairPlanet</a><script src="https://www.fairplanet.org/republish.js" charset="utf-8" async></script>',
        "content" : '0001.html'
    }
]

@articles.route('/')
def index():

    return render_template('articles.html')