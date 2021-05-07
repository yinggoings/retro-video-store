# Retro Video Store

Once upon a time in ye olden days to watch a movie a person had to head down to their local video store and rent a video.  We are going to step into the shoes of this old timey retro video store owner and build for ourselves all of the tools that we need in order to run our successful corner video store.  We will need a Video Store API to handle the back end, and in keeping with our retro vibe, we will build a Command Line Interface (CLI) for the front end.

## Postman Tests instead of Pytest

This project is designed to be more open ended than anything you've written in the past.  To that end, we will not be giving you Pytest tests like we have on previous projects.  We invite you to write your own tests, using the tests from Task List as a framework, but writing tests is not a required part of the project.  We will provide a suite of Postman tests, which are scripts that can be run inside of Postman to test your API.  We will be testing your CLI manually to see how it performs all of the required behaviors.  We recommend that you find a partner to "play-test" your CLI and put it through it's paces.  

## Timeline

This project is broken up into two parts, the Video Store API and the Video Store CLI.  Each part has it's own submission deadline.  The Video Store API submission deadline is May 21st, 9:00pm.  The Video Store CLI submission deadline is May 28th, 9:00pm.

## Skills Assessed

- Following directions and reading comprehension
- Demonstrating understanding of the client-server model, request-response cycle and conventional RESTful routes
- Driving development with independent research, experimentation, and collaboration
- Using Postman as part of the development workflow
- Using git as part of the development workflow

### Part 1

Working with the Flask package:

- Creating models
- Creating conventional RESTful CRUD routes for models
- Reading query parameters to create custom behavior
- Create unconventional routes for custom behavior
- Creating a many-to-many relationship between two models


### Part 2

Building a front-end Command Line Interface

- Using an external API
- Gain experience making design decisions

## Goal

### Part 1

A video store API with the following minimum functionality:
- Customers, all CRUD actions
- Videos, all CRUD actions
- Video rental checkout, custom endpoint
- Video rental check in, custom endpoint
- Listing videos checked out to a customer, custom endpoint
- Listing customers who have checked out a video, custom endpoint

### Part 2

A video store rental Command Line Interface (CLI) with the following minimum functionality

- Customer create, edit, delete
- Video create, edit, delete
- List customers
- List videos
- Check out video to customer
- Check in video
- [Optional] List videos checked out to a customer
- [Optional] List all customers who have currently checked out a video

## How to Complete and Submit

### Part 1

Go through the waves one-by-one and build the features of this API.

At submission time, no matter where you are, submit the project via Learn.

### Part 2

Go through the user stories and build the features of the CLI.

At submission time, no matter where you are, submit the project via Learn.

## Project Directions

### Part 1

1. [Setup](ada-project-docs/part-1/setup.md)
1. [Hints and suggestions](ada-project-docs/part-1/hints.md)
1. [Wave 1: CRUD for two models](ada-project-docs/part-1/wave_01.md)
1. [Wave 2: Custom endpoints](ada-project-docs/part-1/wave_02.md)
1. [Wave 3: Optional extensions](ada-project-docs/part-1/wave_03.md)

### Part 2

1.  [User Stories](ada-project-docs/part-2/user_stories.md)