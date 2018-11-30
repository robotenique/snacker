# YOUR PRODUCT/TEAM NAME

 > _Note:_ This document is meant to be written during (or shortly after) your review meeting, which should happen fairly close to the due date.      
 >      
 > _Suggestion:_ Have your review meeting a day or two before the due date. This way you will have some time to go over (and edit) this document, and all team members should have a chance to make their contribution.


## Iteration 3 - Review & Retrospect

 * When: November 27th
 * Where: Tutorial

## Process - Reflection

 * Planning: Again, Trello board was used with success, we were creating tasks that were taken by members quickly, which make it easier to be clear what exactly needs to be implemented. The control flow of “tickets to do”, “in progress”, “testing”, and “done” was very useful and our team was good at updating the board regularly. The work was divided based on our specialties and preferred development roles. A majority of people were flexible between backend and frontend which meant tickets did not require a lot of overhead and members were able to complete bigger chunks of work. 

 * Development: As long as the major components, such as the recommendation system were implemented according to our timeline, the implementation of other features were shifted towards 30 November. We had some bugs (e.g. errors appearing in the front end with the change of data stored about the users), which were only fixed a day before the deadline.

* Our GitHub workflow improved significantly - members were reviewing and testing pull requests and contributing with useful comments. When it comes to requests that were changing some significant features or their implementation, we were seeking the majority of the team to review the pull request, which was also quite successful. There was one time we had a major merge conflict, but we managed to get it resolved during our meeting during the tutorial, in a discussion between ourselves and the TA.


#### Decisions that turned out well

* Assigning deadlines to tasks on Trello, so that members who decide to take on a task need to finish it by the task’s deadline. Apart from a few small slips, we did it pretty well and almost everybody who decided to pick the ticket with the deadline actually met the deadline. This was very important because last iteration we had some problems in doing tasks that weren’t done in time (only by the last minute). Our Trello board can be accessed [here](https://trello.com/b/78v6AhWR/csc301-project)

* Getting more people to do pull request reviews. This allowed us to avoid having many bugs on master and also enabled us to improve the code quality that is on the master branch. Moreover, many of the members benefited from having other members suggest improvements in their code, as it allowed us to learn different syntax and code writing styles, that other people use.

* A few people did code clean-ups, which made the code more readable and easier to understand for all the members of the team.


#### Decisions that did not turn out as well as we hoped

 * We didn’t manage to consistently hold our weekly progress review meetings, however, we kept a good communication on the group chat, which almost eliminated the need for the meeting. We were consistently discussing the issues and implementation during the most intense period of coding.

 * Consistent contributions to the project, throughout the entire period of a few weeks. Again, members were making excuses of having exams and other coursework and therefore the majority of work was forced to be done at the end of the “sprint”, which means, we were implementing the code close to the deadline on 30 Nov.


#### Planned changes

Assuming this means what changes we have in mind if there would be a D4. One good change would be having members decide which tasks they are gonna do during every in-person meeting so the tasks for the week can become equally assigned before everyone leaves. This will help with the problem of people avoiding taking enough tasks on their own voluntarily through Trello which results in unequal workload divide among members.


## Product - Review

#### Goals and/or tasks that were met/completed:

1. A machine learning based Snack recommendation system 
2. Basic and different account page for companies and regular users
3. Wishlist for normal users
4. Company users can create, verify existing snacks and/or brands from their company
5. Company users can see brands and snacks belonging to their company from their account page
6. Snacks become automatically verified after a certain number of reviews or through company users that recognizes their snacks
7. Automatically gets user geolocation in the backend when creating a snack and/or review
8. User search bar autocomplete/suggestion feature
9. Users are capable to change their account information via the account page 
10. Restricted actions for Company users such as reviewing snacks and wishlist
11. Change frontend to give alternative search query and prompt the users to create a snack if the search turns out empty

Our Snack recommender system uses a Matrix Factorization algorithm, based on the user ratings. We created mocked data with a lot of new users, snacks and reviews. More details about the recommender system can be found in  [this document](https://github.com/csc301-fall-2018/project-team-16/blob/master/deliverables/doc/recommender.md). Since this task is a bigger one, it was divided into three different pull request ([I](https://github.com/csc301-fall-2018/project-team-16/pull/39), [II](https://github.com/csc301-fall-2018/project-team-16/pull/53) and [III](https://github.com/csc301-fall-2018/project-team-16/pull/55)).

Most of the information we acquired to mock our data regarding snacks, was from a website called [Taquitos](https://www.taquitos.net/). The mocked users were generated with the [Random User API](https://randomuser.me).


#### Goals and/or tasks that were planned but not met/completed:


Competitor/pay-attention watchlist for company users 
‘Contact Us’ form implementation (using email server to send emails, etc.).

## Meeting Highlights

 * Our team is happy with the work we have completed for this project, and we appreciate each other’s effort and commitment to this project.
 * Even though we started early and tickets were assigned accordingly, there were still tasks that were completed last minute. Most of these are bug fixes for recent features.
 * The project has a potential to be expanded and the current implementation allows to scale it up easily.

Going into the next iteration, our main insights are:

1. Adding search and query functionality for our reviews.
2. Making sure we spend more time testing not before the deadline. Testing should be a higher priority.
3. Having members decide which tasks they are gonna do during every in-person meeting so tasks for the week/sprint can become equally assigned before everyone leaves.

