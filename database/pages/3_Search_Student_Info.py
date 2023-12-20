import streamlit as st
import requests
from PIL import Image
import base64
import pandas as pd

st.set_page_config(page_title="Student's search", layout="wide")

if "res_json_borrow_stab" not in st.session_state:
    st.session_state["res_json_borrow_stab"] = [{}]
if "res_json_return_stab" not in st.session_state:
    st.session_state["res_json_return_stab"] = [{}]
if "original_borrow_stab" not in st.session_state:
    st.session_state["original_borrow_stab"] = [
        Image.new("RGBA", (640, 640), (255, 255, 255, 0))
    ]
if "res_borrow_stab" not in st.session_state:
    st.session_state["res_borrow_stab"] = [
        Image.new("RGBA", (640, 640), (255, 255, 255, 0))
    ]
if "original_return_stab" not in st.session_state:
    st.session_state["original_return_stab"] = [
        Image.new("RGBA", (640, 640), (255, 255, 255, 0))
    ]
if "res_return_stab" not in st.session_state:
    st.session_state["res_return_stab"] = [
        Image.new("RGBA", (640, 640), (255, 255, 255, 0))
    ]


student_id = st.text_input("Input student's ID")

if student_id != "":
    borrow_search = requests.get(
        "http://127.0.0.1:8080/get_student_borrow_by_id",
        params={"student_id": student_id.upper()},
    )
    return_search = requests.get(
        "http://127.0.0.1:8080/get_student_return_by_id",
        params={"student_id": student_id.upper()},
        )
    if borrow_search.status_code == 400:
        st.toast("Can't find student", icon="❌")
        st.session_state["res_json_borrow_stab"].append({})
    else:
        st.session_state["res_json_borrow_stab"].append(borrow_search.json())
    if return_search.status_code == 400:
        st.toast("Can't find student", icon="❌")
        st.session_state["res_json_return_stab"].append({})
    else:
        st.session_state["res_json_return_stab"].append(return_search.json())

col1, col2 = st.columns([1,1])
borrow_col1, borrow_col2 = col1.columns([1,1])
return_col1, return_col2 = col2.columns([1,1])
if st.session_state["res_json_borrow_stab"][-1] != {}:
    col1.text("Borrow")
    borrow_col1.image(base64.b64decode(st.session_state["res_json_borrow_stab"][-1]["Original Image"]))
    borrow_col2.image(base64.b64decode(st.session_state["res_json_borrow_stab"][-1]["Result Image"]))
    col1.dataframe(pd.DataFrame(
            {
                "Borrow tool": [
                    name
                    for name in list(
                        st.session_state["res_json_borrow_stab"][-1].keys()
                    )[5:-1]
                ],
                "Borrow count": [
                    count
                    for count in list(
                        st.session_state["res_json_borrow_stab"][-1].values()
                    )[5:-1]
                ],
            }))
else:
    col1.text("")
    # borrow_col1.image(Image.new("RGBA", (640, 640), (255, 255, 255, 0)))
    # borrow_col2.image(Image.new("RGBA", (640, 640), (255, 255, 255, 0)))
    # col1.dataframe(pd.DataFrame())
if st.session_state["res_json_return_stab"][-1] != {}:
    col2.text("Return")
    return_col1.image(base64.b64decode(st.session_state["res_json_return_stab"][-1]["Original Image"]))
    return_col2.image(base64.b64decode(st.session_state["res_json_return_stab"][-1]["Result Image"]))
    col2.dataframe(pd.DataFrame(
        {
            "Return tool": [
                name
                for name in list(
                    st.session_state["res_json_return_stab"][-1].keys()
                )[5:-1]
            ],
            "Return count": [
                count
                for count in list(
                    st.session_state["res_json_return_stab"][-1].values()
                )[5:-1]
            ],
        }))
else:
    col2.text("")
    # return_col1.image(Image.new("RGBA", (640, 640), (255, 255, 255, 0)))
    # return_col2.image(Image.new("RGBA", (640, 640), (255, 255, 255, 0)))
    # col2.dataframe(pd.DataFrame())
# st.write(st.session_state["res_json_borrow_stab"][-1]) 
# st.write(st.session_state["res_json_return_stab"][-1])

