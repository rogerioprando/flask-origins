import uuid

from flask import Blueprint, render_template, redirect, url_for, flash, abort, request

website = Blueprint('website', __name__)


@website.errorhandler(404)
def page_not_found(e):
    error_type = 'error'
    flash(e)
    return render_template('404.html', error_type=error_type), 404


@website.errorhandler(500)
def internal_server_error(e):
    error_type = 'error'
    flash(e)
    return render_template('500.html', error_type=error_type), 500


@website.errorhandler(Exception)
def unhandled_exception(e):
    error_type = 'error'
    flash(e)
    return render_template('500.html', error_type=error_type), 500


@website.route('/')
def index():
    return render_template('website/index.html')
