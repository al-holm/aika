# Use Cases

# Definitions

**Progress tracker** is a component within the German chat interface that monitors, records, and displays a user's progress through users messages and task completion.

**Learning State** refers to the current status of a user's progress in the curriculum determined by their interactions with the app. It is updated dynamically based on user actions such as sending messages, completing tasks. It consists of already learned topics defined in the curriculum with the sccores for each topic. 

**Curriculum** is organized in a graph structure, where each node represents a specific learning objective or topic, and edges between nodes indicate prerequisite relationships. Each node has other metadata such as type (e.g. Grammar or Vocabulary).

# Table of contents
<!-- TOC start -->
- [Welcome Screen](#welcome-screen)
   * [1a. Authentication - Log in (Optional)](#1a-authentication-log-in-optional)
   * [1b. Authentication - New account (Optional)](#1b-authentication-new-account-optional)
   * [1c. Guide - New account (Optional)](#1c-guide-new-account-optional)
   * [1d. Interaction with main menu](#1d-interaction-with-main-menu)
- [Chat with German Bot](#chat-with-german-bot)
   * [2a. Send a message & get a response](#2a-send-a-message-get-a-response)
   * [2b. Restore the message history](#2b-restore-the-message-history)
   * [2c. Start a new lesson](#2c-start-a-new-lesson)
   * [2d. Automatic translation](#2d-automatic-translation)
   * [2e. Task Widget](#2e-task-widget)
   * [2f. Progress tracker](#2f-progress-tracker)
   * [2g. Update learning state](#2g-update-learning-state)
   * [3. Persisting message data in the data base](#3-persisting-message-data-in-the-data-base)
- [Chat with Recht und Alltag Bot](#chat-with-recht-und-alltag-bot)
   * [4a. Send a message & get a response](#4a-send-a-message-get-a-response)
<!-- TOC end -->

<!-- TOC --><a name="welcome-screen"></a>
# Welcome Screen

<!-- TOC --><a name="1a-authentication-log-in-optional"></a>
## 1a. Authentication - Log in (Optional)

**Actor:** User

**Goal:** To securely log into the system using a username and password.

**Basic Flow:**

---

=> The user enters their username and password.

=> The system validates the credentials.

=> Upon successful validation, the user is granted access to the system.

=> If the credentials are incorrect, the user is prompted either to create a new account or try again.

---

<!-- TOC --><a name="1b-authentication-new-account-optional"></a>
## 1b. Authentication - New account (Optional)

**Actor:** User

**Goal:** To securely log into the system using a username and password for the first time.

**Basic Flow:**

---

=> The user presses on "Create new account" in the welcome menu.

=> The user enters their username and password.

=> New account details are added to the database with user data.

---

<!-- TOC --><a name="1c-guide-new-account-optional"></a>
## 1c. Guide - New account (Optional)

**Actor:** User

**Goal:** To get first impressions for the system.

**Prerequisites**: User is logged in for the first time.

**Basic Flow:**

---

=> The system displays a widget with a welcome message & a button 'Continue'.

=> After pressing the continue button, the system suggests the user to select the interface language.

=> After selecting a language, all the system elements will be displayed in the selected language.

=> A further widget with information about 2 interfaces ('German chat' and 'Recht & Alltag’) is displayed. 

=> A next widget tells the user about learning German with the app and  the main functionalities such as chat interface, buttons, tasks widgets, translation and progress tracker.

---

<!-- TOC --><a name="1d-interaction-with-main-menu"></a>
## 1d. Interaction with main menu

**Actor:** User

**Goal:** To naviagate between the different components of the system.

**Prerequisites**: User is logged into the app.

**Basic Flow:**

---

=> The system displays a screen with a welcome message, buttons "Deutsch" and "Recht & Alltag" at the bottom of the screen. At the top right corner there is a setting icon. 

=> After pressing the button, the according chat interface is displayed.

=> After pressing on a setting icon, the user can adjust their language.

---

<!-- TOC --><a name="chat-with-german-bot"></a>
# Chat with German Bot

<!-- TOC --><a name="2a-send-a-message-get-a-response"></a>
## 2a. Send a message & get a response

**Actor:** User

**Goal:** Send a message to a German bot.

**Prerequisites**: User is logged in.

**Basic Flow:**

---

=> The user presses a button 'Deutsch'.

=> A chat interface with the welcome message appears.

=> The user sends a message or question to the German bot.

=> The sent message with metadata are persisted to a SQL data base.

=> The system processes the request using AI-based System to understand and generate a response.

=> the system respnse with a metadata is persisted to a SQL data base as well.

=> The system display the response in the chat.

=> If the message contains audio, an audio player component is displayed under the message.

---

<!-- TOC --><a name="2b-restore-the-message-history"></a>
## 2b. Restore the message history

**Actor:** User

**Goal:** To see the message history from the previous sessions.

**Prerequisites**: User is logged in and there are messages from this user in the data base from the last session.

**Basic Flow:**

---

=> The user presses a button 'Deutsch'.

=> The system fetches the message history from the data base and displays it in the chat insterface.

---

<!-- TOC --><a name="2c-start-a-new-lesson"></a>
## 2c. Start a new lesson

**Actor:** User

**Goal:** To start a new lesson.

**Prerequisites**: User is logged in and navigated to the german chat interface.

**Basic Flow:**


---

=> the system displays the message histroy and the new message with a button under the message 'New lesson'. 

=> The user presses a button to start a new lesson.

=> The system uses AI to generate tasks based on the user's progress and a retrieved topic from the curriculum.

=> The user completes the tasks and views corrections and asks for explanations where necessary.

=> If all tasks are done and there is no question, the system informs the user that they completed the lesson.


---

<!-- TOC --><a name="2d-automatic-translation"></a>
## 2d. Automatic translation

**Actor:** User

**Goal:** To see the translation.

**Prerequisites**: User is logged in and and navigated to the german chat interface.

**Basic Flow:**


---

=> The user sends a message to the system and gets a response.

=> Under the system message is a small standard translation icon displayed.

=> The user presses the icon button.

=> The system tranlates a message into the selected interface language.


---

<!-- TOC --><a name="2e-task-widget"></a>
## 2e. Task Widget

**Actor:** User

**Goal:** To complete the tasks.

**Prerequisites**: User is logged in and and navigated to the german chat interface, system generated a set of tasks.

**Basic Flow:**


---

=> The user clicks the "tasks" button under the system message to open the task widget.

=> System displays tasks relevant to the current learning context.

=> User can swipe left or click "back" to return to the main chat interface any time, the current progress is saved. 

=> System logs task completion to progress tracker and switches back to the main chat interface.


---

<!-- TOC --><a name="2f-progress-tracker"></a>
## 2f. Progress tracker

**Actor:** User

**Goal:** To see the current progress.

**Prerequisites**: User is logged in and and navigated to the german chat interface.

**Basic Flow:**


---

=> The user selects to view the curriculum and clicks the icon of a graph at top right corner of the screen.

=> The system display the progress of the user in form of table of contents with different header styles. 

=> The unit with the lowest header level has a progress bar displaying a user progress. 


---

<!-- TOC --><a name="2g-update-learning-state"></a>
## 2g. Update learning state

**Actor:** User

**Goal:** To update learning state.

**Prerequisites**: User sent a message to system or completed tasks.

**Basic Flow:**


---

=> After each user message, the system checks the spelling and grammar mistakes and matches the mistakes with the according elements from the curriculum.

=> The learning state is updates.

=> The progress tracker updates the progress interface (2f).



---

<!-- TOC --><a name="3-persisting-message-data-in-the-data-base"></a>
## 3. Persisting message data in the data base

**Actor:** System

**Goal:** To save message history.

**Prerequisites**: User sent a message to the system.

**Basic Flow:**


---

=> The system creates a DTO object including message text, timestamp, generated message_id, username, role. 

=> The system persists data into a SQL data base.



---

<!-- TOC --><a name="chat-with-recht-und-alltag-bot"></a>
# Chat with Recht und Alltag Bot

<!-- TOC --><a name="4a-send-a-message-get-a-response"></a>
## 4a. Send a message & get a response

**Actor:** User

**Goal:** Send a message to a Law & Daily life microservice.

**Prerequisites**: User is logged in.

**Basic Flow:**


---

=> The user presses a button 'Recht & Alltag'.

=> A chat interface with the welcome message appears.

=> The user sends a message or question to the bot.

=> The user can attach a PDF to their message. 

=> The sent message with metadata are persisted to a SQL data base.

=> The system processes the request using Retrieval-Augmented Generation System to generate a response based on the data in the vectordatabase.

=> The system response with a metadata is persisted to a SQL data base as well.

=> The system display the response in the chat.

---

