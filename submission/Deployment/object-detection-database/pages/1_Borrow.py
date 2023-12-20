import streamlit as st
from PIL import Image, ImageOps
import pandas as pd
import requests
import base64
import style.style as style

st.set_page_config(page_title="Student's borrow", layout="wide")

if "original_borrow_btab" not in st.session_state:
    st.session_state["original_borrow_btab"] = [
        Image.new("RGBA", (640, 640), (255, 255, 255, 0))
    ]
if "res_borrow_btab" not in st.session_state:
    st.session_state["res_borrow_btab"] = [
        Image.new("RGBA", (640, 640), (255, 255, 255, 0))
    ]
if "res_json_btab" not in st.session_state:
    st.session_state["res_json_btab"] = [{}]
if "edit_value_btab" not in st.session_state:
    st.session_state["edit_value_btab"] = pd.DataFrame()


st.markdown(style.hide_menu_style, unsafe_allow_html=True)
st.markdown(style.button_center, unsafe_allow_html=True)

student_id = st.text_input("Student's ID input:", "")
if student_id != "":
    if (
        requests.get(
            "http://127.0.0.1:8080/get_student_info",
            params={"student_id": student_id.upper()},
        ).status_code
        == 400
    ):
        st.toast("This is not a FPTU's student", icon="❌")
        st.session_state["res_json_btab"].append({})
        st.session_state["original_borrow_btab"].append(
            Image.new("RGBA", (640, 640), (255, 255, 255, 0))
        )
        st.session_state["res_borrow_btab"].append(
            Image.new("RGBA", (640, 640), (255, 255, 255, 0))
        )


uploaded_file = st.file_uploader("Choose a file", ["jpg", "png", "jpeg"])


_, button_col1, _, button_col2, _ = st.columns([1, 2, 1, 2, 1])


if button_col1.button("Get result"):
    if uploaded_file is not None:
        post_url = "http://127.0.0.1:8080/add_student_borrow"
        upload_result = requests.post(
            post_url,
            files={"file": uploaded_file.getvalue()},
            params={"student_id": student_id.upper()},
        )

        if not upload_result.status_code == 400:
            json_res = upload_result.json()
            st.session_state["res_json_btab"].append(json_res)
            img = base64.b64decode(json_res["original_image_borrow"])
            st.session_state["original_borrow_btab"].append(img)
            img_res = base64.b64decode(json_res["result_image_borrow"])
            st.session_state["res_borrow_btab"].append(img_res)
    else:
        st.toast("You haven't uploaded file", icon="❌")

if button_col2.button("Update result"):
    if uploaded_file is not None:
        update_url = "http://127.0.0.1:8080/update_student_borrow_by_id"
        update_value = dict(
            zip(
                st.session_state["edit_value_btab"]["Name"],
                st.session_state["edit_value_btab"]["Count"],
            )
        )
        update_request = requests.put(
            update_url, json=update_value, params={"student_id": student_id.upper()}
        )

        if update_request.status_code == 400:
            st.toast("Cannot find student in database", icon="❌")
        else:
            st.toast("Update successfully", icon="✅")
    else:
        st.toast("You haven't uploaded file", icon="❌")

col1, col2 = st.columns(2)

col1.image(st.session_state["original_borrow_btab"][-1])
col2.image(st.session_state["res_borrow_btab"][-1])


if st.session_state["res_json_btab"][-1] == {}:
    st.markdown(style.hide_img_fs, unsafe_allow_html=True)
else:
    student_info = requests.get(
        "http://127.0.0.1:8080/get_student_info",
        params={"student_id": st.session_state["res_json_btab"][-1]["student_id"]},
    ).json()
    st.header(
        f"{student_info['student_id']} - {student_info['student_name']} - {student_info['student_class']} borrow's result"
    )
    st.markdown(style.show_img_fs, unsafe_allow_html=True)
    edit_value = st.data_editor(
        pd.DataFrame(
            {
                "Name": [
                    name
                    for name in list(st.session_state["res_json_btab"][-1].keys())[3:-1]
                ],
                "Count": [
                    count
                    for count in list(st.session_state["res_json_btab"][-1].values())[
                        3:-1
                    ]
                ],
            }
        ),
        use_container_width=True,
        hide_index=True,
        disabled=["Name"],
    )
    st.session_state["edit_value_btab"] = edit_value
