# Predicting Lead Contamination in New York Schools

Project completed for Erdos institute data science bootcamp (fall-2025)

### Team members
1. [Cami Goray]
2. [Hana Lang](https://github.com/hlang-3304)
3. [Ranadeep Roy]


## Project overview
We developed a comprehensive analysis to predict the presence of lead contamination in New York school drinking water using a rich dataset of demographic, socioeconomic, infrastructural, and geographic features. We obtained our main dataset from New York’s Department of Health. Our target variable is a binary: 1 if there is a drinking outlet with above five parts per billion (>5 ppb) lead contamination, and 0 if there are no such drinking outlets. This level is recommended by the New York Public Health Law, which governs school potable water testing standards.

## Stakeholders
Our primary stakeholders are education administrators in the State of New York, as well as the NY State Department of Health, New York Schools, and NY parents and families of schoolchildren, as this project aims to predict lead contamination and therefore improve safety of school facilities. 

## Modeling approach
The dataset was split into training and testing sets, with 20% of the data set aside as the final test set. For each model, we performed hyperparameter tuning with nested cross validation using random search. Models were considered in increasing order of complexity: logistic regression (with and without penalty), decision trees, support vector machines, random forest, AdaBoost and XGBoost. All the models were evaluated on the basis of mean ROC-AUC scores. This metric was chosen because our dataset was nearly balanced and we wanted to ensure that our model can distinguish between the two classes well.

## Results
1. Hyperparameter-tuned logistic regression model produced the best mean AUC score in the training stage, with an average ROC-AUC score of 0.7621 across the five outer folds of the nested cross-validation.
2. On the final test set we obtained an ROC-AUC score of 0.7278 on the validation set using the Logistic Regression with penalty and the best hyperparameters found in the training stage.
![county-wide heat map](model_comparison/final_model_cm.png)
4. Feature importance analysis based on permutation importance methods indicates that the most important features of a school were: 
    -   (a) school district of NYC Department of Education
    -   (b) the proportion of white students 
    -   (c) the proportion of Hispanic students 
    -   (d) a city location of Staten Island 
    -   (e) a city location of Brooklyn. 

Based on EDA, we had expected geographical features to appear as important predictors (see the county-wide heat map displaying the proportion of schools with target variable 

![county-wide heat map](eda_and_images/county_map.png)

## Conclusion and future directions
1. Geographical features (school district and city) are strong predictors of whether or not a school has lead-contaminated water. In further work, we would explore other features capturing why location plays a critical role in lead detection.
2. To investigate why location plays a critical role, we would include incorporating spatial modeling to identify “hotspots” of elevated lead levels, including water system maps and pollution metrics. We would also hope to obtain institution-specific building age for future modeling, rather than using a county-wide metric.
3. Obtain more socioeconomic data, for example school board funding, with the hypothesis that better funded schools serving wealthier students might be more likely to have already addressed elevated lead levels in drinking water.
4. Finally, lead contamination in school drinking water is not a problem limited to New York State. In future work, we would look to expand modeling to include other states. 


## Folder organization
