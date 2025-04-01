# Population Pyramid of Spain
#### Author: Juan José Carrasco Fernández
#### Date: 01/04/2025
### Description:
#### Introduction:

This README file outlines the Population Pyramid of Spain, a Dash app designed to visualize demographic data from 1970 to 2023. This app allows users to observe demographic trends over the years, revealing how the proportion of children in the population has decreased while the group of older adults has increased, which may inform future social and economic challenges.

#### Dataset:

The dataset used in this project is a JSON file containing disaggregated data by gender, age and date from 1970 to 2023. You can download the dataset from [ine](https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736177095&menu=ultiDatos&idp=1254735572981).

#### Libraries:

The required libraries are listed in the *requirements.txt* file. The app uses the Pandas library to load and process the data, while the Plotly and Dash libraries are employed to create the app's visualizations and interactivity.

#### Features

The app initially displays Spain's population pyramid in 1970. Population data is presented disaggregated by age and gender, along with the total population. Users can change the displayed year using a slider, and pressing the play button activates an animation that automatically scrolls through the years.
