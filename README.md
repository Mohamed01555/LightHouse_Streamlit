# Lighthouse: A Streamlit App for Finding Missing Persons

Lighthouse is a web application powered by Streamlit, designed to assist in the rapid and effective identification and location of missing persons. Utilizing advanced facial recognition technology, the app enables parents of missing children and volunteers to upload images, which are then processed and compared to find potential matches.
Key Features:
- User-Friendly Interface: Streamlined workflows for both parents and volunteers to submit critical information and photographs of missing individuals.
- Facial Recognition Matching: Images uploaded are converted into facial embeddings using a custom function. These embeddings are then compared using cosine similarity to identify potential matches - with a high degree of accuracy.
- Automatic Notifications: When a potential match is found, the system automatically notifies the parent, providing details and images of the match.- 
- Data Handling: All data, including images and personal details, are stored securely and are accessible for matching anytime new data is entered into the system.

Technologies:
- Streamlit: For creating the web interface.
- Face Recognition: To generate and compare facial embeddings.
- JSON: For storing volunteer and parent data entries.
- Python Libraries: numpy, face_recognition, and others for handling image processing and facial recognition tasks.

This project aims to harness the power of community and technology to bring families together and provide crucial support in finding lost loved ones. Contributions, suggestions, and feedback are warmly welcomed to improve the effectiveness and reach of this application.
