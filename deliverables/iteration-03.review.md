# Snacker/Team 16

## Iteration 3 - Review & Retrospect

 * When: November 27th
 * Where: Tutorial

## Process - Reflection

 * Planning: Again, Trello board was used with success, new tasks were created as issues came up and a large task was broken down into simpler tasks in trello, which made it clear what exactly needed to be implemented. The control flow of “tickets to do”, “in progress”, “testing”, and “done” was very useful and our team was good at updating the board regularly. The work was individually selected based on our specialties and preferred development roles. A majority of people were flexible between backend and frontend which meant tickets did not require a lot of overhead and members were able to complete bigger chunks of work. 

 * Development: We met most of our weekly deadlines, however, once again we pushed some tasks that were supposed to be done by the week before to the last week. We had quite a few bugs which were only fixed a day before the deadline. By Nov 17th our first weekly progress meeting, less than half of the memberes implemented anything significant.

* Our GitHub workflow improved significantly - members were reviewing and testing pull requests and contributing with useful comments. When it comes to requests that were changing some significant features or their implementation, we were seeking more members of team to review the pull request, which was also quite successful. There was one time we had a major merge conflict, and the issuer of the pull request solved it by creating a new branch and redoing the feature based off the new master.


#### Decisions that turned out well

* Assigning deadlines to tasks on Trello, so that members who decide to take on a task need to finish it by the task’s deadline. Apart from a few small slips, we did it pretty well and almost everybody who decided to pick the ticket with the deadline actually met the deadline. However, this plan backfired somewhat as some members didn't assign any of the earlier-due tasks to themselves on trello seeing the deadlines, which resulted in heavier pressures on other members during a already busy week in order to meet the weekly deadline of the team. Our Trello board can be accessed [here](https://trello.com/b/78v6AhWR/csc301-project)

* Getting more people to do pull request reviews. This allowed us to avoid having many bugs on master and also enabled us to improve the code quality that is on the master branch. Moreover, many of the members benefited from having other members suggest improvements in their code, as it allowed us to learn different syntax and code writing styles that other people use.

* A few people did code clean-ups, which made the code more readable and easier to understand for all the members of the team.


#### Decisions that did not turn out as well as we hoped

 * We didn’t manage to consistently hold our weekly progress review meetings. In the first online meeting on Nov 17th, during which members should report their progress by 6pm, only 3 people did so. And out of the 3 people who reported on Nov 17th, only 2 people did any significant amount of work. However, we kept a good communication on the group chat. We were consistently discussing the issues and implementation during the most intense period of coding.

 * Allowing members to voluntarily choose tasks off trello whenever they want to. This results in inconsistent contributions to the project throughout the entire period of a few weeks. Again, some members were making excuses of having exams and other coursework at the start of the sprint and therefore the majority of work was forced to be done at the end of the “sprint”, which means, we were implementing the code close to the deadline on 30 Nov. 


#### Planned changes

Assuming this means what changes we have in mind if there would be a D4. One good change would be having members decide which tasks they are going to do before every in-person meeting ends so the tasks for the week can become equally assigned before everyone leaves. This will help with the problem of people avoiding taking enough tasks on their own voluntarily through Trello which results in unequal workload divide among members.


## Product - Review

#### Goals and/or tasks that were met/completed:

1. Distinguish between regular and company user in register backend
2. Front end regular vs company user register differentiation register
3. A machine learning based snack recommendation system
4. Basic account page for company and regular user
5. Company users can’t review a snack
6. After 10 reviews have been created, a snack becomes automatically verified
7. Automatically get user geolocation in the backend (figure out which country the user is from) when create a snack/review
8. Company users can add brands to their company
9. Company users can create automatically verified snacks belonging to one of their brands
10. Company users can see brands and snacks belong to their company from their account page
11. Company users can verify existing snacks that belong to one of their brands
12. Wishlist for normal users or Competitor/pay-attention watchlist for company users
13. Change frontend to give similar snack suggestions and prompt the users to create a snack if the search turns out empty
14. Search snack real time ajax feedback
15. Users able to change their info in their account page
16. Polish everything

We met all of our goals! 

Our Snack recommender system uses a Matrix Factorization algorithm, based on the user ratings. We created mocked data with a lot of new users, snacks and reviews. More details about the recommender system can be found in  [this document](https://github.com/csc301-fall-2018/project-team-16/blob/master/deliverables/doc/recommender.md). Since this task is a bigger one, it was divided into three different pull request ([I](https://github.com/csc301-fall-2018/project-team-16/pull/39), [II](https://github.com/csc301-fall-2018/project-team-16/pull/53) and [III](https://github.com/csc301-fall-2018/project-team-16/pull/55)).

Most of the information we acquired to mock our data regarding snacks, was from a website called [Taquitos](https://www.taquitos.net/). The mocked users were generated with the [Random User API](https://randomuser.me).

#### Goals and/or tasks that were planned but not met/completed:

There is one minor front end bug we can't deal with, it is the only task in trello under TODO that is marked in red and orange.

## Meeting Highlights

 * Our team is happy with the work we have completed for this project, and we appreciate each other’s effort and commitment to this project.
 * The project has a potential to be expanded and the current implementation allows to scale it up easily.
 * We should have spent more time testing before the deadline. Testing should be of a higher priority.
 * One functionality we would like to implement if we were to continue with this project is to add search and query functionality within our reviews. 

