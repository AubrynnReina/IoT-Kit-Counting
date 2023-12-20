import streamlit as st
from PIL import Image, ImageOps
import pandas as pd
import requests
import base64
import style.style as style

def color_coding(row):
    return ['background-color:transparent'] * len(row) if row["Borrow count"] == row["Return count"] else ['background-color:#FF6969'] * len(row)

def onChange(df):
    df = st.session_state["edit_value_rtab"]

st.set_page_config(page_title="Student's return", layout="wide")

if "original_image_rtab" not in st.session_state:
    st.session_state["original_image_rtab"] = [
        Image.new("RGBA", (640, 640), (255, 255, 255, 0))
    ]
if "res_image_rtab" not in st.session_state:
    st.session_state["res_image_rtab"] = [
        Image.new("RGBA", (640, 640), (255, 255, 255, 0))
    ]
if "res_json_borrow_rtab" not in st.session_state:
    st.session_state["res_json_borrow_rtab"] = [{}]
if "res_json_return_rtab" not in st.session_state:
    st.session_state["res_json_return_rtab"] = [{}]
if "edit_value_rtab" not in st.session_state:
    st.session_state["edit_value_rtab"] = pd.DataFrame()
if "usage_rtab" not in st.session_state:
    st.session_state["usage_rtab"] = [""]


st.markdown(style.hide_menu_style, unsafe_allow_html=True)
st.markdown(style.button_center, unsafe_allow_html=True)

student_id = st.text_input("Student's ID input:", "")
if student_id != "":
    borrow_search = requests.get(
        "http://127.0.0.1:8080/get_student_borrow_by_id",
        params={"student_id": student_id.upper()},
    )
    if borrow_search.status_code == 400:
        st.toast("Student hasn't borrowed yet", icon="❌")
        st.session_state["res_json_borrow_rtab"].append({})
        st.session_state["original_image_rtab"].append(
            Image.new("RGBA", (640, 640), (255, 255, 255, 0))
        )
        st.session_state["res_image_rtab"].append(
            Image.new("RGBA", (640, 640), (255, 255, 255, 0))
        )
    else:
        st.session_state["res_json_borrow_rtab"].append(borrow_search.json())

uploaded_file = st.file_uploader("Choose a file", ["jpg", "png", "jpeg"])
_, button_col1, _, button_col2, _, button_col3, _, button_col4 = st.columns(
    [1, 2, 1, 2, 1, 2, 1, 2]
)
st.subheader(st.session_state["usage_rtab"][-1])
col1, col2 = st.columns(2)

if button_col1.button("Get result"):
    if uploaded_file is not None:
        post_url = "http://127.0.0.1:8080/add_student_return"
        upload_result = requests.post(
            post_url,
            files={"file": uploaded_file.getvalue()},
            params={"student_id": student_id.upper()},
        )

        if not upload_result.status_code == 400:
            json_res = upload_result.json()
            st.session_state["res_json_return_rtab"].append(json_res)
            img = base64.b64decode(json_res["original_image_return"])
            st.session_state["original_image_rtab"].append(img)
            img_res = base64.b64decode(json_res["result_image_return"])
            st.session_state["res_image_rtab"].append(img_res)
        st.session_state["usage_rtab"].append("Return result")
        st.experimental_rerun()
    else:
        st.toast("You haven't uploaded file", icon="❌")

if button_col2.button("Update result"):
    if uploaded_file is not None:
        update_url = "http://127.0.0.1:8080/update_student_return_by_id"
        update_value = dict(
            zip(
                st.session_state["edit_value_rtab"]["Return tool"],
                st.session_state["edit_value_rtab"]["Return count"],
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

if button_col3.button("Show borrow image"):
    if uploaded_file is not None:
        st.session_state["usage_rtab"].append("Borrow result")
        st.session_state["original_image_rtab"].append(
            base64.b64decode(st.session_state["res_json_borrow_rtab"][-1]["Original Image"])
        )
        st.session_state["res_image_rtab"].append(
            base64.b64decode(st.session_state["res_json_borrow_rtab"][-1]["Result Image"])
        )
        st.experimental_rerun()
    else:
        st.toast("You haven't uploaded file", icon="❌")

if button_col4.button("Show return image"):
    if uploaded_file is not None:
        st.session_state["usage_rtab"].append("Return result")
        st.session_state["original_image_rtab"].append(
            base64.b64decode(
                st.session_state["res_json_return_rtab"][-1]["original_image_return"]
            )
        )
        st.session_state["res_image_rtab"].append(
            base64.b64decode(
                st.session_state["res_json_return_rtab"][-1]["result_image_return"]
            )
        )
        st.experimental_rerun()
    else:
        st.toast("You haven't uploaded file", icon="❌")
if st.session_state["original_image_rtab"][-1] == Image.new("RGBA", (640, 640), (255, 255, 255, 0)):
    st.markdown(style.hide_caption, unsafe_allow_html=True)
else:
    st.markdown(style.show_caption, unsafe_allow_html=True)

col1.image(st.session_state["original_image_rtab"][-1], caption="Original image")
col2.image(st.session_state["res_image_rtab"][-1], caption="Result image generated by model")

if st.session_state["res_json_return_rtab"][-1] == {}:
    st.markdown(style.hide_img_fs, unsafe_allow_html=True)
else:
    student_info = requests.get(
        "http://127.0.0.1:8080/get_student_info",
        params={
            "student_id": st.session_state["res_json_return_rtab"][-1]["student_id"]
        },
    ).json()
    st.header(
        f"{student_info['student_id']} - {student_info['student_name']} - {student_info['student_class']} return's result"
    )
    st.markdown(style.show_img_fs, unsafe_allow_html=True)
    edit_value = st.data_editor(pd.DataFrame(
            {
                "Borrow tool": [
                    name
                    for name in list(
                        st.session_state["res_json_borrow_rtab"][-1].keys()
                    )[5:-1]
                ],
                "Borrow count": [
                    count
                    for count in list(
                        st.session_state["res_json_borrow_rtab"][-1].values()
                    )[5:-1]
                ],
                "Return tool": [
                    name
                    for name in list(
                        st.session_state["res_json_return_rtab"][-1].keys()
                    )[3:-1]
                ],
                "Return count": [
                    name
                    for name in list(
                        st.session_state["res_json_return_rtab"][-1].values()
                    )[3:-1]
                ],
            }).style.apply(color_coding, axis=1),
        use_container_width=True,
        disabled=["", "Borrow tool", "Borrow count", "Return tool"],
    )
    st.session_state["edit_value_rtab"] = edit_value
    print(edit_value)

