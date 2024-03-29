from flask import Flask, request, render_template, redirect, url_for
from config import Config
from app import routes

app = Flask(__name__)
app.config.from_object(Config)