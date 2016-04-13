Bill Roberts - wjr2113
Jonathan Sun - jys2124

COMS W4111.001 - Introduction to Databases
Spring 2016

"Liberated-Fitness Web-server"



UNI to identify our database:
	jys2124

The URL of your web application:
	http://<IP ADDRESS>:8111/


Overview:

Our original proposal was to design an application that will service two kinds of users: coaches and athletes. Coaches will view and edit a calendar feature that enables them to coordinate and schedule classes. They will enter client attendance for classes into an attendance feature, which will provide a dashboard view of attendance data. Athletes will be able to store and retrieve their performance data for workouts. Finally, the application will present the “Most Liberated” leaderboard for viewing by athletes and editing by coaches.






A description of the parts of your original proposal in Part 1 that you implemented, the parts you did not (which hopefully is nothing or something very small), and possibly new features that were not included in the proposal and that you implemented anyway. If you did not implement some part of the proposal in Part 1, explain why.

In-depth look at two pages:

	'Attendance'
	The attendance page consists of three primary components: a calendar, an attendance sheet, and an attendance form. This page is intended for coach (admin) use. The Coach can use the calendar to traverse the months. Instances of class times will populate the calendar.

	The calendar population is a multi-part query flow. The current month in view is reflected in the URL. The application responds dynamically by querying for class-times within the month. Then when the calendar is rendered, the class times are injected into their appropriate cells.

	A coach can select any of these classes to view the attendance for that class on that day. Below the calendar, the attendance sheet will populate with the attendees for that class on that day. This is calculated from the database by querying for a list of users in the 'attends' relationship table, constrained against a range of dates.

	Next to the attendance sheet is an attendance form listing all athletes. A Coach can mark any number of athletes as present and submit the form. This inserts those marked users to the 'attends' table appropriately. The page is refreshed and the new changes are reflected in the attendance sheet.




Briefly describe two of the web pages that require (what you consider) the most interesting database operations in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.
