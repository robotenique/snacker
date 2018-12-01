# Snacker/Team 16

## Iteration 3

 * Start date: Nov 13, 2018
 * End date: Nov 30, 2018

## Process

#### Changes from previous iteration

 * We will start assigning deadlines to tasks on trello and members who decide to take on a task needs to finish it by the task’s deadline. This is to avoid the problem we have experienced with the past deliverable where lots of work is being done in the last week. This is especially important for cases where one task has to be done before another important task can be done. And it is especially important for deliverable 3 since we must finish everything by the due date and can’t afford to push unfinished stuff onward.
 
 * We will also start consistently holding weekly progress review meeting every Sat night to make sure the tasks can be done in time and if a member can’t finish their chosen part in time, the rest of team can offer help during the weekend and resolve the issue early. The current plan is every member report by 6pm on Sat on their progress and whether or not they need help to finish their task in time, this is also an opportunity to ask for help if any member gets stuck on something.

#### Roles & responsibilities
Some roles members take on:
 * Scrum master: Juliano
 * Everyone is a developer

Some responsibilities members take on that can't be demonstrated by code commits:
 * Juliano: populated the database with thousands of users, snacks, and reviews
 * Giuliano: verified thousands of snacks in the databse according to whether they had 10 reviews or not
 * Jayde and Harry: demo video script writing and video making

#### Events
In Person Meeting 1
 * Nov 13, 2018 in tut
 * Planning meeting where tasks are prioritized and assigned deadlines

In Person Meeting 2
 * Nov 20, 2018 in tut
 * Progress Review, we should finish task 1, 2, 4, 5, 6, 7, 8, 9 in the following Goals and Tasks section and we should have a concrete plan of what to do with snack recommendation.

In Person Meeting 3
 * Nov 27, 2018 in tut
 * Progress Review, we should finish snack recommendation, account page, wishlist, and everything else. And we should film a draft video during tut.

Review Meeting 3
 * Nov 30, 2018 in person on campus
 * We should have everything polished up and finish the final version of video.

Weekly Sat Night Progress Report Meeting
 * 1st one Nov 17th, 2nd one Nov 24th
 * Since it is hard for everyone to be present for a specific time slot, what we will do this time is to have everyone report their progress by 6pm on Sat, and then we will discuss whether to re-assign/re-prioritize some tasks and we can help each other to implement tasks if needed.

#### Artifacts

* The most important artifact is our [Trello Board](https://trello.com/b/78v6AhWR/csc301-project). This artifact is where we: Keep track of tasks we need to do, keep track of the priority and scope of the task (backend, frontend, documentation, etc.) and will also serve as the schedule (by giving each task a deadline). The assignment of the task depends on the initiative of the team members, members assign tasks to themselves on the trello board when available;

* Another important artifact for this iteration will be a documentation of the recommendation system, which will be written in our repo [here]((https://github.com/csc301-fall-2018/project-team-16/blob/master/deliverables/doc/recommender.md). This is an important artifact because the recommendation system is not as straightforward to understand as the usual backend/frontend tasks, just by looking at the code; In data science, the code not always can be self explanatory (or not enough), so the process and the model of how it was built needs to be documented.

#### Git / GitHub workflow

Each member should open their own branch off master when working on their tasks and they should issue pull requests back to master when they finish their work. Any member of the team can review pull request and everyone should contribute by reviewing pull requests. At least two reviewers’ opinions are needed before a pull request can be merged to master. We avoid most conflicts by using the updated code in the branches. That is, a branch shouldn’t be opened for a long time, because the code of the master could change a lot, and this would lead to unnecessary conflicts when a pull-request is made for the current branch. If a conflict does arise, however, the pull request issuer is expected to resolve the conflicts in their branch before merging to master.

## Product

#### Goals and tasks
1. Distinguish between regular and company user in register backend (20th)
2. Front end regular vs company user register differentiation register (20th)
3. Snack recommendation (20th: come up with a concrete plan of how exactly do we implement recommendation what data (how much data) do we exactly need to put etc., 24th: finish and start testing, 27th: finish and work well)
4. Basic account page for company and regular user (20th)
5. Company users can’t review a snack (20th)
6. After 10 reviews have been created, a snack becomes automatically verified (20th)
7. Automatically get user geolocation in the backend (figure out which country the user is from) when create a snack/review (20th)
8. Company users can add brands to their company (20th)
9. Company users can create automatically verified snacks belonging to one of their brands (20th)
10. Company users can see brands and snacks belong to their company from their account page (27th)
11. Company users can verify existing snacks that belong to one of their brands (27th)
12. Wishlist for normal users or Competitor/pay-attention watchlist for company users (27th)
13. Change frontend to give similar snack suggestions and prompt the users to create a snack if the search turns out empty (27th)
14. Search snack real time ajax feedback (27th)
15. Users able to change their info in their account page (27th)
16. Polish everything (29th)

#### Artifacts

We will present our website that would be locally run on a group member’s laptop. Along with the live [demo](https://www.youtube.com/watch?v=ZIszrKrW3gM), we will have a powerpoint presentation with slides for the technical discussion and process distribution. We will showcase the tech stack we used through images or text. We will include code snippets to show the style we implemented and the quality of our code. To show off our process distribution, we present our trello board that has the tasks and which stage each task is in. 
