# Snacker/Team 16

## Iteration 2 - Review & Retrospect

## Process - Reflection

 * Planning: We utilized the Trello board pretty well, the tasks were created as issues came up and were assigned or taken by members very quickly. The control flow of “tickets to do”, “in progress”, “testing”, and “done” was very useful and our team was good at updating the board regularly. The work was divided based on our specialties and preferred development roles. A majority of people were flexible between backend and frontend which meant tickets did not require a lot of overhead and members were able to complete bigger chunks of work.

 * Development: We hit some last minute snags with some of our implementations as our TA said our original implementation was lacking some features. We were already working on the features but they were not fully polished until the last minute. There also seemed to be miscommunication about exactly what was the best practice for approving and merging GitHub pull requests. Some members merged for others which led to a discussion of what should we do. We eventually decided to enforce the ruling that each PR requires a approval from at least one person preferably two and should also require a review from that particular person if the change is modifying that person’s work.

 * Our timeline were not followed well: we planned originally to finish our entire work on Tuesday before the Friday when Deliverable 2 is due, however that did not happen. We also didn’t meet any one of our set weekly development goal. Some members were quite unresponsive until the weekend before the due date.

 * To account for members’ work outside of code commits (for participation marks): Juliano and Jayde worked on creating the database and connecting to it via flask; Juliano and Giuliano populated the database with flasks with a script he wrote that get snack data from another website; Juliano, Jayde, and Flora created the database relationship diagram; Jayde, Adam and Alex wrote/edited the video script; Jayde and Alex created the video; Juliano fulfilled the duties of a scrum master dutifully and organized things to discuss during each meeting before the meetings so that we were able to utilize our meeting time well

#### Decisions that turned out well

 * Trello task management: We decided to use the Trello board, and it was a very important decision, because it’s a very easy and convenient way to keep track of what tasks need to be done, and in which ‘area’ of development (backend, frontend, administrative, testing, etc.). By looking at the board itself, we have an overview of which part of our project one should focus on, which is very important for our planning.

 * Sunday online meetings: There should be two of such meetings, but at the end only one of them was held (Oct 28). That meeting was successful because the team used the time to resolve technical confusions and pull request miscommunication, and also to lay out timeline expectation of tasks. Even though not every member of the team attended the meeting, we kept each other updated and that made development easier.

 * Using Readme: We decided to have a readme document detailing how to set up the dev environment, how to use flask, our agreed coding style and naming convention. This was great since we were able to ask members to refer to Readme for lots of common questions instead of having to explain every time.

#### Decisions that did not turn out as well as we hoped

 * Pull request reviews: Initially, we didn’t communicate the pull request expectation well which allowed poor implementations and bugs to be merged to master branch since code was pushed without having been reviewed. Then we clarified the pull request procedure that only the commits reviewed and approved by a few members of the team can be merged. However, then we encountered the problem that pull request stayed open for too long since members were not actively reviewing the pull request fast enough, this is especially problematic to other members who might need the code in the open pull request. So then we made the decision that only 2 reviewers’ opinions are needed before a pull request can be merged, and in the case of emergent bug fixes just let other members know through facebook group chat and push to master.
 * Our original timeline for the tasks was not followed so well: Due to midterm exams, many people can not do their tasks until the weekend before the due date. Even though it was against our initial agreement, everybody started working on the project as soon as they could, which is highly appreciated.

#### Planned changes

 * We should start assigning deadlines to tasks on trello and members who decide to take on a task needs to finish it by the task’s deadline. This is to avoid the problem we have experienced with the current deliverable where lots of work is being done in the last week. This is especially important for cases where one task has to be done before another important task can be done. And it is especially important for deliverable 3 since we must finish everything by the due date and can’t afford to push unfinished stuff onward.

 * We should also consistently hold < 20min weekly progress review meeting every Sat to make sure the tasks can be done in time and if a member can’t finish their chosen part in time, the rest of team can offer help during the weekend

## Product - Review

#### Goals and/or tasks that were met/completed:

The 12 tasks we planned to finish by deliverable 2
 1. Decide on the stack/framework/database
 2. Setup everyone’s dev environment
 3. Decide on the frontend look/choose a frontend template
 4. Setup basic frontend
 5. Decide on and set up database schema
 6. Create an account
 7. Login
 8. Populate database with some snacks
 9. Index page
 10. Search a snack
 11. About/contact page
 12. User create a snack
 
We finished all of them! In addition, we also implemented displaying all the reviews for a specific snack and creating a new review for a snack. And our web app can be run locally with flask as planned. We also finished the data relationship diagram and the video in time as planned.

#### Goals and/or tasks that were planned but not met/completed:

Even though we finished every feature, some features’ functionality are not satisfactory, namely:
 * Number 6 create an account is not fully finished since our system should distinguish between normal user and company user but it currently doesn’t.
 * Number 10 search a snack needs to be improved too so that users can get real time search results from their inputted letters like when they type in google. Right now we have a three-parameter search bar that filters through the snack name, brand, and location, however, the desired purpose is for it to have a single search which filters through all attributes of a snack in our database and give search result feedback as users type. We should also change the UI to prompt the users to create a snack if the search turns out empty.
 * After we implement distinguishment between normal user and company user, we need to change number 12 user create a snack too so that company users can create automatically verified snacks.
 * There is additional work to be done with regards to UI to improve the user’s experience.

## Meeting Highlights

 * Our team is generally happy with the work we have completed so far and we appreciate each other’s effort and commitment to this project.
 * We should really start early next time and avoid pushing work to the last week as this sacrifices quality of our product and increases stress.
 * Everyone needs to take some time to review pull requests so that they can be merged to master in a timely manner.
