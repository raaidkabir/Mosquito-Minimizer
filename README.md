## Mosquito Minimizer
---
### 1. Inspiration
In my country, Bangladesh, we have a very serious mosquito issue. These mosquitos carry diseases such as West Nile Virus, Malaria, Zika, and Dengue. Every year, 725,000 people die from mosquito-borne illness year each, and some of my family members are included in these statistics. 

The desire to help my country inspired me to create an application that would help minimize these mosquitoes in a safe way.

### 2. What is Mosquito Minimizer?
This is a tool to help campgrounds, or any kind of population manage their mosquito population by introducing dragonflies. Why dragonflies? Well these creatures are in the middle of the food chain for many areas, and their primary feeding is on mosquitoes. This will allow for the population of the dragonflies to be controlled as well, and not cause some kind of invasive species problem.

### 3. How was this project built?
This project was built using three main libraries: Mesa, numpy, and Tkinter. Mesa was used to create agents, and I was able to model animals using them. These animals could be randomly scheduled to create a psuedo-artificial intelligence. Numpy was mainly used to compute fast calculations. For example, the animal speed to age ratio was modeled by the equation $-(2x+1)^{4} +1 . $

Tkinter was used for GUI purposes. The GUI allows for the user to custom calibrate any kind of parameters for the animal, such as birth rate. This is important because these properties can change based on the regions that the animal exists in.

### 4. Challenges
This project is the first time I have built any kind of GUI on python, therefore, I exhibited many issues when trying to get the simulation to display. Additionally, there are some bugs that this program still encounters, such as dragonflies trying to eat mosquitoes that are supposed to be dead. The next steps are to address these issues and try to package it into a full-fledged executable for park rangers to use.