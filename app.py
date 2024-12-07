import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters



st.header('Personalized Movie Recommendation System')

# Load movie data and similarity matrix
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

# Search bar for movie input
selected_movie = st.text_input(
    "Type a movie name to get recommendations",
    placeholder="Enter a movie name..."
)

if st.button('Show Recommendation'):
    if selected_movie:  # Check if user has entered a movie
        try:
            # Strip and lowercase the input for case-insensitive matching
            selected_movie = selected_movie.strip().lower()
            movie_titles = movies['title'].str.lower()  # Lowercase the dataset movie titles

            # Find movies that contain the entered text
            matched_movies = movies[movie_titles.str.contains(selected_movie, na=False)]

            if matched_movies.empty:
                st.warning("Movie not found! Please check the spelling or try another movie.")
            else:
                # Use the first match for recommendations (or let user choose if needed)
                matched_movie = matched_movies.iloc[0]
                matched_movie_title = matched_movie['title']
                matched_movie_id = matched_movie['movie_id']

                # Fetch the poster for the selected movie
                selected_movie_poster = fetch_poster(matched_movie_id)

                # Display the selected movie
                st.subheader("Selected Movie")
                col = st.columns(3)[1]  # Center-align the movie display
                with col:
                    st.image(selected_movie_poster, caption=matched_movie_title, use_column_width=True)

                # Get recommendations
                recommended_movie_names, recommended_movie_posters = recommend(matched_movie_title)

                # Handle empty recommendations
                if not recommended_movie_names:
                    st.warning("No recommendations found for this movie. Please try another one.")
                else:
                    # Display recommendations
                    st.subheader("Recommended Movies")
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.text(recommended_movie_names[0])
                        st.image(recommended_movie_posters[0])
                    with col2:
                        st.text(recommended_movie_names[1])
                        st.image(recommended_movie_posters[1])
                    with col3:
                        st.text(recommended_movie_names[2])
                        st.image(recommended_movie_posters[2])
                    with col4:
                        st.text(recommended_movie_names[3])
                        st.image(recommended_movie_posters[3])
                    with col5:
                        st.text(recommended_movie_names[4])
                        st.image(recommended_movie_posters[4])
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a movie name to get recommendations.")
