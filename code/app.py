import os
from flask import Flask, session, render_template, request, flash, redirect
#from sqlalchemy.exc import IntegrityError??
from models import db, connect_db, User, Review, Favorite
import requests
from forms import UserSignupForm, UserLoginForm, UserReviewForm
CURR_USER_KEY = "curr_user"

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///cocktails'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']='mySecret'

app.app_context().push()
connect_db(app)
db.create_all()


@app.route('/')
def landingPage():
    '''homepage with general search functionality'''
    return render_template('home.html')



@app.route('/get_drink', methods=['POST'])
def call_by_drink():
    drink =request.form['drink']
    api_url = f'http://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink}'
    response = requests.get(api_url)
    data=response.json()
    # drink_name=data['drinks'][0]
    # drinks = data.get('drinks', [])
    drink=data['drinks'][0]
    print(drink)
    reviews = Review.query.filter_by(drinkname=drink['strDrink']).all()
    drink_details = []
    for i in range(1, 16):  # Assuming there are 15 ingredients
        ingredient = drink.get(f'strIngredient{i}', '')
        if ingredient:
            details = [ingredient]
            measure = drink.get(f'strMeasure{i}', '')
            if measure:
                details.append(measure)
            drink_details.append(details)

            print(drink_details)
    return render_template('drink_search.html', drink=drink, drink_details=drink_details, reviews=reviews)

@app.route('/get_drink_with_ingredient')
def get_drink_using_ingredient():
    drink=request.args['drink']
    api_url = f'http://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink}'
    response = requests.get(api_url)
    data=response.json()
    # drink_name=data['drinks'][0]
    # drinks = data.get('drinks', [])
    drink=data['drinks'][0]
    print(drink)
    reviews = Review.query.filter_by(drinkname=drink['strDrink']).all()
    print(reviews)
    drink_details = []
    for i in range(1, 16):
        ingredient = drink.get(f'strIngredient{i}', '')
        if ingredient:
            details = [ingredient]
            measure = drink.get(f'strMeasure{i}', '')
            if measure:
                details.append(measure)
            drink_details.append(details)
            print(drink_details)
    return render_template('drink_search.html',drink=drink, drink_details=drink_details, reviews=reviews)



@app.route('/use_ingredient/', methods=['POST'])
def call_by_ingredient():
    ingredient=request.form['ingredient']
    api_url = f'http://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredient}'
    response = requests.get(api_url)
    data=response.json()
    drink=data['drinks']
    print(drink)
    return render_template('drink_by_ingredient.html', drink=drink)



@app.route('/random_drink')
def get_random_drink():
    api_url = f'http://www.thecocktaildb.com/api/json/v1/1/random.php'
    response = requests.get(api_url)
    data = response.json()
    drink=data['drinks'][0]
    drink_details = []
    for i in range(1, 16):  # Assuming there are 15 ingredients
        ingredient = drink.get(f'strIngredient{i}', '')
        if ingredient:
            details = [ingredient]
            measure = drink.get(f'strMeasure{i}', '')
            if measure:
                details.append(measure)
            drink_details.append(details)

            print(drink_details)
    reviews = Review.query.filter_by(drinkname=drink['strDrink']).all()
    return render_template('random_drink.html', drink=drink, drink_details=drink_details, reviews=reviews)
    
    # if reviews:
    #     return render_template('random_drink.html', drink=drink, drink_details=drink+details, reviews=reviews)
    # else:
    #     return render_template('random_drink.html', drink=drink, drink_details=drink_details)
    # return render_template('random_drink.html', drink=drink, drink_details=drink_details)


@app.route('/user_get_drink/<int:user_id>', methods=['POST'])
def user_call_by_drink(user_id):
    user = User.query.get_or_404(user_id)
    drink =request.form['drink']
    api_url = f'http://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink}'
    response = requests.get(api_url)
    data=response.json()
    # drink_name=data['drinks'][0]
    # drinks = data.get('drinks', [])
    drink=data['drinks'][0]
    print(drink)
    reviews = Review.query.filter_by(drinkname=drink['strDrink']).all()
    print(reviews)
    drink_details = []
    for i in range(1, 16):
        ingredient = drink.get(f'strIngredient{i}', '')
        if ingredient:
            details = [ingredient]
            measure = drink.get(f'strMeasure{i}', '')
            if measure:
                details.append(measure)
            drink_details.append(details)
            print(drink_details)
    return render_template('user_drink_search.html',user=user, drink=drink, drink_details=drink_details, reviews=reviews)



@app.route('/user_use_ingredient/<int:user_id>', methods=['POST'])
def user_call_by_ingredient(user_id):
    user = User.query.get_or_404(user_id)
    ingredient=request.form['ingredient']
    api_url = f'http://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredient}'
    response = requests.get(api_url)
    data=response.json()
    drink=data['drinks']
    print(drink)
    return render_template('user_drink_by_ingredient.html', user=user, drink=drink, ingredient=ingredient)



@app.route('/user_get_drink_with_ingredient/<int:user_id>')
def get_drink_from_ingredient(user_id):
    drink=request.args['drink']
    user = User.query.get(user_id)
    api_url = f'http://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink}'
    response = requests.get(api_url)
    data=response.json()
    # drink_name=data['drinks'][0]
    # drinks = data.get('drinks', [])
    drink=data['drinks'][0]
    print(drink)
    reviews = Review.query.filter_by(drinkname=drink['strDrink']).all()
    print(reviews)
    drink_details = []
    for i in range(1, 16):
        ingredient = drink.get(f'strIngredient{i}', '')
        if ingredient:
            details = [ingredient]
            measure = drink.get(f'strMeasure{i}', '')
            if measure:
                details.append(measure)
            drink_details.append(details)
            print(drink_details)
    return render_template('user_drink_search.html',user=user, drink=drink, drink_details=drink_details, reviews=reviews)



@app.route('/user_random_drink/<int:user_id>')
def get_user_random_drink(user_id):
    user = User.query.get_or_404(user_id)
    api_url = f'http://www.thecocktaildb.com/api/json/v1/1/random.php'
    response = requests.get(api_url)
    data = response.json()
    drink=data['drinks'][0]
    print(drink)
    drink_details = []
    for i in range(1, 16):  # Assuming there are 15 ingredients
        ingredient = drink.get(f'strIngredient{i}', '')
        if ingredient:
            details = [ingredient]
            measure = drink.get(f'strMeasure{i}', '')
            if measure:
                details.append(measure)
            drink_details.append(details)
            print(drink_details)
    reviews = Review.query.filter_by(drinkname=drink['strDrink']).all()
    if reviews:
        return render_template('random_drink.html', drink=drink, drink_details=drink_details, reviews=reviews, user=user)
    else:
        return render_template('random_drink.html', drink=drink, drink_details=drink_details, user=user)
    # return render_template('random_drink.html', drink=drink, drink_details=drink_details)



@app.route('/random_drink_details/<drinkname>')
def get_details_of_random_drink(drinkname):
    api_url = f'http://www.thecocktaildb.com/api/json/v1/1/search.php?s={drinkname}'
    userid =request.args['userid']
    response = requests.get(api_url)
    data=response.json()
    # drink_name=data['drinks'][0]
    # drinks = data.get('drinks', [])
    drink=data['drinks'][0]
    print(drink)
    reviews = Review.query.filter_by(drinkname=drink['strDrink']).all()
    print(reviews)
    drink_details = []
    for i in range(1, 16):
        ingredient = drink.get(f'strIngredient{i}', '')
        if ingredient:
            details = [ingredient]
            measure = drink.get(f'strMeasure{i}', '')
            if measure:
                details.append(measure)
            drink_details.append(details)
            print(drink_details)
    return render_template('user_drink_search.html',userid=userid, drink=drink, drink_details=drink_details, reviews=reviews)



@app.route('/signup')
def go_to_add_user_page():
    form = UserSignupForm()
    return render_template("signup.html", form=form)



@app.route('/store_user', methods=['POST'])
def storeUserInfo():
    # if CURR_USER_KEY in session:
    #     del session[CURR_USER_KEY]
    ########################################
    form = UserSignupForm()
    if form.validate_on_submit():
        user = User.signup(username=form.username.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        password=form.password.data)
        db.session.commit()
############################################
    return redirect(f'/user_page/{user.id}')



@app.route('/login_page')
def go_to_login_page():
    form = UserLoginForm()
    return render_template('login_page.html', form=form)



@app.route('/login_user', methods=['POST'])
def login_user():
    form = UserLoginForm()
    if form.validate_on_submit():
        # user = User.login(form.username.data,
        #                          form.password.data)
        user = User.login(username=form.username.data, password=form.password.data)
        if user:
            session[CURR_USER_KEY] = user.id
            # flash(f"Hello, {user.username}!", "success")
            return redirect(f"user_page/{user.id}")
        flash("Invalid credentials.", 'danger')
    return render_template('login_page.html', form=form)
 


@app.route('/user_page/<int:user_id>')
def to_user_page(user_id):
    user = User.query.get_or_404(user_id)
    favorites=Favorite.query.filter_by(userid=user_id).all()
    print(favorites)
    reviews = Review.query.filter_by(userid=user_id).all()
    if reviews:
        print(reviews[0].title)
        return render_template('user_page.html', user=user, reviews=reviews, favorites=favorites)
    else:
        return render_template('/user_page.html', user=user, favorites=favorites)



@app.route('/review/<int:user_id>/')
def write_review(user_id):
    drink = request.args['drink']
    form=UserReviewForm()
    print(drink)
    return render_template('review.html', user_id=user_id, drink=drink, form=form)



@app.route('/save_review/<int:user_id>', methods=['POST'])
def save_review(user_id):
    drink=request.args['drink']
    form=UserReviewForm()
    if form.validate_on_submit():
        title=form.title.data
        review=form.review.data
        review=Review(title=title, review=review, userid=user_id, drinkname=drink)
        db.session.add(review)
        db.session.commit()
    return redirect(f'/user_page/{user_id}')



@app.route('/add_favorite', methods=['POST'])
def add_drink_to_favorites():
    userid=request.args['userid']
    drinkname=request.args['drinkname']
    print(drinkname)
    favorite=Favorite(userid=userid, drinkname=drinkname)
    print(favorite)
    db.session.add(favorite)
    db.session.commit()
    return redirect(f'/user_page/{userid}')



@app.route('/edit_user_favorites/<int:user_id>')
def edit_favorites(user_id):
    favorites=Favorite.query.filter_by(userid=user_id).all()
    print(favorites)
    return render_template('edit_favorites.html', favorites=favorites, userid=user_id)



@app.route('/delete_favorite/<int:id>')
def delete_favorite(id):
    userid=request.args['userid']
    favorite = Favorite.query.get(id)
    # favorite=Favorite.query.filter_by(id=id)
    print(favorite)
    db.session.delete(favorite)
    db.session.commit()
    return redirect(f'/user_page/{userid}')