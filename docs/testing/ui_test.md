# UI Tests

## Test Case 1a: Successful Login
**Description**: Verify that the user can successfully log in and authenticate.
**Prerequisites**: Register in the app with the username "aaa" and password "111".

**Steps:**

1. Open the application.
2. Enter the username "aaa" and password "111".
3. Ensure the "Sign up" checkbox is unchecked.
4. Click the "Submit" button.

**Expected Result:**
The main screen displays two buttons: "DEUTSCH!" and "RECHT & POLITIK".

**Actual Result:**
Consistent.

## Test Case 1b: Unsuccessful Login
**Description**: Verify that the error message is displayed when user credentials can't be found in the database.

**Steps:**

1. Open the application.
2. Enter the username "aab" and password "112er344t".
3. Ensure the "Sign up" checkbox is unchecked.
4. Click the "Submit" button.

**Expected Result:**
The error message is displayed.
**Actual Result:**
Consistent.


## Test Case 2: User Registration
**Description:** Verify that a new user can successfully register.

**Steps:**

1. Open the application.
2. On the "Welcome" screen, enter the username "sfEer" and password "3234566".
3. Check the "Sign up" checkbox.
4. Click the "Submit" button.

**Expected Result:**

Tthe main screen is displayed.
**Actual Result:**
Consistent.

## Test Case 3: Accessing German Chat Screen
**Description:** Verify that the user can navigate to the German chat screen.

**Steps:**
1. On the main screen, click the "DEUTSCH!" button.

**Expected Result:**

The user can see chat interface, a welcome message and a "New Lesson" button.

**Actual Result:**
Consistent.

## Test Case 4: Accessing Law and Politics Chat Screen
**Description:** Verify that the user can navigate to the Law and Politics chat screen.

**Steps:**

1. On the main screen, click the "RECHT & POLITIK" button.

**Expected Result:**

The user can see chat interface, a welcome message.
**Actual Result:**
Consistent.

## Test Case 5: Sending a Message in German Chat
**Description:** Verify that the user can send a message in the German chat.

**Steps:**

1. On the German chat screen, type a message "How can I say "I'd like to see a doctor?"?" in the chat input field.
2. Press the "Send" button.

**Expected Result:**
The application receives displays a response with the German translation in the chat history.

**Actual Result:**
Consistent.

## Test Case 6: Starting a New Lesson in German Chat
**Description:** Verify that the user can start a new lesson in the German chat.

**Steps:**

1. On the German chat screen, click the "New Lesson" button.

**Expected Result:**

The message with a lesson content on grammar is displayed.

**Actual Result:**
Consistent.

## Test Case 7: Accessing Tasks for a Lesson

**Description:** Verify that the user can access tasks for a generated lesson.

**Prerequisites:** The message with a lesson on grammar is displayed.

**Steps:**
1. After starting a new lesson, click on the "Tasks" button.

**Expected Result:**
The tasks are displayed, including their type, questions, and answer fields.

**Actual Result:**
Consistent.

## Test Case 8: Submitting Task Answers

**Description:** Verify that the user can submit answers for tasks.

**Prerequisites:** The displayed tasks are completed.

**Steps:**
1. Click the "Submit" button.

**Expected Result:**
The user is navigated back to the chat, a message offering to start a new lesson is appeared with a button "New lesson".

**Actual Result:**
Consistent.

## Test Case 9: Viewing a Question from the Law Chat

**Description:** Verify that the user can view the question list.

**Steps:**

1. On the Law chat screen, click on the hat icon at the top right corner.

**Expected Result:**

The user sees a list with possible questions.

**Actual Result:**
Consistent.


## Test Case 10: Selecting a Question from the Law Question View List
**Description:** Verify that the user can select a question from the question list and get the answer in the chat.

**Steps:**

1. On the Question View List, click on a question "Welche Bedeutung hat das Grundgesetz für die Bürgerrechte in Deutschland?" from the question list.

**Expected Result:**
The user is navigated back to the law chat screen.
The question is displayed in the chat history.
The application displays a response in the chat history.

**Actual Result:**
Consistent.
