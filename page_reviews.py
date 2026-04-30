from tlbx_imports import *
from ui_toolbox import *
from db_actions import *


def submit_review(movie_options, movie_choice, rating, review_text, user_id):
#must be logged in
    if user_id is None:
        ui.notify('You must be logged in to review')
        return

#validation for the review table
    if movie_choice.value is None:
        ui.notify('Pick a movie')
        return



    if not rating.value:
        ui.notify('Enter a rating')
        return



    try:
        rating_num = int(rating.value)
    except ValueError:
        ui.notify('Rating must be a number')
        return




    if not 1 <= rating_num <= 5:
        ui.notify('Rating must be between 1 and 5')
        return

    try:
        selected_movie_id = movie_options[movie_choice.value]

        add_review(
            int(user_id),
            int(selected_movie_id),
            rating_num,
            review_text.value
        )

        ui.notify('Review added')

#refreshs page to see updated table
        ui.navigate.to('/reviews')

    except Exception as e:
        ui.notify(f'Error: {e}')


@ui.page('/reviews')
def reviews():
    uit_banner()

#get the logged in user
    user_id = app.storage.user.get('user_id', None)

#get movies for dropdown table
    movies = get_movie_options()


#creates a list of movies matches the title with id
    movie_options = { movie['title']: movie['movie_id']
                      for movie in movies }

    with ui.card():
        ui.label('Add Review')
        if user_id is None:
            ui.label('You must be logged in to make a review.')
            ui.button('Go to Login', on_click=lambda: ui.navigate.to('/login'))

#select makes a dropdown table put movie_option into the dropdown
        else:
            movie_choice = ui.select( options=list(movie_options.keys()),   label='Movie')

            rating = ui.input('Rating  (1-5)')
            review_text = ui.textarea('Review')

            ui.button(
                'Submit Review ',
                on_click=lambda: submit_review(
                    movie_options, movie_choice, rating, review_text, user_id
                )
            )

#get the reviews
    try:
        rows = get_all_reviews()
    except Exception as e:
        rows = []
        ui.notify(f'Could not load reviews: {e}')

#table columns
    columns = [
        {'name': 'username', 'label': 'Reviewer', 'field': 'username'},
        {'name': 'title', 'label': 'Movie', 'field': 'title'},
        {'name': 'rating', 'label': 'Rating', 'field': 'rating'},
        {'name': 'review_text', 'label': 'Review', 'field': 'review_text'},
        {'name': 'created_at', 'label': 'Date', 'field': 'created_at'},
    ]


# display the reviews we got on table

    with ui.card():
        ui.label('All Reviews')
        ui.table(columns=columns, rows=rows).style('width: 73vw')

    uit_footnote()