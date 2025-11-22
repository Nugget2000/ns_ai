# ns_ai
An ai powered application for analyzing and managing type 1 diabetes using Nightscout and loop using different personas with different roles and expertise.
The tagline is a funny twist on "We are not waiting", with ai this cleverly becomes "The microbolus generation is here".
It is clear that the webpage is built on the fantastic work of the open source community and that we are all for ever grateful for the tireless work done by all contributors. 

Personas:
- Emanuel Reading: Helping the user to understand the documentation for Nightscout and loop.
    Skillfully trainied on the documentation for Nightscout and loop he can give expert advice on the documentation and help the user to understand the documentation and quickly find links to the documentation.
    Is ready for immediate interaction.

- Hanna Horizon: Helping the user to do a overarching retrospective analysis of the data in Nightscout. She is a data analyst with a focus on diabetes management.
Analyzing the data in Nightscout she can give expert advice on the data and help the user to understand the data and quickly find links to the data, she also calculates KPIs and provides insights based on the data and KPIs. 
The user needs to sign up and provide access to the data in Nightscout to use this persona.

- Cora Carbcount: Helping the user to do a detailed event analysis of the data in Nightscout. She finds significant events and provides insights based on the data and KPIs and helps understand if some insight can be found, like improving carb count, pre-bolus, always rising when changing pump, alot of missing values often ends up as high glucose values.
The user needs to sign up and provide access to the data in Nightscout to use this persona.

- Benny Basal: Helping the user to do a settings analysis of the data in Nightscout. Will analyse the balance of settings and verify the settings are optimal for the user by comparing the settings with the data in Nightscout and Loop data.
The user needs to sign up and provide access to the data in Nightscout to use this persona.


Backend
--------------------
The application is a web application that can be run as a docker container divided into different services:
- Backend: The backend is a fastapi application that provides the api for the frontend and the personas.
-- Technologies used:
--- Fastapi with pydantic models
--- Firestore
--- Docker
--- Python

-- Responsiblies of the backend:
--- Authentication and authorization of the users.
--- Retrieving data from the nighscout api.
--- Caching of the data retrieved from the nighscout api.
--- Caching of the ai generated responses.
--- Providing the api for the frontend and the personas.


Database
--------------------
- Database: The database is a firestore database that stores the caches data retrieved from the nighscout api along and caches 
the ai generated responses.
The database is cloudbased and no local database is used.


Frontend
--------------------
- Frontend: The frontend is a react application that provides the user interface for the backend and the personas.
-- Technologies used:
--- React
--- Docker
--- Python

Look and feel is non cluttered and modern with dark background. Top will have a small bar showing the name of the application and the version. 
- Landing page - Introducing the personas and their roles and expertise along with pictures. The personas are presented as four squares with a picture and a short description. 
Below is a disclaimer saying the resposibility and medical actions are not taken by the application and the personas and are supposed to be used as advice. 
Also an explaination how the service works. Emanuel is ready for immediate interaction with a link to his page.


- Emanuel page - Introducing Emanuel and his role and expertise along with pictures. Emanuel is ready for immediate interaction with a link to his page.

- A "AI Insights" page - Introducing the AI Insights page where the user can connect nightscout api and get feedback from the personas Hanna, Cora and Benny.

- Feedback and comments page - Introducing the feedback and comments page where the user can provide feedback and comments to the application and the personas. The vibrant community can share their thoughts and experiences with the application and the personas and give suggestions for improvement.

- About page - Introducing the application and the personas and their roles and expertise along with pictures. The personas are presented as four squares with a picture and a short description. 


- Tribute page  to the open source community and all contributors - carusell showing top contributors and their contributions in the open source community. Specifically on the sites https://github.com/nightscout/cgm-remote-monitor and https://github.com/nightscout/Loop the authors of https://www.loopnlearn.org/ and https://loopkit.github.io/loopdocs/ are thanked for changing so many people's lives.



