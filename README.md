# c1-SF-Dispatch
Submission for Capital One Software Engineering Summit
The task was to use a given dataset to realize and display trends in San Francisco's Fire and Police department dispatches.

* Challenge: https://www.mindsumo.com/contests/sfpd-dispatch/
* Deployed on Heroku: https://c1-dispatch-predict.herokuapp.com/

## Authors
* **Andrew Li** - [GitHub](https://github.com/ubrandrew)

## Technologies Used
* Python, HTML, CSS, JavaScript
* [Bokeh](https://bokeh.pydata.org/en/latest/) for data visualization
* [MatPlotLib](https://matplotlib.org/) for data visualization
* [Pandas](https://pandas.pydata.org/) for data parsing
* [Folium](https://folium.readthedocs.io/) for heat-map creation
* [scikit-learn](http://scikit-learn.org/stable/) for dispatch prediction model
* [Flask](http://flask.pocoo.org/) for backend development

### Deliverables
- Data Visuals: Display or graph 3 metrics or trends from the data set that are interesting to you.
   * Used pandas and Jupyter notebook to parse the dataset CSV
   * Graphed correlation between time of day and hospital transport times using Bokeh
   * Graphed the frequency of each type of call vs. the time of day using Bokeh
   * Graphed the top responding battalions based on number of dispatch responses using matplotlib

- Given an address and time, what is the most likely dispatch to be required?
   * Attempted this problem using the LinearSVC model from scikit-learn using latitude, longitude, and number of seconds since 00:00:00 as features. Unit_type was used for labels.

- Which areas take the longest time to dispatch to on average? How can this be reduced?
   * Folium generated heatmap displayed the distribution of calls across San Francisco weighted with the amount of time a dispatch arrived.

### Additional Deliverables Implemented
- Heat maps: Add heat maps that show dispatch frequency, urgency over the city.
- Crime correlation: Based on the type of dispatch and the frequency of dispatch, show the most calm and safe neighborhoods in the city

## Future work
   * Machine learning model didn't perform as accurately as I'd expected.
      - One reason I believe is that there was a lot of bias towards certain dispatches (mainly ENGINE and MEDIC).
      - Another reason is the insignificance of latitude and longitude coordinates. Coordinates in the training data were extremely similar in value, only ranging between 33 to 34 North and -122 to 123 West.
