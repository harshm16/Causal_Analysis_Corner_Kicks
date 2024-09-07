## Welcome to the Code Repo. for "A Causal Analysis of Corner Kicks"

#### Refer `Opta Forum 2024 Presentation.pptx` to go through the results in brief.
#### The video presentation is available on [Opta's website](https://www.statsperform.com/2024-opta-forum-session-videos/?mkt_tok=MjI3LUVJWS0zMzEAAAGSgNDAkXv6AQ3iBeIWs6saQ7GR6DrVTLmHZmX6B1A6MFMjVr0GQwcmXt5ShkTrTgjRlx7Kd0EV-pLlGTnN-M6CpFa3LqHQvPyLG_t4wA1f1HB5fGPU#:~:text=19%3A27-,A%20Causal%20Analysis%20of%20Corner%20Kicks%20%E2%80%93%20Harsh%20Mishra,-19%3A57) as well.


# Repository structure -:

* analysis
    * Analysis.ipynb
    * ate_causalmodel.ipynb
    * classifier_all_features.ipynb
    * configs.py
    * Intervention.ipynb

* data
    * extracted tracking data : 
        * Due to Opta's copy rights, the tracking data is not publicly shareable.
        
    * corner_timeelapsed_store.json
    * dtype.csv
    * event_names.csv
    * features.csv
    * notears_point2.gexf
    * qualifier_names.csv

* data_extraction
    * Attacking Setup Cluster.ipynb
    * Closely Marked.ipynb
    * Defense Type Cluster.ipynb
    * Dynamic Movement.ipynb

* figures
    * Figures from results of above notebooks


# Data Extraction Process -:

We extract the following 6 features from the combination of Opta's tracking and events data. Extracted data can be accessed from the above mentioned google drive link. The notebooks used to extract the data are `Extract data.ipynb` and `Extract data filtered.ipynb`.

#### Already recorded in the data -:

* Shot Attempt:
    * 0 – No shot
    * 1 – Goals / Attempt Saved / Miss

* Corner Type:
    * 0 – Inswinger
    * 1 – Outswinger

#### Extracted using Clustering some features -:

* Defense Type:
    * 0 – Man Mark
    * 1 – Zonal

    Gausian Mixture Models were used to find two clusters based on the following 3 features. 
    1) Cost - Distance between attacker & their most closest marker was found using the Linear Sum Assignment problem, using the defensive players (minus Goalkeeper) and attacking players as two different sets.
    2) Number of attackers within 6 yards of goal
    3) Number of defenders within 6 yards of goal
    
    The code to extract all these 3 features and use GMM to model them is present in `Defensive Type Cluster.ipynb`. The notebook also contains codes to use Kmeans as an alternative clustering technique and also has GMM model which uses only the Cost as the feature.

* Attacking Setup:
    * 1 - Players start from near post 
    * 2 - Players make runs from deeper areas to the back post 
    * 3 - Player make two-way movement 
    * 4 - Player make near post runs 

    The code to extract this feature can be found in `Attacking Setup Cluster.ipynb`. Here we follow a similar approach to the research [A Playbook for Corner Kicks](https://www.sloansportsconference.com/research-papers/routine-inspection-a-playbook-for-corner-kicks). Active attackers are first found and then the feature vectors for all the active attackers are computed based on their start and end zones. GMMs were trained on the start and end coordinates of the players to initially find those clusters. How our method differs from their proposed method is in the utilization of these feature vectors of corner kicks to find clusters. Their proposed method uses a Agglomerative Clustering model to cluster the features of all the corner kicks. Although we have the code available to do that in our notebook, we found it harder to comprehend these clusters and then categorize them into clusters that made sense for human understanding. In our approach we use a KMeans cluster to do so, so that we could then use the centers of these clusters to find the start and end locations where most active attackers were found. The player split between each zone can be found in the above mentioned notebook.

#### Extracted using Thresholding the data distribution -:
* Closely Marked:
    * 0 – No
    * 1 – Yes

    The code to extract this feature can be found in `Closely Marked.ipynb`. The distribution of the distances between the active attackers and their closest markers was seen and a threshold of 1.45m (the median of the distribution) was determined as the value to determine whether the players were closely marked or not. The value of this feature is No, if distance of more than half the active attackers was found to be more than the median distance. 


* Dynamic Movement:
    * 0 – No
    * 1 – Yes

    The code to extract this feature can be found in `Dynamic Movement.ipynb`. The frames where the ball started from the corner kick spot, till the time it reached the closest edge of the penalty box were looked at for this feature. If more than half of the active attackers had speed more than the average speed found in the data distribtuion, we conlcude that dynamic movement was made otherwise not.



#### All these features can be found in `features.csv` under the data folder.

# Casual Modelling -:

#### Structure Learning
The notebook `Analysis.ipynb` and the python module `configs.py` contain the code used to learn the graphical structure from our feature set. We use a Structural learning method called NoTears. We put conditions on there being no incoming edge towards our treatment variables (Corner Type & Defense Type) and no outgoing edge from our outcome variables (Shot Attempt). The following extra edges were added on top of the graph predicted by the NoTears algorithm -: Defense Type -> Shot Attempt, Dynamic Movement -> Shot Attempt, Closely Marked -> Shot Attempt and Attacking Setup -> Shot Attempt.


![casual graph.png](<figures/casual graph.png>)


#### Traditional Modelling
The notebook `classifier_all_features.ipynb` contains the code to train a Random Forest Classifier to predict Shot Attempts using all other features, except Attacking Setup.


#### Non-Parametric Causal Modelling
The notebook `ate_causalmodel.ipynb` contains the code to find the Average Treatment Effect of all variables on Shot Attempt, while conditioning on confounders.


#### Parametric Causal Modelling
The notebook `Intervention.ipynb` contains the code to use a parametric approach for causal modelling. Here we train parametric models for each node using their respective feature sets (incoming edges). The treatment variables are assumped to be Empirically Distributed, all other covariates having a Random Forest Classifier of their own. These models then allow us to perform interventions, which is setting the value of a variable to something specific & letting other variables respond according to their causal model, based on the parameters learned from the data.

