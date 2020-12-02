import recommendition_funcs as gr
# import goodreads_api_client as gr


"""
'average_rating', 'num_pages', 'format', 'edition_information', 'ratings_count', 'text_reviews_count', 'url', 'link', 'authors', 'reviews_widget', 'popular_shelves', 'book_links', 'buy_links', 'series_works'])
"""

if __name__ == '__main__':
    print( gr.get_book_title_from("Best") )
    # print( get_book_genre( get_book_id( 'Best Mystery Books' ) ) )
