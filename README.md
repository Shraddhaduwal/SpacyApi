# SpacyApi

The SpacyApi is the restful-Api that helps in easy interactions between the end users and the server. This is made with the help of flask, flask-restful, flask-sqlalchemy. Here, different types of operations are done to clean the text(for preprocessing) and find about the properties of the text like their part_of_speece, dependencies, and so on

## Routes
1. GET /data/<string:text_id> : This route helps in getting all the text of a certain `text_id` from the database. `text descriptions` can be added to body and `text_id` should be passed in the url. If `text_id` doesn't exist then it will be informed.
2. GET /plot/<string:csv_filename> : This route is for getting the graph plots of the given csv file. The `csv_filename` should be passed in the url to get the plots. The available `csv_filename` are:
- `adj_frequency.csv`
- `adj_noun_frequency.csv`
- `name_frequency.csv`
- `noun_adj_frequency.csv`
- `noun_frequency.csv`
- `noun_noun_phrase_frequency.csv`
- `verb_frequency.csv`
3. POST /data/<string:text_id> : This route is for posting the data ie `text_description` to the database.  If `text_id` already exists or doesn't exist then it will be informed.
4. PUT /data/<string:text_id> : This route is for updating the `text_description` of the particular `text_id`. If `text_id` doesnot exist, it will be informed.
5. DELETE /data/<string:text_id> : This route is for deleting the text of particular `text_id`.  If `text_id` doesnot exist, it will be informed.
