# Pileh: A Modern Electronics Marketplace with Real-time Chat

## Project Overview

Pileh is a comprehensive web application designed as a specialized marketplace for electronic devices, particularly focusing on mobile phones. Built as the Capstone Project for CS50's Web Programming with Python and JavaScript, Pileh aims to deliver a seamless and intuitive user experience for buying and selling used electronic goods. Our primary goal was to create a platform that is significantly more dynamic and user-centric than typical e-commerce solutions, emphasizing direct user interaction and sophisticated product management.

## Key Features & Innovations

Pileh distinguishes itself from previous CS50 projects and generic web applications through several key functionalities and design choices:

1.  **Direct, Real-time Chat System:**
    * **Beyond Email:** Unlike the CS50 Email project which focused on asynchronous email exchanges, Pileh incorporates a direct, product-specific chat system. Users can initiate and maintain conversations tied to a specific product listing, fostering immediate and relevant communication between buyers and sellers. This real-time interaction is designed to enhance trust and expedite transactions.
    * **User-Friendly Interface:** The chat interface is designed for ease of use, making communication fluid and accessible on all devices.

2.  **Advanced Local Image Upload & Management:**
    * **Server-Side Storage:** Instead of relying on external image URLs, Pileh allows users to directly upload product images from their local devices to the server. This provides greater control over content, ensures image persistence, and simplifies the listing process for users.
    * **Optimized Display:** Images are efficiently handled and displayed across the platform, from product listings to detail pages.

3.  **Seamless Product Navigation:**
    * **Direct Switching:** Users can navigate between product detail pages sequentially using "Next" and "Previous" buttons directly from any product detail page, without needing to return to the main product list. This streamlines Browse and mimics a native application feel.

4.  **Specialized Product Data Entry:**
    * **Structured Input:** For electronic devices, Pileh implements a sophisticated data entry system for product specifications (Brand, Model, Storage, SIM Card Status, Color). This is managed through interactive modal pop-ups with sequential selections, ensuring data consistency and improving search accuracy. This goes beyond the generic product fields seen in previous e-commerce projects.

5.  **Dedicated User Profiles & Listings:**
    * Users have dedicated profile pages where they can view all products listed by a specific seller. This enhances transparency and allows for exploration of a seller's complete inventory, providing a more robust user experience than basic listing views.

6.  **Full Mobile Responsiveness (Adaptive UI/UX):**
    * The entire application is meticulously designed to be fully mobile-responsive. Layouts, elements, and interactions adapt seamlessly across various screen sizes, from large desktops to small mobile devices, ensuring optimal usability on any platform.
    * Particular attention has been paid to the responsiveness of the navigation bar, product cards, detail pages, chat interface, and modal forms, ensuring all components are functional and aesthetically pleasing.

7.  **Elegant and Intuitive Design:**
    * Pileh boasts a clean, modern, and user-friendly interface. This includes thoughtful use of shadows, consistent sizing, smooth hover effects, and a fluid overall feel, drawing inspiration from modern mobile operating systems. The implementation of a **Dark Mode** toggle further enhances user customization and accessibility.

8.  **Robust Backend & Database Design:**
    * The application features a well-structured Django backend with a robust database schema. This includes models for Users, Products, Product Images, Chats, and Messages, ensuring efficient data storage and retrieval, and supporting the complex interactions within the platform.

## Technologies Used

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript
* **Styling & Responsiveness:** Bootstrap 4
* **Database:** SQLite (default for development, scalable to PostgreSQL/MySQL for production)
* **User Authentication:** Django's built-in authentication system
* **Image Handling:** Django's ImageField

## Distinctiveness & Complexity Justification

Pileh represents a significant step up in complexity from previous CS50 projects. While it draws inspiration from aspects of the Email (messaging) and Commerce (listing) projects, its unique combination and enhancement of features create a distinct application:

* **Integrated Communication:** The tight integration of direct, product-specific chat goes beyond simple email messaging, enabling real-time negotiation and inquiry directly within the transaction context, a feature absent in the Commerce project.
* **Specialized Data Flow:** The structured, multi-step modal input for electronics specifications demonstrates advanced front-end JavaScript logic and a deeper consideration for database integrity and user experience in a niche market, which was not required in previous general e-commerce platforms.
* **Comprehensive User Experience:** Features like seamless product navigation, dedicated seller profiles, local image uploads, and the Dark Mode toggle contribute to a polished and professional application that prioritizes user convenience and adaptability across devices.

These elements collectively showcase a more ambitious and fully-realized web application, designed not just to meet functional requirements but to provide a cohesive and engaging user journey.

## How to Run the Project

1.  Clone the repository using Git:  
    `git clone https://github.com/ipemw/cs50web-finall-project-capstone-pile.git`

2.  Change into the project directory:  
    `cd cs50web-finall-project-capstone-pile`

3.  Install dependencies: `pip install -r requirements.txt`

4.  Run database migrations: `python manage.py makemigrations` and `python manage.py migrate`

5.  Create a superuser (for admin access): `python manage.py createsuperuser`

6.  Run the development server: `python manage.py runserver`

7.  Access the application at `http://127.0.0.1:8000/` in your browser.

