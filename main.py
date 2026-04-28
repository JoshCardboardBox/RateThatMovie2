"""
WEBSITE: RateThatMovie!

    This is the internal home file, from where we run our website pages.
    For our COMP-340 class, presented on 30 April 2026. Rhodes College.
    Team: Malik Waters, Peter Kennedy, Joshua Inha Hwang

    On this website, users get to:
    - search movies, actors, and directors
    - rate movies
    - get recommendations
"""

#Import Tools
from tlbx_imports import *

#Import Webpages
from page_homepage import *
from page_login import *
from page_createacc import *
from page_search import *


#RUN WEBSITE
ui.run(reload=False, storage_secret="TEMP")