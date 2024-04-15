import streamlit as st
from utils import * 

os.makedirs(volunteer_images_dir, exist_ok=True)
os.makedirs(parent_images_dir, exist_ok=True)

def main():
    st.title('Find the Missing Child')
    
    # User role selection
    role = st.radio("Are you a:", ("Parent", "Volunteer"))

    if role == "Volunteer":
        st.subheader("Volunteer Information Upload")
        
        if 'vol_child_name' not in st.session_state:
            st.session_state.vol_child_name = None
        
        if 'vol_child_age' not in st.session_state:
            st.session_state.vol_child_age = None
        
        if 'vol_last_seen_location' not in st.session_state:
            st.session_state.vol_last_seen_location = None
        
        if 'vol_last_seen_date' not in st.session_state:
            st.session_state.vol_last_seen_date = None
        
        if 'vol_additional_info' not in st.session_state:
            st.session_state.vol_additional_info = None
        
        if 'vol_image_file' not in st.session_state:
            st.session_state.vol_image_file = None
        st.session_state.vol_child_name = st.text_input("Child's Name", value=st.session_state.vol_child_name,
                                            on_change=lambda: setattr(st.session_state, 'vol_child_name', st.session_state.vol_child_name))
            
        st.session_state.vol_child_age = st.text_input("Child's Age", value=st.session_state.vol_child_age,
                                        on_change=lambda: setattr(st.session_state, 'vol_child_age', st.session_state.vol_child_age))
        
        st.session_state.vol_last_seen_location = st.text_input("Last Seen Location", value=st.session_state.vol_last_seen_location,
                                        on_change=lambda: setattr(st.session_state, 'vol_last_seen_location', st.session_state.vol_last_seen_location))
        
        st.session_state.vol_last_seen_date = st.date_input("Last Seen Date", help="Select the date when the child was last seen.", value=st.session_state.vol_last_seen_date,
                                        on_change=lambda: setattr(st.session_state, 'vol_last_seen_date', st.session_state.vol_last_seen_date))
        
        st.session_state.vol_additional_info = st.text_area("Additional Information", value=st.session_state.vol_additional_info,
                                        on_change=lambda: setattr(st.session_state, 'vol_additional_info', st.session_state.vol_additional_info))
        
        st.session_state.vol_image_file = st.file_uploader("Upload an image of the missing person.Ensure he/she is alone in the image",
                                        type=['jpg', 'png','jpeg'],
                                           )
        with st.form(key='volunteer_form'):
            
            
            submit_button = st.form_submit_button(label='Submit')

            if submit_button:
                if st.session_state.vol_image_file is None:
                    st.warning("Please upload an image of the missing person before submitting.")
                    st.stop()

                else:
                    image_path = os.path.join(volunteer_images_dir, st.session_state.vol_image_file.name)
                    with open(image_path, "wb") as f:
                        f.write(st.session_state.vol_image_file.getbuffer())

                face_encoding = encode_face(image_path)
                if face_encoding is not None:
                        data = {
                            "name": st.session_state.vol_child_name,
                            "age": st.session_state.vol_child_age,
                            "last_seen_location": st.session_state.vol_last_seen_location,
                            "last_seen_date" : str(st.session_state.vol_last_seen_date),
                            "vol_additional_info": st.session_state.vol_additional_info,
                            "face_encoding": face_encoding,
                            "image_path": image_path
                        }
                        save_data("volunteer_db.json", data)
                        st.success("Information uploaded successfully. Thanks for help.")
                else:
                    st.error("No face detected. Please upload a different image.")


    elif role == "Parent":
        st.subheader("Parent Information Upload")
        if 'parent_missing_since' not in st.session_state:
            st.session_state.parent_missing_since = None
        
        if 'parent_child_name' not in st.session_state:
            st.session_state.parent_child_name = ''
        
        if 'parent_child_age' not in st.session_state:
            st.session_state.parent_child_age = ''
        
        
        if 'parent_image_file' not in st.session_state:
            st.session_state.parent_image_file = None
        
        st.session_state.parent_child_name = st.text_input("Your Child's Name", value=st.session_state.parent_child_name,
                                            on_change=lambda: setattr(st.session_state, 'parent_child_name', st.session_state.parent_child_name))
        st.session_state.parent_child_age = st.text_input("Your Child's Age", value=st.session_state.parent_child_age,
                                            on_change=lambda: setattr(st.session_state, 'parent_child_age', st.session_state.parent_child_age))
        st.session_state.parent_missing_since = st.date_input("Missing Since", value=st.session_state.parent_missing_since,
                                                on_change=lambda: setattr(st.session_state, 'parent_missing_since', st.session_state.parent_missing_since))
        
        
        st.session_state.parent_image_file = st.file_uploader(
                "Upload an image of the missing person.Ensure he/she is alone in the image",
                  type=['jpg', 'png','jpeg'],
                                                                )
    
        with st.form(key='parent_form'):
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                
                if st.session_state.parent_image_file is None:
                    st.warning("Please upload an image of the missing person before submitting.")
                    st.stop()
                
                else:
                    image_path = os.path.join(parent_images_dir, st.session_state.parent_image_file.name)
                    with open(image_path, "wb") as f:
                        f.write(st.session_state.parent_image_file.getbuffer())
                    
                    face_encoding = encode_face(image_path)
                    if face_encoding is not None:
                        data = {
                            "name": st.session_state.parent_child_name,
                            "age": st.session_state.parent_child_age,
                            "parent_missing_since": str(st.session_state.parent_missing_since),
                            "face_encoding": face_encoding,
                            "image_path": image_path
                        }
                        save_data("parent_db.json", data)
                        st.success("Information uploaded successfully. Now we search in database. Please Wait 🚨")

                        # Load volunteer data and compare
                        volunteer_data = load_data(volunteer_db)
                        best_match = None
                        highest_similarity = -1  # Start with a low similarity score

                        for entry in volunteer_data:
                            vol_face_encoding = np.array(entry["face_encoding"]['embedding'])
                            
                            similarity = cosine_similarity(vol_face_encoding, face_encoding['embedding'])
                            if similarity > highest_similarity:
                                highest_similarity = similarity
                                best_match = entry

                        if best_match and highest_similarity > 0.5:  # Assuming a threshold of 0.5 for a decent match
                            col1, col2 = st.columns(2)  # Creates two columns
    
                            with col1:  # This block pertains to the first column
                                # image = ImageOps.exif_transpose(image)

                                st.image(ImageOps.exif_transpose(Image.open(best_match["image_path"])), caption="Best Match from Volunteers' uploaded images")
                                st.write(f"Volunteer entered Name: {best_match['name']}")
                                st.write(f"Volunteer entered Age: {best_match['age']}")

                            with col2:  # This block pertains to the second column
                                
                                # Display uploaded image if available in session state
                                st.image(ImageOps.exif_transpose(Image.open(image_path)), caption="Parent Image")
                            st.write(f"Similarity Score: {highest_similarity:.2f}")
                        else:
                            st.info("No match found yet. Please check back later.")
                    else:
                        st.error("No face detected. Please upload a different image.")

if __name__ == "__main__":
    main()