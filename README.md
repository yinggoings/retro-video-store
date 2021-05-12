# Retro Video Store

Once upon a time in ye olden days to watch a movie a person had to head down to their local video store and rent a video.  We are going to step into the shoes of this old timey retro video store owner and build for ourselves all of the tools that we need in order to run our successful corner video store.  

For Part 1 of the project (which will be built in this repository) we will need a Video Store API to handle the back end. 

In keeping with our retro vibe, for Part 2 of the project (which has [it's own repository](https://github.com/AdaGold/video-store-cli)), we will build a Command Line Interface (CLI) for the front end.

## Postman Tests instead of Pytest

This project is designed to be more open ended than anything you've written in the past.  To that end, we will not be giving you Pytest tests like we have on previous projects.  We invite you to write your own tests, using the tests from Task List as a framework, but writing tests is not a required part of the project.  We will provide a suite of Postman tests, which are scripts that can be run inside of Postman to test your API. 

## Skills Assessed

- Following directions and reading comprehension
- Demonstrating understanding of the client-server model, request-response cycle and conventional RESTful routes
- Driving development with independent research, experimentation, and collaboration
- Using Postman as part of the development workflow
- Using git as part of the development workflow

- Working with the Flask package:
    - Creating models
    - Creating conventional RESTful CRUD routes for models
    - Reading query parameters to create custom behavior
    - Create unconventional routes for custom behavior
    - Creating a many-to-many relationship between two models

## Goal

The full functionality is spelled out further in the "Project Directions" files (linked below). At a high-level, our goal is to create a video store API with the following minimum functionality:
- Customers, all CRUD actions
- Videos, all CRUD actions
- Video rental checkout, custom endpoint
- Video rental check in, custom endpoint
- Listing videos checked out to a customer, custom endpoint
- Listing customers who have checked out a video, custom endpoint

## How to Complete and Submit

Go through the waves one-by-one and build the features of this API.

At submission time, no matter where you are, submit the project via Learn.

## Project Directions

1. [Setup](ada-project-docs/part-1/setup.md)
1. [Hints and suggestions](ada-project-docs/part-1/hints.md)
1. [Wave 1: CRUD for two models](ada-project-docs/part-1/wave_01.md)
1. [Wave 2: Custom endpoints](ada-project-docs/part-1/wave_02.md)
1. [Wave 3: Optional extensions](ada-project-docs/part-1/wave_03.md)
